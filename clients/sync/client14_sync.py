import gc
import csv
import os
import socket
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import time
import sys
import copy
from torch.autograd import Variable
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from time import process_time
from datetime import datetime

import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Adiciona o caminho da pasta onde o arquivo está localizado ml_model
file_path = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/models'
sys.path.append(file_path)

import ml_model
import socket_fun as sf

### global variable
### variável global
DAM = b'ok!'    # dammy
MODE = 0    # 0->train, 1->test

BATCH_SIZE = 128

print(" ------ USER 14 ------")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("device: ", device)

# Argumento de linha de comando para delay
if len(sys.argv) < 2:
    print("Uso: client_sync.py <delay>")
    sys.exit(1)

delay = float(sys.argv[1])
print(f"Accuracy recebido: {delay}")

#MNIST
root = './datasets/mnist_data'
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))  # Parâmetros de normalização para MNIST
])

# download dataset
trainset = torchvision.datasets.MNIST(root=root, download=True, train=True, transform=transform)
testset = torchvision.datasets.MNIST(root=root, download=True, train=False, transform=transform)

print("trainset_len: ", len(trainset))
print("testset_len: ", len(testset))
image, label = trainset[0]
print (image.size())

trainloader = DataLoader(trainset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
testloader = DataLoader(testset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

mymodel1 = ml_model.ml_model_in().to(device)
mymodel2 = ml_model.ml_model_out(NUM_CLASSES=10).to(device)

# -------------------- connection ----------------------
# -------------------- conexão ----------------------
# socket establish
# estabelecimento de soquete
host = '127.0.0.1'
port = 19089
ADDR = (host, port)

# CONNECT
# CONECTAR
s = socket.socket()
s.connect(ADDR)
w = 'start communication'

# SEND
# ENVIAR
s.sendall(w.encode())
print("sent request to a server")
dammy = s.recv(4)

# ------------------ start training -----------------
# ------------------ comece a treinar -----------------
epochs = 1
lr = 0.005

# set error function
# define função de erro
criterion = nn.CrossEntropyLoss()

# set optimizer
# definir otimizador
optimizer1 = optim.SGD(mymodel1.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)
optimizer2 = optim.SGD(mymodel2.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)



def train():
    global comm_time, comm_data_size

    # forward prop. function
    # suporte para frente. função
    def forward_prop(MODEL, data):

        output = None
        if MODEL == 1:
            optimizer1.zero_grad()
            output_1 = mymodel1(data)
            time.sleep(0.3521)  # Adiciona latência na ativação
            output = output_1
        elif MODEL == 2:
            optimizer2.zero_grad()
            output_2 = mymodel2(data)
            time.sleep(0.3521)  # Adiciona latência na ativação
            output = output_2
        else:
            print("!!!!! MODEL not found !!!!!")

        return output

    train_acc_list, val_acc_list = [], []
    #p_time_list = []

    for e in range(epochs):
        print("--------------- Epoch: ", e +1 , " --------------")
        train_acc = 0
        val_acc = 0

        p_start = process_time()
        # ================= train mode ================
        # ================= modo trem ================
        mymodel1.train()
        mymodel2.train()
        ### send MODE
        ### enviar MODO
        MODE = 0    # train mode -> 0:train, 1:test, 2:finished train, 3:finished test
        MODEL = 1   # train model
        for data, labels in tqdm(trainloader):
            # send MODE number
            # envia o número do MODO
            sf.send_size_n_msg(MODE, s)
        
            data = data.to(device)
            labels = labels.to(device)

            output_1 = forward_prop(MODEL, data)

            #time.sleep(delay)
            # SEND ----------- feature data 1 ----------------
            # ENVIAR ----------- dados do recurso 1 ---------------
            start_time = process_time()
            sf.send_size_n_msg(output_1, s)
            
            

            ### wait for SERVER to calculate... ###
            ### espere o SERVIDOR calcular... ###

            # RECEIVE ------------ feature data 2 -------------
            # RECEBER ------------ dados do recurso 2 -------------
            start_time = process_time()
            recv_data2 = sf.recv_size_n_msg(s)
            
            

            # recebe dados do recurso 2 -> MODEL=2
            MODEL = 2   # receive feature data 2 -> MODEL=2

            # start forward prop. 3
            # inicia a hélice para frente. 3
            OUTPUT = forward_prop(MODEL, recv_data2)

            loss = criterion(OUTPUT, labels)

            loss.backward()     # parts out-layer (peças da camada externa)

            optimizer2.step()

            # SEND ------------- grad 2 -----------
            # ENVIAR ------------- 2ª série -----------
            start_time = process_time()
            sf.send_size_n_msg(recv_data2.grad, s)
            
            

            #time.sleep(delay)
            # RECEIVE ----------- grad 1 -----------
            # RECEBER ----------- 1ª série -----------
            start_time = process_time()
            recv_grad = sf.recv_size_n_msg(s)
            
            

            MODEL = 1

            
            train_acc += (OUTPUT.max(1)[1] == labels).sum().item()

            output_1.backward(recv_grad)    # parts in-layer (peças em camada)
            time.sleep(0.3521)  # Adiciona latência no gradiente

            optimizer1.step()
        
        
        avg_train_acc = train_acc / len(trainloader.dataset)
        
        print("train mode finished!!!!")
        
         
        train_acc_list.append(avg_train_acc)

        # =============== test mode ================
        # =============== modo de teste ================
        mymodel1.eval()
        mymodel2.eval()

        with torch.no_grad():
            print("start test mode!")
            MODE = 1    # change mode to test (mude o modo para testar)
            for data, labels in tqdm(testloader):
                # send MODE number
                # envia o número do MODO
                sf.send_size_n_msg(MODE, s)

                data = data.to(device)
                labels = labels.to(device)
                output = mymodel1(data)

                # SEND --------- feature data 1 -----------
                # ENVIAR --------- dados do recurso 1 -----------
                start_time = process_time()
                sf.send_size_n_msg(output, s)
                
                

                ### wait for the server...
                ### espere pelo servidor...

                # RECEIVE ----------- feature data 2 ------------
                # RECEBER ----------- dados do recurso 2 ------------
                start_time = process_time()
                recv_data2 = sf.recv_size_n_msg(s)
                
                

                OUTPUT = mymodel2(recv_data2)
                #loss = criterion(OUTPUT, labels)

                #val_loss += loss.item()
                val_acc += (OUTPUT.max(1)[1] == labels).sum().item()

        p_finish = process_time()
        p_time = p_finish-p_start
        if e == epochs-1:
            MODE = 3
        else:                                 
            MODE = 2    # finished test -> start next client's training
        sf.send_size_n_msg(MODE, s)           
        print("Processing time: ", p_time)
         #p_time_list.append(p_time)

        #avg_val_loss = val_loss / len(testloader.dataset)
        avg_val_acc = val_acc / len(testloader.dataset)
        
        print ('Epoch [{}/{}], Acc: {acc:.5f}, val_acc: {val_acc:.5f}' 
                    .format(e+1, epochs, acc=avg_train_acc, val_acc=avg_val_acc))
        
        
        val_acc_list.append(avg_val_acc)

        if e == epochs-1: 
            s.close()
            print("Finished the socket connection(USER 14)")



    return train_acc_list, val_acc_list



def write_to_csv(train_acc_list, val_acc_list):
    print("Inicio funcao CSV")
    print(train_acc_list)
    print(val_acc_list)

    file_dir = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file = os.path.join(file_dir, 'result_train_sync.csv')

    try:
        file_exists = os.path.isfile(file)
        with open(file, 'a', newline='') as f:
            csv_writer = csv.writer(f)

            if not file_exists:
                csv_writer.writerow(['User', 'Train Accuracy', 'Validation Accuracy', 'Timestamp'])

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            result = [
                'user 14',
                ','.join(map(str, train_acc_list)),  # Converte a lista em string separada por vírgulas
                ','.join(map(str, val_acc_list)),
                timestamp
            ]
            csv_writer.writerow(result)
            print(result)

    except Exception as e:
        print(f"Erro ao tentar escrever no CSV: {e}")

if __name__ == '__main__':
    train_acc_list, val_acc_list = train()
    print("Fim de treino!")
    write_to_csv(train_acc_list, val_acc_list)
