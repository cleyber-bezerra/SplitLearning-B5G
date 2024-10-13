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
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <sys/mman.h>  // Para mmap, munmap
#include <sys/stat.h>  // Para shm_open, shm_unlink
#include <fcntl.h>     // Para O_CREAT, O_RDWR
#include <unistd.h>    // Para close
#include <cstdlib>     // Para system


using namespace ns3;
NS_LOG_COMPONENT_DEFINE("CttcNrDemo");

int main(int argc, char* argv[])
{

    // Definir a seed fixa para a simulação
    SeedManager::SetSeed(1); // Fixa a seed para garantir que os valores aleatórios sejam repetíveis
    SeedManager::SetRun(1);  // Define o número da "run" para criar diferentes execuções com a mesma seed, se necessário

    uint16_t gNbNum = 1;
    uint16_t ueNumPergNb = 3;
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
    double bandwidthBand1 = 50e6;
    uint16_t numerologyBwp2 = 2;
    double centralFrequencyBand2 = 28.2e9;
    double bandwidthBand2 = 50e6;
    double totalTxPower = 35;
    std::string simTag = "default";
    std::string outputDir = "./";
    uint32_t totalUeNum = ueNumPergNb * gNbNum; // Calculando o número total de UEs
    double distanceLimit = 150.0; // Limite de distanciamento em metros


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
    for (uint32_t i = 0; i < gridScenario.GetBaseStations().GetN(); ++i)
    {
        Ptr<Node> gNbNode = gridScenario.GetBaseStations().Get(i);
        Ptr<MobilityModel> mob = gNbNode->GetObject<MobilityModel>();
        mob->SetPosition(Vector(0.0 + i * 50, 0.0, 10.0));  // Posição fixada para gNBs
    }

    // Definir posições fixas para UEs
    mobility.Install(gridScenario.GetUserTerminals());
    for (uint32_t i = 0; i < gridScenario.GetUserTerminals().GetN(); ++i)
    {
        Ptr<Node> ueNode = gridScenario.GetUserTerminals().Get(i);
        Ptr<MobilityModel> mob = ueNode->GetObject<MobilityModel>();
        mob->SetPosition(Vector(10.0 + i * 10, 5.0, 1.5));  // Posição fixada para UEs

        // Calcular distância para a gNB mais próxima
        Ptr<Node> gNbNode = gridScenario.GetBaseStations().Get(0);  // Supondo que a gNB 0 é a mais próxima
        Ptr<MobilityModel> gNbMob = gNbNode->GetObject<MobilityModel>();
        Vector uePos = mob->GetPosition();
        Vector gNbPos = gNbMob->GetPosition();

        double distance = std::sqrt(std::pow(uePos.x - gNbPos.x, 2) + std::pow(uePos.y - gNbPos.y, 2) + std::pow(uePos.z - gNbPos.z, 2));

        // Verifica se a distância é maior que o limite e corrige se necessário
        if (distance > distanceLimit) {
            std::cerr << "O UE " << ueNode->GetId() << " está a " << distance << " metros, fora do limite de " << distanceLimit << " metros.\n";
            // Aqui, você pode ajustar a posição do UE para ficar dentro do limite
            // Neste exemplo, vamos apenas deixar uma mensagem de erro
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

    // ALOCACAO DE MEMORIA DOS VETORES
    std::vector<uint32_t> lostPacketsVector(totalUeNum);
    std::vector<double> throughputVector(totalUeNum, 0.0);
    std::vector<double> delayVector(totalUeNum, 0.0);
    std::vector<double> energyConsumption(totalUeNum, 0.0); // ou algum valor padrão
    std::vector<double> distanceVector(totalUeNum, 0.0);

    // Potência estimada para processamento por UE (em Watts)
    double processingPowerPerUE = 0.05; // Exemplo: 50 mW por UE


    // Definir posições fixas para UEs e calcular distâncias
    mobility.Install(gridScenario.GetUserTerminals());
    for (uint32_t i = 0; i < gridScenario.GetUserTerminals().GetN(); ++i) {
        Ptr<Node> ueNode = gridScenario.GetUserTerminals().Get(i);
        Ptr<MobilityModel> mob = ueNode->GetObject<MobilityModel>();
        mob->SetPosition(Vector(10.0 + i * 10, 5.0, 1.5));  

        Ptr<Node> gNbNode = gridScenario.GetBaseStations().Get(0);
        Ptr<MobilityModel> gNbMob = gNbNode->GetObject<MobilityModel>();
        Vector uePos = mob->GetPosition();
        Vector gNbPos = gNbMob->GetPosition();

        double distance = std::sqrt(std::pow(uePos.x - gNbPos.x, 2) + std::pow(uePos.y - gNbPos.y, 2) + std::pow(uePos.z - gNbPos.z, 2));
        distanceVector[i] = distance;

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

    // Adicionar cálculo de consumo de energia por processamento de pacotes
    for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i)
    {
        uint32_t ueIndex = (i->first - 1) % totalUeNum;

        double throughput = i->second.rxBytes * 8.0 / flowDuration / 1000 / 1000; // Mbps
        double delay = i->second.rxPackets > 0 ? i->second.delaySum.GetSeconds() / i->second.rxPackets : 0.0;
        uint32_t lostPackets = i->second.txPackets - i->second.rxPackets;

        // Calcular energia consumida pelo processamento
        double energyConsumed = processingPowerPerUE * flowDuration; 

        lostPacketsVector[ueIndex] = lostPackets;
        throughputVector[ueIndex] = throughput;
        delayVector[ueIndex] = delay;
        energyConsumption[ueIndex] = energyConsumed;

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
        throughputVector.size() != lostPacketsVector.size()) {
        std::cerr << "Erro: Todos os vetores devem ter o mesmo tamanho." << std::endl;
        return 1;
    }

    // ALOCACAO DE MEMORIA COMPARTILHADA
    const char* shm_name = "ns3_shared_memory";
    size_t element_size = sizeof(double); // Tamanho de um elemento (double)
    size_t num_vectors = 5; // Agora temos 5 vetores: delay, throughput, consumo de energia, perda de pacotes e distância
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
        data[i * 5] = delayVector[i];
        data[i * 5 + 1] = throughputVector[i];
        data[i * 5 + 2] = energyConsumption[i];
        data[i * 5 + 3] = lostPacketsVector[i];
        data[i * 5 + 4] = distanceVector[i]; // Adicionando a distância
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


    // Imprimir resultados médios
    std::cout << "Average Delay: " << averageFlowDelay << " s\n";
    std::cout << "Average Throughput: " << averageFlowThroughput << " Mbps\n";

    //Exporta CSV com dados do Delay
    std::ofstream outputFileDelay("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/images/delay.csv");
    outputFileDelay << "User,Delay\n";
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileDelay << i << ","
                   << delayVector[i] << "\n";
    }
    outputFileDelay.close(); 

    //Exporta CSV com dados do Throughput
    std::ofstream outputFileThroughput("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/images/throughput.csv");
    outputFileThroughput << "User,Throughput\n";
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileThroughput << i << ","
                   << throughputVector[i] << "\n";
    }
    outputFileThroughput.close();

    //Exporta CSV com dados do Energy Consumption
    std::ofstream outputFileEnergyConsumption("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/images/energyConsumption.csv");
    outputFileEnergyConsumption << "User,EnergyConsumption\n";
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileEnergyConsumption << i << ","
                   << energyConsumption[i] << "\n";
    }
    outputFileEnergyConsumption.close();

    //Exporta CSV com dados do Lost Packets
    std::ofstream outputFileLostPacketsVector("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/images/lostPacketsVector.csv");
    outputFileLostPacketsVector << "User,LostPackets\n";
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileLostPacketsVector << i << ","
                   << lostPacketsVector[i] << "\n";
    }
    outputFileLostPacketsVector.close();

    //Exporta CSV com dados do Distance
    std::ofstream outputFileLostDistance("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/images/distance.csv");
    outputFileLostDistance << "User,Distance\n";
    for (size_t i = 0; i < throughputVector.size(); ++i) {
        outputFileLostDistance << i << ","
                   << distanceVector[i] << "\n";
    }
    outputFileLostDistance.close();



    //Exporta CSV com todos os dados dos conjunto de vetores
    std::ofstream outputFileAll("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/images/line_all.csv");
    outputFileAll << "User,Delay,Throughput,EnergyConsumption,LostPackets\n";

    // Supondo que os vetores delayVector, throughputVector, etc. têm o mesmo tamanho.
    size_t numEntries = delayVector.size(); // ou throughputVector.size(), assumindo que todos têm o mesmo tamanho

    for (size_t i = 0; i < numEntries; ++i) {
        outputFileAll << i << ","
                      << delayVector[i] << ","
                      << throughputVector[i] << ","
                      << energyConsumption[i] << ","
                      << lostPacketsVector[i] << "\n";
    }
    outputFileAll.close();

    // Exportar as posições para um arquivo CSV - UE e gNB
    std::ofstream posFile("/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/images/positions.csv");
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
    // Crie o comando concatenando a variável ueNumPergNb à string do comando
    std::string command = "python3 scratch/SplitLearning-B5G/servers/server_sync.py " + std::to_string(ueNumPergNb);

    // Use o comando no system()
    int result = system(command.c_str());
    
    if (result != 0) {
        std::cerr << "Erro ao executar o script Python." << std::endl;
    }

    return 0;
}
