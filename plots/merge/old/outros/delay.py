import pandas as pd
import os

# Definir os caminhos das pastas onde estão os arquivos
pasta1 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/low'
pasta2 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/medium'
pasta3 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high'

# Definir os nomes dos arquivos
arquivo_nome = 'delay.csv'

# Caminho completo dos arquivos
arquivo1 = os.path.join(pasta1, arquivo_nome)
arquivo2 = os.path.join(pasta2, arquivo_nome)
arquivo3 = os.path.join(pasta3, arquivo_nome)

# Carregar os arquivos CSV
df1 = pd.read_csv(arquivo1)
df2 = pd.read_csv(arquivo2)
df3 = pd.read_csv(arquivo3)

# Realizar o merge dos dois DataFrames (concatenação de dados)
df_merged = pd.concat([df1, df2, df3], ignore_index=True)

# Salvar o arquivo mergeado
df_merged.to_csv('delay.csv', index=False)

print("Merge concluído e salvo.")
