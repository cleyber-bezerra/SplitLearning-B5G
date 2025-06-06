import os
import socket
import pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torch.optim as optim
import time
import sys
from torch.utils.data import DataLoader
from time import process_time
import pandas as pd
import subprocess
import gc
from multiprocessing import shared_memory
import struct
import argparse

# suprimir aviso de atualização de biblioteca
import warnings
warnings.simplefilter("ignore", category=FutureWarning)

# Adiciona o caminho da pasta onde o arquivo está localizado ml_model
file_path = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/models'
sys.path.append(file_path)

import ml_model
import socket_fun as sf
DAM = b'ok!'  # dammy Send credit

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("device: ", device)

mymodel = ml_model.ml_model_hidden().to(device)
print("mymodel: ", mymodel)

# Função para processar o argumento ueNumPergNb
def get_arguments():
    parser = argparse.ArgumentParser(description='Receber o valor de ueNumPergNb.')
    parser.add_argument('ueNumPergNb', type=int, help='Número de UEs a ser processado por cliente.')
    args = parser.parse_args()
    return args.ueNumPergNb

# Recebe o valor ueNumPergNb
ueNumPergNb = get_arguments()
print(f"Valor de ueNumPergNb: {ueNumPergNb}")

# Definir os caminhos de pastas
pastas = ["./csv/ia", "./images"]
for pasta in pastas:
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"Pasta '{pasta}' criada.")

# -------------------- connection ----------------------
user_info = []
host = '127.0.0.1'
port = 19089
ADDR = (host, port)
s = socket.socket()
s.settimeout(7200)  # 7200 seg, 60min, 2h de espera no socket
s.bind(ADDR)

# Inicialização das variáveis de armazenamento dos dados
delays = []
throughput = []
energy_consumption = []
packet_loss = []
distance_device = []

# Tamanho de um valor double (8 bytes)
double_size = 8

# Número total de UEs e número de vetores agora baseado no valor de ueNumPergNb
total_ue_num = ueNumPergNb
num_vectors = 5    # delay, throughput, consumo de energia, perda de pacotes, distance

# Calcular o tamanho do buffer
buffer_size = total_ue_num * num_vectors * double_size

# Função para ler dados da memória compartilhada
def read_shared_memory(name, size, retries=5, delay=1):
    shm = None
    values = None
    delay_vector, throughput_vector, energy_consumption_vector, lost_packets_vector, distance_vetor = [], [], [], [], []
    
    for attempt in range(retries):
        try:
            shm = shared_memory.SharedMemory(name=name)
            buffer = shm.buf[:size]  # Lê exatamente o tamanho esperado

            values = struct.unpack(f'{total_ue_num * num_vectors}d', buffer)
            delay_vector = values[::5]
            throughput_vector = values[1::5]
            energy_consumption_vector = values[2::5]
            lost_packets_vector = values[3::5]
            distance_vetor = values[4::5]

            break

        except Exception as e:
            print(f"Erro ao acessar memória compartilhada: {e}")
            time.sleep(delay)

    if shm:
       try:
          shm.close()  # Fecha o objeto de memória compartilhada
       except Exception as e:
          print(f"Erro ao fechar a memória compartilhada: {e}")

    return delay_vector, throughput_vector, energy_consumption_vector, lost_packets_vector, distance_vetor

# Nome e tamanho da memória compartilhada
shared_memory_name = "ns3_shared_memory"
num_entries = total_ue_num  # Número de clientes
shared_memory_size = num_entries * num_vectors * double_size

python_interpreter = "python3"

# Lista para armazenar subprocessos
subprocesses = []

# Ler os dados da memória compartilhada
try:
    delay_vector, throughput_vector, energy_consumption_vector, lost_packets_vector, distance_vetor = read_shared_memory(shared_memory_name, shared_memory_size)

    if delay_vector and throughput_vector and energy_consumption_vector and lost_packets_vector and distance_vetor:
        for i in range(len(delay_vector)):
            print(f"Entrada {i + 1}: Delay: {delay_vector[i]}, Throughput: {throughput_vector[i]}, Energy Consumption: {energy_consumption_vector[i]}, Packet Loss: {lost_packets_vector[i]}, Distance Device: {distance_vetor[i]}")

        for i in range(len(delay_vector)):
            delay = delay_vector[i]
            throughput = throughput_vector[i]
            energy = energy_consumption_vector[i]
            packet_loss_value = lost_packets_vector[i]
            distance = distance_vetor[i]

            delays.append(delay)
            energy_consumption.append(energy)
            packet_loss.append(packet_loss_value)
            distance_device.append(distance)

            script_path = f"scratch/SplitLearning-B5G/clients/sync/client{i + 1}_sync.py"
            proc = subprocess.Popen(['gnome-terminal', '--', python_interpreter, script_path, str(delay)])
            subprocesses.append(proc)


except Exception as e:
    print(f"Erro ao ler memória compartilhada: {e}")

# Fechar a memória compartilhada corretamente
try:
    shm = shared_memory.SharedMemory(name='ns3_shared_memory')

    for proc in subprocesses:
        proc.wait()

    gc.collect()

    shm.close()
    shm.unlink()

except Exception as e:
    print(f"Erro ao fechar ou remover a memória compartilhada: {e}")

USER = num_entries
s.listen(USER)
print("Waiting clients...")

# Conectar-se com os clientes
for num_user in range(USER):
    conn, addr = s.accept()
    user_info.append({"name": "Client " + str(num_user + 1), "conn": conn, "addr": addr})
    print("Connected with Client " + str(num_user + 1), addr)

for user in user_info:
    recvreq = user["conn"].recv(1024)
    print("Received request message from client <{}>".format(user["addr"]))
    user["conn"].sendall(DAM)

# Treinamento
def train(user):

    p_start = process_time()
    i = 1
    ite_counter = -1
    user_counter = 0
    lr = 0.005
    optimizer = torch.optim.SGD(mymodel.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)
    total_comm_time = 0
    total_comm_data = 0
    
    while True:
        start_comm_time = time.time()
        recv_mode = sf.recv_size_n_msg(user["conn"])
        end_comm_time = time.time()
        total_comm_time += (end_comm_time - start_comm_time)
        total_comm_data += sys.getsizeof(recv_mode)
        if recv_mode == 0:
            
            mymodel.train()
            ite_counter += 1
            print("(USER {}) TRAIN Loading... {}".format(i, ite_counter))

            start_comm_time = time.time()
            recv_data1 = sf.recv_size_n_msg(user["conn"])
            end_comm_time = time.time()
            total_comm_time += (end_comm_time - start_comm_time)
            total_comm_data += sys.getsizeof(recv_data1)

            optimizer.zero_grad()

            output_2 = mymodel(recv_data1)

            start_comm_time = time.time()
            sf.send_size_n_msg(output_2, user["conn"])
            end_comm_time = time.time()
            total_comm_time += (end_comm_time - start_comm_time)
            total_comm_data += sys.getsizeof(output_2)

            recv_grad = sf.recv_size_n_msg(user["conn"])

            output_2.backward(recv_grad)

            optimizer.step()

            start_comm_time = time.time()
            sf.send_size_n_msg(recv_data1.grad, user["conn"])
            end_comm_time = time.time()
            total_comm_time += (end_comm_time - start_comm_time)
            total_comm_data += sys.getsizeof(recv_data1.grad)

        elif recv_mode == 1:
            ite_counter = -1
            mymodel.eval()
            print("(USER {}) TEST Loading...".format(i))

            start_comm_time = time.time()
            recv_data = sf.recv_size_n_msg(user["conn"])
            end_comm_time = time.time()
            total_comm_time += (end_comm_time - start_comm_time)
            total_comm_data += sys.getsizeof(recv_data)

            output_2 = mymodel(recv_data)

            start_comm_time = time.time()
            sf.send_size_n_msg(output_2, user["conn"])
            end_comm_time = time.time()
            total_comm_time += (end_comm_time - start_comm_time)
            total_comm_data += sys.getsizeof(output_2)

        elif recv_mode == 2:
            ite_counter = -1
            print(user["name"], " finished training!!!")
            i = i % USER
            print("Now is user ", i + 1)
            user = user_info[i]
            i += 1

        elif recv_mode == 3:
            user_counter += 1
            i = i % USER
            print(user["name"], "all done!!!!")
            user["conn"].close()
            if user_counter == USER:
                break
            user = user_info[i]
            i += 1

        else:
            print("!!!!! MODE error !!!!!")

    print("=============Training is done!!!!!!===========")
    print("Finished the socket connection(SERVER)")

    p_finish = process_time()

    print("Processing time: ", p_finish - p_start)
    print("Total Communication Time: ", total_comm_time)
    print("Total Communication Data: ", total_comm_data, "bytes")

def main():
    train(user_info[0])

if __name__ == '__main__':
    main()
