import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def process_file(file_path, color, label):
    df = pd.read_csv(file_path)

    # Calcular a média e erro padrão para rx_packets agrupados por cliente
    grouped = df.groupby('User')['Validation Accuracy'].agg(['mean', 'std', 'count'])
    grouped['stderr'] = grouped['std'] / np.sqrt(grouped['count'])

    # Calcular intervalo de confiança (95% CI)
    confidence_level = 0.95
    z_score = stats.norm.ppf((1 + confidence_level) / 2)
    grouped['ci_low'] = grouped['mean'] - z_score * grouped['stderr']
    grouped['ci_high'] = grouped['mean'] + z_score * grouped['stderr']

    # Preparar os dados para o plot
    clients = grouped.index
    mean_rx_packets = grouped['mean'].to_numpy()  # Convertendo para NumPy array
    ci_low = grouped['ci_low'].to_numpy()         # Convertendo para NumPy array
    ci_high = grouped['ci_high'].to_numpy()       # Convertendo para NumPy array


    # Plotar o gráfico
    plt.plot(clients, mean_rx_packets, marker='', linestyle='-', linewidth=1, color=color, label=label)
    plt.fill_between(clients, ci_low, ci_high, color=color, alpha=0.1, linewidth=0)


# Caminhos para os arquivos
files = ['low_accuracy.csv', 'medium_accuracy.csv', 'high_accuracy.csv']
colors = ['g', 'b', 'r']
labels = ['Baixa - 2 dB', 'Média - 3 dB', 'Alta - 4dB']

# Configuração do plot
plt.figure(figsize=(10, 6))

# Processar cada arquivo
for file, color, label in zip(files, colors, labels):
    process_file(file, color, label)

# Configuração do gráfico
plt.title('Médias de Acurácia - 26 dBm', fontsize=16)
plt.xlabel('Distância do gNB (mt)', fontsize=15)
plt.ylabel('Acurácia', fontsize=15)
plt.grid(True)
plt.legend(loc='center right', bbox_to_anchor=(1.41, 0.5), fontsize=11)  # Legenda no canto inferior direito
plt.xticks(fontsize=13, rotation=0)
plt.yticks(fontsize=13)
plt.ylim(0, None)  # Forçar eixo y a começar do zero
plt.tight_layout()

# Salvar e exibir o gráfico
name_output_file = "accuracy"
plt.savefig(name_output_file + ".png")
#plt.show()
