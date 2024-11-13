SplitLearning-B5G

#INSTALANDO O GCC E MAKE
``shell
sudo apt update
sudo apt install build-essential
sudo apt install gcc-10 g++-10
``

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100

gcc --version
make --version

#INSTALANDO O OPENSSL

#INSTALANDO O CMAKE
https://cmake.org/download/
baixar o arquivo e extrair
no terminal acesse a pasta
./bootstrap && make && sudo make install

#INSTALANDO O GIT
sudo apt-get install git -y

#INSTALANDO O NS-3-DEV
git clone https://gitlab.com/nsnam/ns-3-dev.git
git checkout -b ns-3.43-release ns-3.43

#CONFIGURAR E COMPILAR O NS-3
dentro da pasta ns-3-dev use os comandos:
./ns3 configure --enable-examples --enable-tests
./ns3 build

#INSTALAR O NR-LENA
sudo apt-get install libc6-dev
sudo apt-get install sqlite sqlite3 libsqlite3-dev
sudo apt-get install libeigen3-dev

cd contrib
git clone https://gitlab.com/cttc-lena/nr.git
cd nr
git checkout -b 5g-lena-v3.1.y origin/5g-lena-v3.1.y

#INSTALAR O NS3-IA
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

cd contrib/
git clone https://github.com/hust-diangroup/ns3-ai.git

cd ns3-ai/py_interface
pip3 install . --user

#HABILITAR MODULOS
./ns3 configure --enable-modules=nr,internet-apps,flow-monitor,config-store,buildings,applications,network,core,wifi,energy,spectrum,propagation,mobility,antenna


#BAIXAR PROJETO
dentro da pasta ns-3-dev/scracth use os comandos:

