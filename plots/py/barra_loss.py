import matplotlib.pyplot as plt
import pandas as pd

# Carregar o arquivo CSV
file_path = '../merge/lostPacketsVector.csv'
data = pd.read_csv(file_path)

# Converter as colunas de acurácia de validação para listas de floats
data['LostPackets'] = data['LostPackets'].apply(lambda x: float(x.strip('[]')) if isinstance(x, str) else x)


# Calcular a média de acurácia de validação por cliente
mean_accuracy_per_client = data.groupby('User')['LostPackets'].mean()

# Plotar o gráfico de barras com rótulos de valor em cada barra
plt.figure(figsize=(10, 6))
bars = plt.bar(mean_accuracy_per_client.index, mean_accuracy_per_client.values, color='yellow')

# Adicionar rótulos de valor em cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 4), va='bottom', fontsize=14)  # Usei '%.4f' para mostrar 4 casas decimais

plt.title('Média de Perda de Pacotes por Usuário', fontsize=16)
plt.xlabel('Usuários', fontsize=14)
plt.ylabel('Perda de Pacotes (%)', fontsize=14)
plt.xticks(rotation=45, fontsize=13)  # Valores de X
plt.yticks(fontsize=13)  # Valores de Y
plt.tight_layout()

# Adicionar a legenda na parte superior direita
plt.legend(['Perda de Pacotes (%)'], loc='upper left', fontsize=12)

# Salvar o gráfico como um arquivo PNG
plt.savefig('../graph/graph_barra_loss.png')

# Mostrar o gráfico
#plt.show()