import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def process_file(file_path, color, label):
    df = pd.read_csv(file_path)

    # Calcular a média e erro padrão para rx_packets agrupados por cliente
    grouped = df.groupby('User')['Jitter'].agg(['mean', 'std', 'count'])
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

    # Usar os valores reais de clients
    clients_complete = np.arange(1, len(clients) + 1)  # Ajustar para o tamanho correto

    # Verificar o comprimento dos arrays
    if len(clients_complete) != len(mean_rx_packets):
        print(f"Warning: Clients and mean_rx_packets lengths do not match for file {file_path}")
        print(f"clients_complete: {clients_complete}")
        print(f"mean_rx_packets: {mean_rx_packets}")

    # Plotar o gráfico
    plt.plot(clients_complete, mean_rx_packets, marker='', linestyle='-', linewidth=1, color=color, label=label)
    plt.fill_between(clients_complete, ci_low, ci_high, color=color, alpha=0.1, linewidth=0)

    # Adicionar anotações para cada ponto
    for i in range(len(clients_complete)):
        plt.annotate(f'({clients_complete[i]}, {mean_rx_packets[i]:.2f})',
                     (clients_complete[i], mean_rx_packets[i]),
                     textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color=color)

# Caminhos para os arquivos
files = ['low/jitter.csv', 'medium/jitter.csv', 'high/jitter.csv']
colors = ['g', 'b', 'r']
labels = ['Low', 'Moderate', 'High']

# Configuração do plot
plt.figure(figsize=(10, 6))

# Processar cada arquivo
for file, color, label in zip(files, colors, labels):
    process_file(file, color, label)

# Configuração do gráfico
plt.title('Average Delay for each User', fontsize=16)
plt.xlabel('Users', fontsize=15)
plt.ylabel('Delay', fontsize=15)
plt.grid(True)
plt.legend(loc='center right', bbox_to_anchor=(1.31,0.5), fontsize=11)  # Legenda no canto inferior direito
plt.xticks(np.arange(1, 7), rotation=0, fontsize=13)
plt.yticks(fontsize=13)
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.9f}'))
plt.ylim(0, None)  # Forçar eixo y a começar do zero
plt.tight_layout()

#Ajuste o layout para nao cortar a legenda externa
plt.tight_layout()

# Salvar e exibir o gráfico
name_output_file = "jitter"
plt.savefig(name_output_file + ".png")
#plt.show()
