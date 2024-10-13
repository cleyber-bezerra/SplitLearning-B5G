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

# Tamanho de cada double (8 bytes)
double_size = 8

# Número total de UEs e número de vetores
total_ue_num = 2  # Este valor deve ser o mesmo que 'totalUeNum' no C++
num_vectors = 4    # delay, throughput, consumo de energia, perda de pacotes

# Calcular o tamanho do buffer
buffer_size = total_ue_num * num_vectors * double_size

# Função para ler dados da memória compartilhada
def read_shared_memory(name, size, retries=5, delay=1):
    shm = None
    values = None
    for attempt in range(retries):
        try:
            shm = shared_memory.SharedMemory(name=name)
            buffer = shm.buf[:size]  # Lê exatamente o tamanho esperado

            # Desempacotar os dados (assumindo um formato contínuo de doubles)
            values = struct.unpack(f'{total_ue_num * num_vectors}d', buffer)

            # Agora os dados são acessíveis em 'values'
            delay_vector = values[::4]
            throughput_vector = values[1::4]
            energy_consumption_vector = values[2::4]
            lost_packets_vector = values[3::4]

            break

        except Exception as e:
            print(f"Erro ao acessar memória compartilhada: {e}")
            time.sleep(delay)

    if shm:
       try:
          shm.close()  # Fecha o objeto de memória compartilhada, mas não chama unlink ainda
       except Exception as e:
          print(f"Erro ao fechar a memória compartilhada: {e}")

    return delay_vector, throughput_vector, energy_consumption_vector, lost_packets_vector

# Nome e tamanho da memória compartilhada
shared_memory_name = "ns3_shared_memory"
num_entries = len([1, 2])  # Número de clientes
shared_memory_size = num_entries * 4 * 8  # 4 valores double por entrada (8 bytes cada): delay, throughput, energy, packet loss

python_interpreter = "python3"


# Lista para armazenar subprocessos
subprocesses = []

# Ler os dados da memória compartilhada
try:
    # Chamada para a função de leitura da memória compartilhada
    delay_vector, throughput_vector, energy_consumption_vector, lost_packets_vector = read_shared_memory(shared_memory_name, shared_memory_size)

    # Verifica se os vetores foram corretamente preenchidos e não estão vazios
    if delay_vector and throughput_vector and energy_consumption_vector and lost_packets_vector:
        # Imprime os valores de cada vetor
        for i in range(len(delay_vector)):
            print(f"Entrada {i + 1}: Delay: {delay_vector[i]}, Throughput: {throughput_vector[i]}, Energy Consumption: {energy_consumption_vector[i]}, Packet Loss: {lost_packets_vector[i]}")

        # Processa cada entrada e inicia subprocessos
        for i in range(len(delay_vector)):
            delay = delay_vector[i]
            throughput = throughput_vector[i]
            energy = energy_consumption_vector[i]
            packet_loss_value = lost_packets_vector[i]

            # Armazena os valores nos respectivos vetores
            delays.append(delay)
            energy_consumption.append(energy)
            packet_loss.append(packet_loss_value)

            # Gera o caminho do script para o cliente correspondente
            script_path = f"scratch/SplitLearning-B5G/clients/sync/client{i + 1}_sync.py"
            
            # Inicia o subprocesso e armazena na lista subprocesses
            proc = subprocess.Popen(['gnome-terminal', '--', python_interpreter, script_path, str(delay)])
            subprocesses.append(proc)  # Armazena o subprocesso para controle futuro

        # Quando todas as leituras estiverem feitas e não houver mais processos utilizando a memória:
        shm = shared_memory.SharedMemory(name=shared_memory_name)
        # shm.unlink()  # Remove a memória compartilhada com segurança
    else:
        print("Os vetores retornados da memória compartilhada estão vazios ou não foram lidos corretamente.")

except Exception as e:
    print(f"Erro ao ler memória compartilhada: {e}")

# Certifique-se de fechar corretamente a memória compartilhada
try:
    # Acessar e manipular a memória compartilhada
    shm = shared_memory.SharedMemory(name='ns3_shared_memory')
    # Aqui manipula os dados...
finally:
    try:
        # Cada processo ou thread deve fechar a memória
        shm = shared_memory.SharedMemory(name='ns3_shared_memory')
        
        # Aguarda todos os subprocessos finalizarem
        for proc in subprocesses:
            proc.wait()  # Use wait() para aguardar a finalização do subprocesso

        # Força a coleta de lixo para garantir que todas as referências foram liberadas
        gc.collect()

        # Fechar a memória compartilhada
        shm.close()
        # Remover a memória compartilhada
        shm.unlink()

    except Exception as e:
        print(f"Erro ao fechar ou remover a memória compartilhada: {e}")


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
