import pandas as pd
import os

# Definir os caminhos das pastas onde estão os arquivos
pasta1 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/1'
pasta2 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/2'
pasta3 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/3'
pasta4 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/4'
pasta5 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/5'
pasta6 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/6'
pasta7 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/7'
pasta8 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/8'
pasta9 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/9'
pasta10 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/10'
pasta11 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/11'
pasta12 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/12'
pasta13 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/13'
pasta14 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/14'
pasta15 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/15'

# Definir os nomes dos arquivos
arquivo_nome = 'positions.csv'

# Caminho completo dos arquivos
arquivo1 = os.path.join(pasta1, arquivo_nome)
arquivo2 = os.path.join(pasta2, arquivo_nome)
arquivo3 = os.path.join(pasta3, arquivo_nome)
arquivo4 = os.path.join(pasta4, arquivo_nome)
arquivo5 = os.path.join(pasta5, arquivo_nome)
arquivo6 = os.path.join(pasta6, arquivo_nome)
arquivo7 = os.path.join(pasta7, arquivo_nome)
arquivo8 = os.path.join(pasta8, arquivo_nome)
arquivo9 = os.path.join(pasta9, arquivo_nome)
arquivo10 = os.path.join(pasta10, arquivo_nome)
arquivo11 = os.path.join(pasta11, arquivo_nome)
arquivo12 = os.path.join(pasta12, arquivo_nome)
arquivo13 = os.path.join(pasta13, arquivo_nome)
arquivo14 = os.path.join(pasta14, arquivo_nome)
arquivo15 = os.path.join(pasta15, arquivo_nome)

# Carregar os arquivos CSV
df1 = pd.read_csv(arquivo1)
df2 = pd.read_csv(arquivo2)
df3 = pd.read_csv(arquivo3)
df4 = pd.read_csv(arquivo4)
df5 = pd.read_csv(arquivo5)
df6 = pd.read_csv(arquivo6)
df7 = pd.read_csv(arquivo7)
df8 = pd.read_csv(arquivo8)
df9 = pd.read_csv(arquivo9)
df10 = pd.read_csv(arquivo10)
df11 = pd.read_csv(arquivo11)
df12 = pd.read_csv(arquivo12)
df13 = pd.read_csv(arquivo13)
df14 = pd.read_csv(arquivo14)
df15 = pd.read_csv(arquivo15)

# Realizar o merge dos dois DataFrames (concatenação de dados)
df_merged = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10,df11, df12, df13, df14, df15], ignore_index=True)

# Salvar o arquivo mergeado
df_merged.to_csv('positions.csv', index=False)

print("Merge concluído e salvo.")
