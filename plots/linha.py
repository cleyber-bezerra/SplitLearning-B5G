import matplotlib.pyplot as plt

# Dados simulados
time = [1, 2, 3, 4, 5, 6]  # Tempo ou rodadas
packet_loss = [1, 5, 10, 15, 20, 25]  # Perda de pacotes
accuracy = [95, 90, 85, 80, 75, 70]  # Acurácia

# Criar gráfico de linha
plt.plot(time, packet_loss, label="Perda de Pacotes (%)", marker='o')
plt.plot(time, accuracy, label="Acurácia (%)", marker='s')
plt.title("Alteração da Acurácia e Perdas de Pacotes")
plt.xlabel("Rodadas de Simulação")
plt.ylabel("Valores (%)")
plt.legend()
plt.grid(True)
plt.show()
