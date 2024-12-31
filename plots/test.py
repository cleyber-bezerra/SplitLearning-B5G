import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Dados simulados
# Eixos X e Y
packet_loss = [1, 5, 10, 15, 20, 25]  # Perda de pacotes (%)
accuracy = [95, 90, 85, 80, 75, 70]  # Acurácia (%)

# Matriz de intensidade simulada (substituir com dados reais)
# Linhas correspondem a accuracy, colunas correspondem a packet_loss
data = np.array([
    [0.9, 0.85, 0.8, 0.75, 0.7, 0.65],
    [0.88, 0.83, 0.78, 0.73, 0.68, 0.63],
    [0.86, 0.81, 0.76, 0.71, 0.66, 0.61],
    [0.84, 0.79, 0.74, 0.69, 0.64, 0.59],
    [0.82, 0.77, 0.72, 0.67, 0.62, 0.57],
    [0.8, 0.75, 0.7, 0.65, 0.6, 0.55]
])  # Cada valor é a intensidade correspondente à relação.

# Criar o heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data, annot=True, fmt=".2f", xticklabels=packet_loss, yticklabels=accuracy, cmap="coolwarm")
plt.title("Heatmap: Relação entre Perda de Pacotes e Acurácia")
plt.xlabel("Perda de Pacotes (%)")
plt.ylabel("Acurácia (%)")
plt.show()
