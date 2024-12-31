import matplotlib.pyplot as plt

# Dados simulados
packet_loss = [1, 5, 10, 15, 20, 25]  # Percentual de perda de pacotes
accuracy = [95, 90, 85, 80, 75, 70]  # Acurácia correspondente

# Criar gráfico de dispersão
plt.scatter(packet_loss, accuracy)
plt.title("Relação entre Perda de Pacotes e Acurácia")
plt.xlabel("Perda de Pacotes (%)")
plt.ylabel("Acurácia (%)")
plt.grid(True)
plt.show()
