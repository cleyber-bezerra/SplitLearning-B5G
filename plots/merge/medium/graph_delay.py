import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def process_file(file_path, color, label):
    df = pd.read_csv(file_path)

    # Calcular a média e erro padrão para rx_packets agrupados por cliente
    grouped = df.groupby('User')['Delay'].agg(['mean', 'std', 'count'])
    grouped['stderr'] = grouped['std'] / np.sqrt(grouped['count'])

    # Calcular intervalo de confiança (95% CI)
    confidence_level = 0.95
    z_score = stats.norm.ppf((1 + confidence_level) / 2)
    grouped['ci_low'] = grouped['mean'] - z_score * grouped['stderr']
    grouped['ci_high'] = grouped['mean'] + z_score * grouped['stderr']

    # Preparar os dados para o plot
    clients = grouped.index  # Usar valores reais da coluna User
    mean_rx_packets = grouped['mean'].to_numpy()
    ci_low = grouped['ci_low'].to_numpy()
    ci_high = grouped['ci_high'].to_numpy()

    # Plotar o gráfico
    plt.plot(clients, mean_rx_packets, marker='', linestyle='-', linewidth=1, color=color, label=label)
    plt.fill_between(clients, ci_low, ci_high, color=color, alpha=0.1, linewidth=0)

    # Adicionar anotações para cada ponto
    for i, client in enumerate(clients):
        plt.annotate(f'({client}, {mean_rx_packets[i]:.2f})',
                     (client, mean_rx_packets[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color=color)

# Caminhos para os arquivos
files = ['0/delay.csv', '13/delay.csv', '26/delay.csv']
colors = ['g', 'b', 'r']
labels = ['TxPower = 0 dBM', 'TxPower = 13 dBM', 'TxPower = 26 dBM']

# Configuração do plot
plt.figure(figsize=(10, 6))

# Processar cada arquivo
for file, color, label in zip(files, colors, labels):
    process_file(file, color, label)

# Configuração do gráfico
plt.title('Canal de média perda (3 dB)', fontsize=16)
plt.xlabel('Distância do gNB (mt)', fontsize=15)
plt.ylabel('Atraso (s)', fontsize=15)
plt.grid(True)
plt.legend(loc='center right', bbox_to_anchor=(1.31, 0.5), fontsize=11)  # Legenda no canto inferior direito
plt.xticks(fontsize=13, rotation=0)
plt.yticks(fontsize=13)
plt.ylim(0, None)  # Forçar eixo y a começar do zero
plt.tight_layout()

# Ajustar o layout para não cortar a legenda externa
plt.tight_layout()

# Salvar e exibir o gráfico
name_output_file = "delayM"
plt.savefig(name_output_file + ".png")