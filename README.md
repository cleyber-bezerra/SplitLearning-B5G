# SplitLearning-B5G

<p align='center' style="margin-bottom: -4px">Cleyber Bezerra dos Reis<sup>1</sup>, Antonio Oliveira-JR<sup>1</sup></p>
<p align='center' style="margin-bottom: -4px"><sup>1</sup>Instituto de Informática, Universidade Federal de Goiás</p>
<p align='center' style="margin-bottom: -4px">E-mail: {cleyber.bezerra}@discente.ufg.br</p>
<p align='center'>E-mail: {antonio}@inf.ufg.br</p>

# Description
O repositório contém todo o desenvolvimento referente à dissertação de mestrado intitulada "Split Learning como habilitador de redes sem fio para futuras gerações". Sendo desenvolvida por meio do Curso de Mestrado Acadêmico em Ciência da Computação - Presencial - Goiânia, pelo Instituto de Informática (INF) da Universidade Federal de Goiás (UFG).

# Table of Contents
- [Article Summary](#getting-started)
	- [Abstract](#abstract)
	- [Baselines](#baselines)
	- [Results](#results)
- [Replicating the Experiment](#replicating-the-experiment)
	- [Requirements](#requirements)
	- [Preparing Environment](#preparing-environment)
 	- [Run Experiments](#run-experiments)

- [How to cite](#how-to-cite)

## Abstract

Split Learning (SL) is a promising approach as an effective solution to data security and privacy concerns in training Deep Neural Networks (DNN), due to its approach characteristics of combining raw data security and the division of the model between client devices and central server.


[Back to TOC](#table-of-contents)

## Baselines

The methods defined as baselines for our proposal: (1) the use of the asynchronous algorithm in training the Split Learning model and (2) the definition of training based on events provided from the simulation in NS3 based on the established latency policy. The training uses the file provided by the simulation (simulator_ns3.csv). 10 devices are simulated and the established policy for network latency is nodes below 04 seconds.

[Back to TOC](#table-of-contents)

## Results
### Results in the communication network environment.

Demonstrations of results within the scope of simulation on the Wi-Fi network, graphically presenting: latencies, transfer rates, packet loss rates and energy consumption.

<p align='center'>
    <img src='/images/figure1.png' width='500'>
</p>    
<p align='center'>
    <figurecaption>
        Fig. 1. Latencys.
    </figurecaption>
</p>

Figure 1 shows the result of latencies in the network simulation.


<p align='center'>
    <img src='/images/figure2.png' width='500'>
</p>    
<p align='center'>
    <figurecaption>
        Fig. 2. Packet Losses.
    </figurecaption>
</p>

Figure 2 shows the result of packet losses in the network simulation.


<p align='center'>
    <img src='/images/figure3.png' width='500'>
</p>    
<p align='center'>
    <figurecaption>
        Fig. 3. Throughput.
    </figurecaption>
</p>

Figure 3 demonstrates the throughput results in the network simulation.

<p align='center'>
    <img src='/images/figure4.png' width='500'>
</p>    
<p align='center'>
    <figurecaption>
        Fig. 4. Throughput.
    </figurecaption>
</p>

Figure 4 demonstrates the energy consumption results in the network simulation.

### Results in the machine learning environment with training and testing

<p align='center'>
    <img src='/images/figure5.png' width='500'>
</p>    
<p align='center'>
    <figurecaption>
        Fig. 5. Accuracy per Round.
    </figurecaption>
</p>
Figure 5 shows the result of accuracy per round during training and testing in the Split Learning learning model.

<p align='center'>
    <img src='/images/figure6.png' width='500'>
</p>    
<p align='center'>
    <figurecaption>
        Fig. 6. Processing Accuracy.
    </figurecaption>
</p>

Figure 6 demonstrates the processing accuracy results during training and testing in the Split Learning learning model.

[Back to TOC](#table-of-contents)

# Replicating The Experiment

## Requirements

- GNU (>=8.0.0)
  
  command to know the version of KERNEL, GCC and GNU Binutils in the terminal
  ```bash
	cat /proc/version
  ```
- GCC (>=11.4.0)
  
  commands to know the GCC version in the terminal.
  ```bash
	gcc --version
	ls -l /usr/bin/gcc*
  ```
- CMAKE (>=3.24)
  
  command to know the version of CMAKE in the terminal.
  ```bash
	cmake --version
  ```
- python (>=3.11.5)
  
  commands to know the version of PYTHON in the terminal.
  ```bash
	python --version
	python3 --version
  ```
- [ns-allinone (3.42)](https://www.nsnam.org/releases/ns-3-42/download/ )
  
[Back to TOC](#table-of-contents)

## Preparing Environment
#INSTALANDO O GCC E MAKE
```bash
    sudo apt update
    sudo apt install build-essential
    sudo apt install gcc-10 g++-10
```

```bash
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100
```

```bash
    gcc --version
    make --version
```

#INSTALANDO O CMAKE

abaixe o arquivo na versão desejada
https://cmake.org/download/

faça a extração no terminal, acesse a pasta e execute o comando:
```bash
    ./bootstrap && make && sudo make install
```

#INSTALANDO O GIT
```bash
    sudo apt-get install git -y
```
#INSTALANDO O NS-3-DEV
```bash
    git clone https://gitlab.com/nsnam/ns-3-dev.git
    git checkout -b ns-3.43-release ns-3.43
```
#CONFIGURAR E COMPILAR O NS-3
dentro da pasta ns-3-dev use os comandos:
```bash
    ./ns3 configure --enable-examples --enable-tests
    ./ns3 build
```

#INSTALAR O NR-LENA
```bash
    sudo apt-get install libc6-dev
    sudo apt-get install sqlite sqlite3 libsqlite3-dev
    sudo apt-get install libeigen3-dev
```

```bash
    cd contrib
    git clone https://gitlab.com/cttc-lena/nr.git
    cd nr
    git checkout -b 5g-lena-v3.1.y origin/5g-lena-v3.1.y
```
#INSTALAR O NS3-IA
```bash
    sudo apt install python3-pip
    
    pip install tensorflow==2.17.0
    pip install cloudpickle==1.2.0
    pip install pyzmq
    pip install protobuf==3.20.3
    pip install tensorflow-estimator==2.15.0
    pip install tensorboard==2.17.0

    pip install numpy==1.18.1
    pip install Keras==3.2.0
    pip install Keras-Applications==1.0.8
    pip install Keras-Preprocessing==1.1.2

    pip install matplotlib==3.3.2
    pip install psutil==5.7.2
```

```bash
    cd contrib/
    git clone https://github.com/hust-diangroup/ns3-ai.git

    cd ns3-ai/py_interface
    pip3 install . --user
```

#HABILITAR MODULOS
```bash
    ./ns3 configure --enable-modules=nr,internet-apps,flow-monitor,config-store,buildings,applications,network,core,wifi,energy,spectrum,propagation,mobility,antenna
```

#BAIXAR PROJETO

dentro da pasta ns-3-dev/scracth use os comandos:
```bash
git clone https://github.com/cleyber-bezerra/SplitLearning-B5G.git
```
[Back to TOC](#table-of-contents)

## Run Experiments

#EXECUTAR PROJETO

dentro da pasta SplitLearning executer o arquivo de script.
```bash
    ./simulator_ns3.sh
```

[Back to TOC](#table-of-contents)

