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
import subprocess
import pandas as pd
from multiprocessing import shared_memory
import struct

#suprimir aviso de atualização de biblioteca
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

### DEFINIR OS CAMINHOS DE PASTAS
pastas = ["./csv/ia", "./images"]
# Verificar e criar as pastas se não existirem
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

# Aqui assumimos que 'delays','throughput', 'energy_consumption' e 'packet_loss' são lidos da memória compartilhada
delays = []
throughput = []
energy_consumption = []
packet_loss = []

# Função para ler dados da memória compartilhada
def read_shared_memory(name, size, retries=5, delay=1):
    for attempt in range(retries):
        try:
            shm = shared_memory.SharedMemory(name=name)
            data = shm.buf[:size]
            return shm, struct.unpack('d' * (size // 8), data)  # Retorna o objeto shm e os dados
        except FileNotFoundError:
            print(f"Memória compartilhada '{name}' não encontrada. Tentativa {attempt + 1} de {retries}")
            time.sleep(delay)
        except Exception as e:
            print(f"Erro ao acessar memória compartilhada: {e}")
            break
    return None, None  # Retorna None se não conseguir ler

# Nome e tamanho da memória compartilhada
shared_memory_name = "ns3_shared_memory"
num_entries = len([1, 2, 3, 4, 5, 6]) #NÚMERO DE CLIENTES
shared_memory_size = num_entries * 4 * 8  # 4 valores double por entrada (8 bytes cada): delay, throughput, energy, packet loss

# Ler os dados da memória compartilhada
shm, shared_data = read_shared_memory(shared_memory_name, shared_memory_size)

python_interpreter = "python3"

if shared_data:
    for i in range(num_entries):
        delay = shared_data[i * 4]
        throughput = shared_data[i * 4 + 1]
        energy = shared_data[i * 4 + 2]
        packet_loss_value = shared_data[i * 4 + 3]

        print(f"Entrada {i + 1}: Delay: {delay}, Throughput: {throughput}, Energy Consumption: {energy}, Packet Loss: {packet_loss_value}")

        # Armazena os valores nos respectivos vetores
        delays.append(delay)
        energy_consumption.append(energy)
        packet_loss.append(packet_loss_value)

        #script_path = f"./clients/sync/client{i + 1}_sync.py"
        script_path = f"scratch/SplitLearning-B5G/clients/sync/client{i + 1}_sync.py"
        subprocess.Popen(['gnome-terminal', '--', python_interpreter, script_path, str(delay)])

else:
    print("Erro ao ler memória compartilhada.")

# Limpar a memória compartilhada
if shm:
    shm.close()  # Fecha o objeto de memória compartilhada
    shm.unlink()  # Remove o objeto de memória compartilhada

USER = num_entries  # Número de clientes a serem atendidos simultaneamente do CSV.
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


# ------------------- start training --------------------
def train(user):

    p_start = process_time()

    i = 1
    ite_counter = -1
    user_counter = 0
    lr = 0.005
    optimizer = torch.optim.SGD(mymodel.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)

    # Variáveis para contabilizar a sobrecarga de comunicação
    total_comm_time = 0
    total_comm_data = 0
    
    while True:

        ### receive MODE
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

# Função principal para iniciar o treinamento
def main():
    train(user_info[0])

if __name__ == '__main__':
    main()
