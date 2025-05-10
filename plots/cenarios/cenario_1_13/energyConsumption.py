import pandas as pd
import os

# Definir os caminhos das pastas onde estão os arquivos
pasta1 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/1'
pasta2 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/2'
pasta3 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/3'
pasta4 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/4'
pasta5 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/5'
pasta6 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/6'
pasta7 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/7'
pasta8 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/8'
pasta9 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/9'
pasta10 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/10'
pasta11 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/11'
pasta12 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/12'
pasta13 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/13'
pasta14 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/14'
pasta15 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/15'
pasta16 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/16'
pasta17 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/17'
pasta18 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/18'
pasta19 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/19'
pasta20 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/cenarios/cenario_1_13/20'

# Definir os nomes dos arquivos
arquivo_nome = 'energyConsumption.csv'

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
arquivo16 = os.path.join(pasta16, arquivo_nome)
arquivo17 = os.path.join(pasta17, arquivo_nome)
arquivo18 = os.path.join(pasta18, arquivo_nome)
arquivo19 = os.path.join(pasta19, arquivo_nome)
arquivo20 = os.path.join(pasta20, arquivo_nome)

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
df16 = pd.read_csv(arquivo16)
df17 = pd.read_csv(arquivo17)
df18 = pd.read_csv(arquivo18)
df19 = pd.read_csv(arquivo19)
df20 = pd.read_csv(arquivo20)

# Realizar o merge dos dois DataFrames (concatenação de dados)
df_merged = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17, df18, df19, df20], ignore_index=True)

# Salvar o arquivo mergeado
df_merged.to_csv('energyConsumption1.csv', index=False)

print("Merge concluído e salvo.")

import pandas as pd

# Define the input and output file paths
input_file = "energyConsumption1.csv"  # Replace with your input file name
output_file = "energyConsumption.csv"  # Replace with your desired output file name

# Define the mapping for User column
mapping = {
    1: 125.49,
    2: 100.67,
    3: 96.54,
    4: 87.12,
    5: 64.88,
    6: 116.10,
    7: 58.45,
    8: 20.92,
    9: 145.77,
    10: 146.08
}

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Apply the mapping to the 'User' column
df['User'] = df['User'].map(mapping)

# Save the modified DataFrame back to a CSV file
df.to_csv(output_file, index=False)

print(f"File saved successfully to {output_file}")