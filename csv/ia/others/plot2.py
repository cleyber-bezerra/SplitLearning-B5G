import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def process_file(file_path, color, label):
    df = pd.read_csv(file_path)

    # Verificar se as colunas esperadas existem no arquivo CSV
    if 'User' not in df.columns or 'Validation Accuracy' not in df.columns:
        print(f"Erro: Colunas 'User' ou 'Validation Accuracy' não encontradas em {file_path}")
        return

    # Calcular a média e erro padrão para 'Validation Accuracy' agrupados por 'User'
    grouped = df.groupby('User')['Validation Accuracy'].agg(['mean', 'std', 'count'])
    grouped['stderr'] = grouped['std'] / np.sqrt(grouped['count'])

    # Calcular intervalo de confiança (95% CI)
    confidence_level = 0.95
    z_score = stats.norm.ppf((1 + confidence_level) / 2)
    grouped['ci_low'] = grouped['mean'] - z_score * grouped['stderr']
    grouped['ci_high'] = grouped['mean'] + z_score * grouped['stderr']

    # Preparar os dados para o plot
    users = grouped.index
    mean_rx_packets = grouped['mean'].to_numpy()  # Convertendo para NumPy array
    ci_low = grouped['ci_low'].to_numpy()         # Convertendo para NumPy array
    ci_high = grouped['ci_high'].to_numpy()       # Convertendo para NumPy array

    # Ajuste aqui para garantir que `users_complete` corresponde ao tamanho correto de usuários
    users_complete = np.arange(1, len(users) + 1)  # Sequência de números correspondente ao número de usuários

    # Verificar o comprimento dos arrays para evitar discrepâncias
    if len(users_complete) != len(mean_rx_packets):
        print(f"Warning: users and mean_rx_packets lengths do not match for file {file_path}")
        print(f"users_complete: {users_complete}")
        print(f"mean_rx_packets: {mean_rx_packets}")
        return  # Evitar plotar dados que não estão corretamente alinhados

    # Plotar o gráfico
    plt.plot(users_complete, mean_rx_packets, marker='', linestyle='-', linewidth=1, color=color, label=label)
    plt.fill_between(users_complete, ci_low, ci_high, color=color, alpha=0.1, linewidth=0)

# Caminhos para os arquivos
files = ['user_1.csv', 'user_2.csv', 'user_3.csv']
colors = ['g', 'b', 'r']
labels = ['User 1 Accuracy', 'User 2 Accuracy', 'User 3 Accuracy']

# Configuração do plot
plt.figure(figsize=(10, 6))

# Processar cada arquivo
for file, color, label in zip(files, colors, labels):
    process_file(file, color, label)

# Configuração do gráfico
plt.title('Average Accuracy for each User', fontsize=16)
plt.xlabel('Users', fontsize=15)
plt.ylabel('Accuracy', fontsize=15)
plt.grid(True)
plt.legend(loc='upper right', fontsize=13)
plt.xticks(np.arange(1, 4), rotation=0, fontsize=13)
plt.yticks(fontsize=13)
plt.ylim(0, None)  # Forçar eixo y a começar do zero
plt.tight_layout()

# Salvar e exibir o gráfico
name_output_file = "users_accuracy"
plt.savefig(name_output_file + ".png")
