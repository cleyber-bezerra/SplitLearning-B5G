import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def process_file(file_path, color, label):
    df = pd.read_csv(file_path)

    # Calcular a média e erro padrão para rx_packets agrupados por cliente
    grouped = df.groupby('User')['LostPackets'].agg(['mean', 'std', 'count'])
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

    # Adicionar anotações para cada ponto
    for i, client in enumerate(clients):
        plt.annotate(f'({mean_rx_packets[i]:.2f})',
                     (client, mean_rx_packets[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center', fontsize=18, color=color, rotation=45)
        
# Caminhos para os arquivos
files = ['cenario_1_13/lostPacketsVector.csv', 'cenario_2_26/lostPacketsVector.csv']
colors = ['g', 'b']
labels = ['Cenário 1 (13 dBM)', 'Cenário 2 (26 dBM)']

# Configuração do plot
plt.figure(figsize=(10, 6))

# Processar cada arquivo
for file, color, label in zip(files, colors, labels):
    process_file(file, color, label)

# Configuração do gráfico
#plt.title('Perda de Pacotes por cenário', fontsize=16)
plt.xlabel('Distância dos dispositivos até gNB (m))', fontsize=22)
plt.ylabel('Perda de Pacotes', fontsize=22)
plt.grid(True)
plt.legend(loc='center right', bbox_to_anchor=(1.0,0.1), fontsize=18)  # Legenda no canto inferior direito
plt.xticks(fontsize=16, rotation=0)
plt.yticks(fontsize=16)
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.9f}'))
plt.ylim(0, None)  # Forçar eixo y a começar do zero
plt.tight_layout()

#Ajuste o layout para nao cortar a legenda externa
plt.tight_layout()

# Salvar e exibir o gráfico
name_output_file = "graficoPerda"
plt.savefig(name_output_file + ".png")
#plt.show()
