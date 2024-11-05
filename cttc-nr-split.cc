#include "ns3/antenna-module.h"
#include "ns3/applications-module.h"
#include "ns3/buildings-module.h"
#include "ns3/config-store-module.h"
#include "ns3/core-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/internet-apps-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/nr-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/constant-position-mobility-model.h"
#include "ns3/random-variable-stream.h"
#include "ns3/position-allocator.h"
#include <vector>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <iostream> 
#include <sstream>
#include <sys/mman.h>  // Para mmap, munmap
#include <sys/stat.h>  // Para shm_open, shm_unlink
#include <fcntl.h>     // Para O_CREAT, O_RDWR
#include <unistd.h>    // Para close
#include <cstdlib>     // Para system

using namespace ns3;
NS_LOG_COMPONENT_DEFINE("CttcNrDemo");

// Função para verificar se o arquivo existe
bool fileExists(const std::string& filename) {
    return std::filesystem::exists(filename);
}

// Função para escrever cabeçalhos apenas se o arquivo não existir
void writeHeader(std::ofstream& file, const std::string& header) {
    // Escreve o cabeçalho se o arquivo estiver vazio (ou seja, acabou de ser criado)
    if (file.tellp() == std::ofstream::pos_type(0)) {
        file << header;
    }
}


int main(int argc, char* argv[])
{

    // Definir a seed fixa para a simulação
    //SeedManager::SetSeed(2); // Fixa a seed para garantir que os valores aleatórios sejam repetíveis
    //SeedManager::SetRun(2);  // Define o número da "run" para criar diferentes execuções com a mesma seed, se necessário

    SeedManager::SetSeed(time(0)); // Usar o tempo atual como seed para gerar aleatoriedade
    SeedManager::SetRun(time(0) % 100);  // Incremental ou aleatório


    uint16_t gNbNum = 1;
    uint16_t ueNumPergNb = 10;
    bool logging = false;
    bool doubleOperationalBand = true;
    uint32_t udpPacketSizeULL = 100;
    uint32_t udpPacketSizeBe = 1252;
    uint32_t lambdaULL = 10000;
    uint32_t lambdaBe = 10000;
    Time simTime = MilliSeconds(1000);
    Time udpAppStartTime = MilliSeconds(400);
    uint16_t numerologyBwp1 = 4;
    double centralFrequencyBand1 = 28e9;
    double bandwidthBand1 = 800e6;
    uint16_t numerologyBwp2 = 2;
    double centralFrequencyBand2 = 28.2e9;
    double bandwidthBand2 = 800e6;
    double totalTxPower = 35;
    std::string simTag = "default";
    std::string outputDir = "./";
    uint32_t totalUeNum = ueNumPergNb * gNbNum; // Calculando o número total de UEs
    double distanceLimit = 200.0; // Limite de distanciamento em metros
    double processingPowerPerUE = 0.05; //potencia estimada para processamento por UE
    double lossExponent = 2.0; // 2,3,4


// ALOCACAO DE MEMORIA DOS VETORES
    std::vector<uint32_t> lostPacketsVector(totalUeNum);
    std::vector<double> throughputVector(totalUeNum, 0.0);
    std::vector<double> delayVector(totalUeNum, 0.0);
    std::vector<double> energyConsumption(totalUeNum, 0.0); // ou algum valor padrão
    std::vector<double> distanceVector(totalUeNum, 0.0);
    std::vector<uint32_t> deviceTypeVector(totalUeNum, 0); // 0 para smartphone, 1 para IoT
    std::vector<double> jitterVector(totalUeNum, 0.0); // Inicializa o vetor de jitter com zero


    CommandLine cmd(__FILE__);
    cmd.AddValue("gNbNum", "The number of gNbs in multiple-ue topology", gNbNum);
    cmd.AddValue("ueNumPergNb", "The number of UE per gNb in multiple-ue topology", ueNumPergNb);
    cmd.AddValue("logging", "Enable logging", logging);
    cmd.AddValue("doubleOperationalBand", "If true, simulate two operational bands with one CC for each band, and each CC will have 1 BWP that spans the entire CC.", doubleOperationalBand);
    cmd.AddValue("packetSizeUll", "packet size in bytes to be used by ultra low latency traffic", udpPacketSizeULL);
    cmd.AddValue("packetSizeBe", "packet size in bytes to be used by best effort traffic", udpPacketSizeBe);
    cmd.AddValue("lambdaUll", "Number of UDP packets in one second for ultra low latency traffic", lambdaULL);
    cmd.AddValue("lambdaBe", "Number of UDP packets in one second for best effor traffic", lambdaBe);
    cmd.AddValue("simTime", "Simulation time", simTime);
    cmd.AddValue("numerologyBwp1", "The numerology to be used in bandwidth part 1", numerologyBwp1);
    cmd.AddValue("centralFrequencyBand1", "The system frequency to be used in band 1", centralFrequencyBand1);
    cmd.AddValue("bandwidthBand1", "The system bandwidth to be used in band 1", bandwidthBand1);
    cmd.AddValue("numerologyBwp2", "The numerology to be used in bandwidth part 2", numerologyBwp2);
    cmd.AddValue("centralFrequencyBand2", "The system frequency to be used in band 2", centralFrequencyBand2);
    cmd.AddValue("bandwidthBand2", "The system bandwidth to be used in band 2", bandwidthBand2);
    cmd.AddValue("totalTxPower", "total tx power that will be proportionally assigned to bands, CCs and bandwidth parts depending on each BWP bandwidth ", totalTxPower);
    cmd.AddValue("simTag", "tag to be appended to output filenames to distinguish simulation campaigns", simTag);
    cmd.AddValue("outputDir", "directory where to store simulation results", outputDir);
    cmd.AddValue("lossExponent", "Loss exponent for signal attenuation (2=residential, 3=open, 4=urban)", lossExponent);
    cmd.Parse(argc, argv);

    NS_ABORT_IF(centralFrequencyBand1 < 0.5e9 && centralFrequencyBand1 > 100e9);
    NS_ABORT_IF(centralFrequencyBand2 < 0.5e9 && centralFrequencyBand2 > 100e9);
    
    if (logging)
    {
        LogComponentEnable("UdpClient", LOG_LEVEL_INFO);
        LogComponentEnable("UdpServer", LOG_LEVEL_INFO);
        LogComponentEnable("LtePdcp", LOG_LEVEL_INFO);
    }

    Config::SetDefault("ns3::LteRlcUm::MaxTxBufferSize", UintegerValue(999999999));

    GridScenarioHelper gridScenario;
    gridScenario.SetRows(1);
    gridScenario.SetColumns(gNbNum);
    gridScenario.SetHorizontalBsDistance(10.0);
    gridScenario.SetVerticalBsDistance(10.0);
    gridScenario.SetBsHeight(10);
    gridScenario.SetUtHeight(1.5);
    gridScenario.SetSectorization(GridScenarioHelper::SINGLE);
    gridScenario.SetBsNumber(gNbNum);
    gridScenario.SetUtNumber(ueNumPergNb * gNbNum);
    gridScenario.SetScenarioHeight(3);
    gridScenario.SetScenarioLength(3);
    gridScenario.CreateScenario();

    MobilityHelper mobility;
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");

    // Definir posições fixas para gNBs (Base Stations)
    mobility.Install(gridScenario.GetBaseStations());
    
    // Configuração do posicionamento aleatório para os UEs
    Ptr<UniformRandomVariable> x = CreateObject<UniformRandomVariable>();
    x->SetAttribute("Min", DoubleValue(0.0));
    x->SetAttribute("Max", DoubleValue(150.0));

    Ptr<UniformRandomVariable> y = CreateObject<UniformRandomVariable>();
    y->SetAttribute("Min", DoubleValue(0.0));
    y->SetAttribute("Max", DoubleValue(150.0));

    // Define Z constante
    Ptr<ConstantRandomVariable> z = CreateObject<ConstantRandomVariable>();
    z->SetAttribute("Constant", DoubleValue(1.5));

    Ptr<RandomBoxPositionAllocator> randomPositionAlloc = CreateObject<RandomBoxPositionAllocator>();
    randomPositionAlloc->SetX(x);
    randomPositionAlloc->SetY(y);
    randomPositionAlloc->SetZ(z);  // Define Z fixo em 1.5

    // Aplicar o modelo de mobilidade com posições aleatórias para os UEs
    mobility.SetPositionAllocator(randomPositionAlloc);
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(gridScenario.GetUserTerminals());

    // Cálculo do consumo de energia baseado na distância
    for (uint32_t i = 0; i < gridScenario.GetUserTerminals().GetN(); ++i) {
        Ptr<Node> ueNode = gridScenario.GetUserTerminals().Get(i);
        Ptr<MobilityModel> mob = ueNode->GetObject<MobilityModel>();
        Vector uePos = mob->GetPosition();

        // Calcular distância para a gNB mais próxima
        Ptr<Node> gNbNode = gridScenario.GetBaseStations().Get(0);  // Supondo que a gNB 0 é a mais próxima
        Ptr<MobilityModel> gNbMob = gNbNode->GetObject<MobilityModel>();
        Vector gNbPos = gNbMob->GetPosition();

        double distance = std::sqrt(std::pow(uePos.x - gNbPos.x, 2) + std::pow(uePos.y - gNbPos.y, 2) + std::pow(uePos.z - gNbPos.z, 2));
        distanceVector[i] = distance;

        // Calcular consumo de energia baseado na distância (exemplo: proporcional ao quadrado da distância)
        double distanceFactor = (distance > 0) ? distance : 1.0; // Evita divisão por zero
        double powerConsumption = processingPowerPerUE * std::pow(distanceFactor, 2); // Exemplo de consumo quadrático

        // Armazenar o consumo de energia diretamente em energyConsumption
        energyConsumption[i] = powerConsumption * simTime.GetSeconds();


        if (distance > distanceLimit) {
            std::cerr << "O UE " << ueNode->GetId() << " está a " << distance << " metros, fora do limite de " << distanceLimit << " metros.\n";
        }
    }


    NodeContainer ueLowLatContainer;
    NodeContainer ueVoiceContainer;
    for (uint32_t j = 0; j < gridScenario.GetUserTerminals().GetN(); ++j)
    {
        Ptr<Node> ue = gridScenario.GetUserTerminals().Get(j);
        if (j % 2 == 0)
        {
            ueLowLatContainer.Add(ue);
        }
        else
        {
            ueVoiceContainer.Add(ue);
        }
    }

    NS_LOG_INFO("Creating " << gridScenario.GetUserTerminals().GetN() << " user terminals and " << gridScenario.GetBaseStations().GetN() << " gNBs");

    Ptr<NrPointToPointEpcHelper> epcHelper = CreateObject<NrPointToPointEpcHelper>();
    Ptr<IdealBeamformingHelper> idealBeamformingHelper = CreateObject<IdealBeamformingHelper>();
    Ptr<NrHelper> nrHelper = CreateObject<NrHelper>();
    nrHelper->SetBeamformingHelper(idealBeamformingHelper);
    nrHelper->SetEpcHelper(epcHelper);

    BandwidthPartInfoPtrVector allBwps;
    CcBwpCreator ccBwpCreator;
    const uint8_t numCcPerBand = 1;
    CcBwpCreator::SimpleOperationBandConf bandConf1(centralFrequencyBand1, bandwidthBand1, numCcPerBand, BandwidthPartInfo::UMi_StreetCanyon);
    CcBwpCreator::SimpleOperationBandConf bandConf2(centralFrequencyBand2, bandwidthBand2, numCcPerBand, BandwidthPartInfo::UMi_StreetCanyon);
    OperationBandInfo band1 = ccBwpCreator.CreateOperationBandContiguousCc(bandConf1);
    OperationBandInfo band2 = ccBwpCreator.CreateOperationBandContiguousCc(bandConf2);

    Config::SetDefault("ns3::ThreeGppChannelModel::UpdatePeriod", TimeValue(MilliSeconds(0)));
    nrHelper->SetChannelConditionModelAttribute("UpdatePeriod", TimeValue(MilliSeconds(0)));
    nrHelper->SetPathlossAttribute("ShadowingEnabled", BooleanValue(false));
    nrHelper->InitializeOperationBand(&band1);

    double totalBandwidth = bandwidthBand1;
    if (doubleOperationalBand)
    {
        nrHelper->InitializeOperationBand(&band2);
        totalBandwidth += bandwidthBand2;
        allBwps = CcBwpCreator::GetAllBwps({band1, band2});
    }
    else
    {
        allBwps = CcBwpCreator::GetAllBwps({band1});
    }

    Packet::EnableChecking();
    Packet::EnablePrinting();
    idealBeamformingHelper->SetAttribute("BeamformingMethod", TypeIdValue(DirectPathBeamforming::GetTypeId()));

    epcHelper->SetAttribute("S1uLinkDelay", TimeValue(MilliSeconds(0)));

    nrHelper->SetUeAntennaAttribute("NumRows", UintegerValue(2));
    nrHelper->SetUeAntennaAttribute("NumColumns", UintegerValue(4));
    nrHelper->SetUeAntennaAttribute("AntennaElement", PointerValue(CreateObject<IsotropicAntennaModel>()));

    nrHelper->SetGnbAntennaAttribute("NumRows", UintegerValue(4));
    nrHelper->SetGnbAntennaAttribute("NumColumns", UintegerValue(8));
    nrHelper->SetGnbAntennaAttribute("AntennaElement", PointerValue(CreateObject<IsotropicAntennaModel>()));

    NetDeviceContainer enbNetDev = nrHelper->InstallGnbDevice(gridScenario.GetBaseStations(), allBwps);
    NetDeviceContainer ueLowLatNetDev = nrHelper->InstallUeDevice(ueLowLatContainer, allBwps);
    NetDeviceContainer ueVoiceNetDev = nrHelper->InstallUeDevice(ueVoiceContainer, allBwps);

    nrHelper->GetGnbPhy(enbNetDev.Get(0), 0)->SetAttribute("Numerology", UintegerValue(numerologyBwp1));
    nrHelper->GetGnbPhy(enbNetDev.Get(0), 0)->SetAttribute("TxPower", DoubleValue(10 * log10((bandwidthBand1 / totalBandwidth) * pow(10, totalTxPower / 10))));

    if (doubleOperationalBand)
    {
        nrHelper->GetGnbPhy(enbNetDev.Get(0), 1)->SetAttribute("Numerology", UintegerValue(numerologyBwp2));
        nrHelper->GetGnbPhy(enbNetDev.Get(0), 1)->SetTxPower(10 * log10((bandwidthBand2 / totalBandwidth) * pow(10, totalTxPower / 10)));
    }

    for (auto it = enbNetDev.Begin(); it != enbNetDev.End(); ++it)
    {
        DynamicCast<NrGnbNetDevice>(*it)->UpdateConfig();
    }
    for (auto it = ueLowLatNetDev.Begin(); it != ueLowLatNetDev.End(); ++it)
    {
        DynamicCast<NrUeNetDevice>(*it)->UpdateConfig();
    }
    for (auto it = ueVoiceNetDev.Begin(); it != ueVoiceNetDev.End(); ++it)
    {
        DynamicCast<NrUeNetDevice>(*it)->UpdateConfig();
    }

    Ptr<Node> pgw = epcHelper->GetPgwNode();
    NodeContainer remoteHostContainer;
    remoteHostContainer.Create(1);
    Ptr<Node> remoteHost = remoteHostContainer.Get(0);
    InternetStackHelper internet;
    internet.Install(remoteHostContainer);

    PointToPointHelper p2ph;
    p2ph.SetDeviceAttribute("DataRate", DataRateValue(DataRate("100Gb/s")));
    p2ph.SetDeviceAttribute("Mtu", UintegerValue(2500));
    p2ph.SetChannelAttribute("Delay", TimeValue(Seconds(0.000)));

    NetDeviceContainer internetDevices = p2ph.Install(pgw, remoteHost);
    Ipv4AddressHelper ipv4h;
    Ipv4StaticRoutingHelper ipv4RoutingHelper;
    ipv4h.SetBase("1.0.0.0", "255.0.0.0");
    Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign(internetDevices);
    Ptr<Ipv4StaticRouting> remoteHostStaticRouting = ipv4RoutingHelper.GetStaticRouting(remoteHost->GetObject<Ipv4>());
    remoteHostStaticRouting->AddNetworkRouteTo(Ipv4Address("7.0.0.0"), Ipv4Mask("255.0.0.0"), 1);

    internet.Install(gridScenario.GetUserTerminals());
    Ipv4InterfaceContainer ueLowLatIpIface = epcHelper->AssignUeIpv4Address(NetDeviceContainer(ueLowLatNetDev));
    Ipv4InterfaceContainer ueVoiceIpIface = epcHelper->AssignUeIpv4Address(NetDeviceContainer(ueVoiceNetDev));

    for (uint32_t j = 0; j < gridScenario.GetUserTerminals().GetN(); ++j)
    {
        Ptr<Ipv4StaticRouting> ueStaticRouting = ipv4RoutingHelper.GetStaticRouting(gridScenario.GetUserTerminals().Get(j)->GetObject<Ipv4>());
        ueStaticRouting->SetDefaultRoute(epcHelper->GetUeDefaultGatewayAddress(), 1);
    }

    nrHelper->AttachToClosestEnb(ueLowLatNetDev, enbNetDev);
    nrHelper->AttachToClosestEnb(ueVoiceNetDev, enbNetDev);

    uint16_t dlPortLowLat = 1234;
    uint16_t dlPortVoice = 1235;

    UdpServerHelper dlPacketSinkLowLat(dlPortLowLat);
    UdpServerHelper dlPacketSinkVoice(dlPortVoice);
    ApplicationContainer serverApps;
    serverApps.Add(dlPacketSinkLowLat.Install(ueLowLatContainer));
    serverApps.Add(dlPacketSinkVoice.Install(ueVoiceContainer));

    UdpClientHelper dlClientLowLat;
    dlClientLowLat.SetAttribute("RemotePort", UintegerValue(dlPortLowLat));
    dlClientLowLat.SetAttribute("MaxPackets", UintegerValue(0xFFFFFFFF));
    dlClientLowLat.SetAttribute("PacketSize", UintegerValue(udpPacketSizeULL));
    dlClientLowLat.SetAttribute("Interval", TimeValue(Seconds(1.0 / lambdaULL)));

    UdpClientHelper dlClientVoice;
    dlClientVoice.SetAttribute("RemotePort", UintegerValue(dlPortVoice));
    dlClientVoice.SetAttribute("MaxPackets", UintegerValue(0xFFFFFFFF));
    dlClientVoice.SetAttribute("PacketSize", UintegerValue(udpPacketSizeBe));
    dlClientVoice.SetAttribute("Interval", TimeValue(Seconds(1.0 / lambdaBe)));

    ApplicationContainer clientApps;
    for (uint32_t i = 0; i < ueLowLatContainer.GetN(); ++i)
    {
        Ptr<Node> ue = ueLowLatContainer.Get(i);
        Ptr<NetDevice> ueDevice = ueLowLatNetDev.Get(i);
        Address ueAddress = ueLowLatIpIface.GetAddress(i);
        dlClientLowLat.SetAttribute("RemoteAddress", AddressValue(ueAddress));
        clientApps.Add(dlClientLowLat.Install(remoteHost));
    }

    for (uint32_t i = 0; i < ueVoiceContainer.GetN(); ++i)
    {
        Ptr<Node> ue = ueVoiceContainer.Get(i);
        Ptr<NetDevice> ueDevice = ueVoiceNetDev.Get(i);
        Address ueAddress = ueVoiceIpIface.GetAddress(i);
        dlClientVoice.SetAttribute("RemoteAddress", AddressValue(ueAddress));
        clientApps.Add(dlClientVoice.Install(remoteHost));
    }

    serverApps.Start(udpAppStartTime);
    clientApps.Start(udpAppStartTime);
    serverApps.Stop(simTime);
    clientApps.Stop(simTime);

    FlowMonitorHelper flowmonHelper;
    Ptr<FlowMonitor> monitor = flowmonHelper.InstallAll();

    Simulator::Stop(simTime);
    Simulator::Run();

    // Definir 50% como smartphones e 50% como IoT
    for (uint32_t i = 0; i < totalUeNum; ++i) {
        if (i < totalUeNum / 2) {
            deviceTypeVector[i] = 1; // IoT
        } else {
            deviceTypeVector[i] = 0; // Smartphone
        }
    }


    // Cálculo do consumo de energia baseado na distância
    for (uint32_t i = 0; i < gridScenario.GetUserTerminals().GetN(); ++i) {
        Ptr<Node> ueNode = gridScenario.GetUserTerminals().Get(i);
        Ptr<MobilityModel> mob = ueNode->GetObject<MobilityModel>();
        Vector uePos = mob->GetPosition();

        // Calcular distância para a gNB mais próxima
        Ptr<Node> gNbNode = gridScenario.GetBaseStations().Get(0);  // Supondo que a gNB 0 é a mais próxima
        Ptr<MobilityModel> gNbMob = gNbNode->GetObject<MobilityModel>();
        Vector gNbPos = gNbMob->GetPosition();

        double distance = std::sqrt(std::pow(uePos.x - gNbPos.x, 2) + std::pow(uePos.y - gNbPos.y, 2) + std::pow(uePos.z - gNbPos.z, 2));
        distanceVector[i] = distance;

        // Calcular consumo de energia baseado na distância (exemplo: proporcional ao quadrado da distância)
        double distanceFactor = (distance > 0) ? distance : 1.0; // Evita divisão por zero
        double powerConsumption = processingPowerPerUE * std::pow(distanceFactor, 2); // Exemplo de consumo quadrático

        // Armazenar o consumo de energia no vetor
        energyConsumption[i] = powerConsumption * simTime.GetSeconds();

        if (distance > distanceLimit) {
            std::cerr << "O UE " << ueNode->GetId() << " está a " << distance << " metros, fora do limite de " << distanceLimit << " metros.\n";
        }
    }

    monitor->CheckForLostPackets();
    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmonHelper.GetClassifier());
    FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats();

    double flowDuration = (simTime - udpAppStartTime).GetSeconds();
    double averageFlowThroughput = 0.0;
    double averageFlowDelay = 0.0;

    double previousDelay = 0.0; // Inicializa o atraso anterior
    for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i)
    {
        // Obter o índice de UE correspondente ao FlowId
        uint32_t ueIndex = (i->first - 1) % totalUeNum;  // Calcula o índice do UE a partir do FlowId

        double throughput = i->second.rxBytes * 8.0 / flowDuration / 1000 / 1000; // Mbps
        double delay = i->second.rxPackets > 0 ? i->second.delaySum.GetSeconds() / i->second.rxPackets : 0.0;
        uint32_t lostPackets = i->second.txPackets - i->second.rxPackets;

        // Calcula o jitter como a diferença absoluta entre o delay atual e o anterior
        double jitter = std::abs(delay - previousDelay);
        previousDelay = delay; // Atualiza o atraso anterior para o próximo cálculo

        // Armazenar os valores nos vetores baseados no índice do UE
        lostPacketsVector[ueIndex] = lostPackets;
        throughputVector[ueIndex] = throughput;
        delayVector[ueIndex] = delay;
        //distanceVector[ueIndex] = delay;
        //energyConsumption[ueIndex] = energyConsumption;
        jitterVector[ueIndex] = jitter; // Armazena o jitter calculado


        // Calcular valores médios
        averageFlowThroughput += throughput;
        if (i->second.rxPackets > 0)
        {
            averageFlowDelay += delay;
        }
    }

    // Calcular valores médios
    averageFlowThroughput /= stats.size();
    averageFlowDelay /= stats.size();

    // Verificar se os vetores têm o tamanho correto
    if (throughputVector.size() != delayVector.size() ||
        throughputVector.size() != energyConsumption.size() ||
        throughputVector.size() != distanceVector.size() ||
        throughputVector.size() != deviceTypeVector.size() ||
        throughputVector.size() != lostPacketsVector.size()) {
        std::cerr << "Erro: Todos os vetores devem ter o mesmo tamanho." << std::endl;
        return 1;
    }

    // ALOCACAO DE MEMORIA COMPARTILHADA
    const char* shm_name = "ns3_shared_memory";
    size_t element_size = sizeof(double); // Tamanho de um elemento (double)
    size_t num_vectors = 6; // Agora temos 5 vetores: delay, throughput, consumo de energia, perda de pacotes e distância
    size_t size = totalUeNum * element_size * num_vectors; // Calcular o tamanho correto da memória

    int shm_fd = shm_open(shm_name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        std::cerr << "Erro ao criar memória compartilhada." << std::endl;
        return 1;
    }

    // Ajusta o tamanho da memória
    if (ftruncate(shm_fd, size) == -1) {
        std::cerr << "Erro ao ajustar o tamanho da memória compartilhada." << std::endl;
        close(shm_fd);
        return 1;
    }

    // Mapear a memória compartilhada
    double* data = (double*)mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (data == MAP_FAILED) {
        std::cerr << "Erro ao mapear a memória compartilhada." << std::endl;
        close(shm_fd);
        return 1;
    }

    // Escrever os dados na memória compartilhada
    for (size_t i = 0; i < totalUeNum; ++i) {
        data[i * 7] = delayVector[i];
        data[i * 7 + 1] = throughputVector[i];
        data[i * 7 + 2] = energyConsumption[i];
        data[i * 7 + 3] = lostPacketsVector[i];
        data[i * 7 + 4] = distanceVector[i];
        data[i * 7 + 5] = deviceTypeVector[i];
        data[i * 7 + 6] = jitterVector[i]; // Adiciona o jitter na memória compartilhada
    }

    std::cout << "Dados escritos na memória compartilhada." << std::endl;

    //  LIBERA A MEMORIA COMPARTILHADA após o uso
    if (munmap(data, size) == -1) {
        std::cerr << "Erro ao liberar a memória compartilhada." << std::endl;
    }

    // Imprimir os vetores
    std::cout << "Delay Vector (s): ";
    for (const auto& delay : delayVector)
    {
        std::cout << delay << " ";
    }
    std::cout << std::endl;

    std::cout << "Throughput Vector (Mbps): ";
    for (const auto& throughput : throughputVector)
    {
        std::cout << throughput << " ";
    }
    std::cout << std::endl;

    
    std::cout << "Lost Packets Vector: ";
    for (const auto& lostPackets : lostPacketsVector)
    {
        std::cout << lostPackets << " ";
    }
    std::cout << std::endl;

    std::cout << "Jitter: ";
    for (const auto& jitter : jitterVector)
    {
        std::cout << jitter << " ";
    }
    std::cout << std::endl;


    std::cout << "Energy Consumption: ";
    for (const auto& energyConsum : energyConsumption)
    {
        std::cout << energyConsum << " ";
    }
    std::cout << std::endl;

    std::cout << "Device Distance: ";
    for (const auto& distancevector : distanceVector)
    {
        std::cout << distancevector << " ";
    }
    std::cout << std::endl;

    std::cout << "Model Device 0-martphone 1-IoT: ";
    for (const auto& deviceTypeVector : deviceTypeVector)
    {
        std::cout << deviceTypeVector << " ";
    }
    std::cout << std::endl;

    // Imprimir resultados médios
    std::cout << "Average Delay: " << averageFlowDelay << " s\n";
    std::cout << "Average Throughput: " << averageFlowThroughput << " Mbps\n";

    //Exporta CSV com dados do Delay
    std::ofstream outputFileDelay("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/delay.csv");
    writeHeader(outputFileDelay, "User,Delay\n");
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileDelay << i+1 << ","
                   << delayVector[i] << "\n";
    }
    outputFileDelay.close(); 

    //Exporta CSV com dados do Throughput
    std::ofstream outputFileThroughput("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/throughput.csv");
    writeHeader(outputFileThroughput , "User,Throughput\n");
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileThroughput << i+1 << ","
                   << throughputVector[i] << "\n";
    }
    outputFileThroughput.close();

    //Exporta CSV com dados do Energy Consumption
    std::ofstream outputFileEnergyConsumption("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/energyConsumption.csv");
    writeHeader(outputFileEnergyConsumption , "User,EnergyConsumption\n");
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileEnergyConsumption << i+1 << ","
                   << energyConsumption[i] << "\n";
    }
    outputFileEnergyConsumption.close();

    //Exporta CSV com dados do Lost Packets
    std::ofstream outputFileLostPacketsVector("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/lostPacketsVector.csv");
    writeHeader(outputFileLostPacketsVector , "User,LostPackets\n");
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileLostPacketsVector << i+1 << ","
                   << lostPacketsVector[i] << "\n";
    }
    outputFileLostPacketsVector.close();

    //Exporta CSV com dados do Distance
    std::ofstream outputFileLostDistance("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/distance.csv");
    writeHeader(outputFileLostDistance , "User,Distance\n");
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileLostDistance << i+1 << ","
                   << distanceVector[i] << "\n";
    }
    outputFileLostDistance.close();

    //Exporta CSV com dados do tipo de dispositivo (IoT oiu Smartphone)
    std::ofstream outputFileDeviceType("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/deviceType.csv");
    writeHeader(outputFileDeviceType , "User,DeviceType\n");
    for (size_t i = 0; i < totalUeNum; ++i) {
        outputFileDeviceType << i+1 << "," << (deviceTypeVector[i] == 0 ? "Smartphone" : "IoT") << "\n";
    }
    outputFileDeviceType.close();

    // Exporta CSV com dados do Jitter
    std::ofstream outputFileJitter("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/jitter.csv");
    writeHeader(outputFileJitter, "User,Jitter\n");
    for (size_t i = 0; i < jitterVector.size(); ++i) {
        outputFileJitter << i+1 << "," << jitterVector[i] << "\n";
    }
    outputFileJitter.close();

    //Exporta CSV com todos os dados dos conjunto de vetores
    std::ofstream outputFileAll("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/line_all.csv");
    writeHeader(outputFileAll, "User,Delay,Throughput,EnergyConsumption,LostPackets,Jitter\n");

    // Supondo que os vetores delayVector, throughputVector, etc. têm o mesmo tamanho.
    size_t numEntries = delayVector.size(); // ou throughputVector.size(), assumindo que todos têm o mesmo tamanho

    for (size_t i = 0; i < numEntries; ++i) {
        outputFileAll << i+1 << ","
                      << delayVector[i] << ","
                      << throughputVector[i] << ","
                      << energyConsumption[i] << ","
                      << lostPacketsVector[i] << ","
                      << jitterVector[i] << "\n";
    }
    outputFileAll.close();

    // Exportar as posições para um arquivo CSV - UE e gNB
    std::ofstream posFile("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/positions.csv");
    posFile << "NodeType,NodeId,X,Y,Z,DistanceFromBSS\n";

    // Exportar posições dos gNBs
    for (uint32_t i = 0; i < gridScenario.GetBaseStations().GetN(); ++i)
    {
        Ptr<Node> gNbNode = gridScenario.GetBaseStations().Get(i);
        Ptr<MobilityModel> mob = gNbNode->GetObject<MobilityModel>();
        Vector pos = mob->GetPosition();
        posFile << "gNB," << gNbNode->GetId() << "," << pos.x << "," << pos.y << "," << pos.z << ",0\n";  // gNB está a 0 metros de si mesma
    }

    // Exportar posições e distâncias dos UEs
    for (uint32_t i = 0; i < gridScenario.GetUserTerminals().GetN(); ++i)
    {
        Ptr<Node> ueNode = gridScenario.GetUserTerminals().Get(i);
        Ptr<MobilityModel> mob = ueNode->GetObject<MobilityModel>();
        Vector pos = mob->GetPosition();

        // Calcular a distância do UE à gNB
        Ptr<Node> gNbNode = gridScenario.GetBaseStations().Get(0);  // gNB mais próxima
        Ptr<MobilityModel> gNbMob = gNbNode->GetObject<MobilityModel>();
        Vector gNbPos = gNbMob->GetPosition();

        double distance = std::sqrt(std::pow(pos.x - gNbPos.x, 2) + std::pow(pos.y - gNbPos.y, 2) + std::pow(pos.z - gNbPos.z, 2));

        posFile << "UE," << ueNode->GetId() << "," << pos.x << "," << pos.y << "," << pos.z << "," << distance << "\n";
    }
    posFile.close();



    //FINALIZACAO da simulação (destruição de objetos criados dinamicamente)
    //Simulator::Run();
    Simulator::Destroy();

    // CHAMAR o script Python
    // Crie o comando concatenando a variável totalUeNum à string do comando
    std::string command = "python3 scratch/SplitLearning-B5G/servers/server_sync.py " + std::to_string(totalUeNum);

    // Use o comando no system()
    int result = system(command.c_str());
    
    if (result != 0) {
        std::cerr << "Erro ao executar o script Python." << std::endl;
    }

    return 0;
}
