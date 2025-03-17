import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def process_file(file_path, color, label):
    df = pd.read_csv(file_path)

    # Verifica se há a coluna "Network Type", senão assume que não há categorização
    if 'Network Type' in df.columns:
        grouped = df.groupby(['Network Type', 'User'])['Validation Accuracy'].agg(['mean', 'std', 'count']).reset_index()
    else:
        grouped = df.groupby('User')['Validation Accuracy'].agg(['mean', 'std', 'count']).reset_index()
        grouped['Network Type'] = ''  # Se não houver categorização, cria um tipo único

    grouped['stderr'] = grouped['std'] / np.sqrt(grouped['count'])

    # Calcular intervalo de confiança (99% CI)
    confidence_level = 0.95
    z_score = stats.norm.ppf((1 + confidence_level) / 2)
    grouped['ci_low'] = grouped['mean'] - z_score * grouped['stderr']
    grouped['ci_high'] = grouped['mean'] + z_score * grouped['stderr']

    return grouped, color, label

# Caminhos para os arquivos
files = ['cenario_1_13/acuracia.csv', 'cenario_2_26/acuracia.csv']
colors = ['g', 'y']
labels = ['Cenário 1 (13 dBM)', 'Cenário 2 (26 dBM)']

# Processar cada arquivo e armazenar dados
all_data = []
for file, color, label in zip(files, colors, labels):
    grouped, color, label = process_file(file, color, label)
    grouped['Scenario'] = label  # Adicionar rótulo de cenário
    grouped['Color'] = color
    all_data.append(grouped)

# Concatenar os DataFrames de diferentes cenários
df_combined = pd.concat(all_data)

# Pegar os tipos de rede únicos
network_types = df_combined['Network Type'].unique()
users = df_combined['User'].unique()

# Configurar posições das barras para cada tipo de rede
x = np.arange(len(users))
width = 0.4  # Largura das barras

# Criar figura
plt.figure(figsize=(12, 7))

for i, net in enumerate(network_types):
    subset = df_combined[df_combined['Network Type'] == net]
    scenario_labels = subset['Scenario'].unique()
    
    for j, scenario in enumerate(scenario_labels):
        scenario_data = subset[subset['Scenario'] == scenario]
        mean_values = scenario_data['mean']
        errors = scenario_data['stderr'] * stats.norm.ppf(0.995)

        pos = x + (i * width) + (j * width / len(scenario_labels))  # Ajustar posições das barras

        bars = plt.bar(pos, mean_values, yerr=errors, capsize=5, width=width, alpha=0.8,
                       label=f"{net} - {scenario}", color=scenario_data['Color'].iloc[0])

        # Adicionar valores dentro das barras
        for bar, value in zip(bars, mean_values):
            plt.text(bar.get_x() + bar.get_width() / 2, 
                     bar.get_height() - 5,  # Ajuste de altura (-3) para melhor visibilidade
                     f"{value:.1f}%", 
                     ha='center', va='top', fontsize=28, color='black', rotation=60) # fontweight='bold',

# Configurar eixos
plt.xlabel('Distância dos dispositivos até gNB (m)', fontsize=24)
plt.ylabel('Acurácia (%)', fontsize=24)
plt.xticks(x + width, users, fontsize=22)
plt.yticks(np.arange(0, 101, 10))
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(loc='upper right', fontsize=20, bbox_to_anchor=(1, 0.2))

# Adicionar título
#plt.title('Acurácia por cenário', fontsize=16)

# Salvar e mostrar o gráfico
plt.tight_layout()
name_output_file = "graficoAcuracia"
plt.savefig(name_output_file + ".png")
#plt.show()

