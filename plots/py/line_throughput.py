import matplotlib.pyplot as plt
import pandas as pd

# Carregar o arquivo CSV
file_path = '../merge/throughput.csv'
data = pd.read_csv(file_path)

# Converter as colunas de Throughput para listas de floats, se necessário
data['Throughput'] = data['Throughput'].apply(lambda x: float(x.strip('[]')) if isinstance(x, str) else x)

# Calcular a média de Throughput por usuário
mean_delay_per_user = data.groupby('User')['Throughput'].mean()

# Converter o índice para lista ou array NumPy para evitar o erro
user_labels = mean_delay_per_user.index.tolist()  # Ou use .to_numpy() para converter para NumPy

# Plotar o gráfico de linhas horizontal
plt.figure(figsize=(10, 6))
plt.plot(mean_delay_per_user.values, user_labels, marker='o', color='green')  # Plotando as linhas horizontalmente

# Adicionar rótulos de valor ao lado de cada ponto
for i, v in enumerate(mean_delay_per_user.values):
    plt.text(v, user_labels[i], f'{v:.4f}', va='center', fontsize=12)

plt.title('Média de Throughput por Usuário', fontsize=16)
plt.xlabel('Throughput (Mbps)', fontsize=14)
plt.ylabel('Usuários', fontsize=14)
plt.xticks(fontsize=13)  # Valores do eixo X
plt.yticks(fontsize=13)  # Valores do eixo Y
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Adicionar a legenda na parte superior direita
plt.legend(['Throughput (Mbps)'], loc='upper left', fontsize=12)

# Salvar o gráfico como um arquivo PNG
plt.savefig('../graph/graph_line_throughput.png')

# Mostrar o gráfico
#plt.show()
