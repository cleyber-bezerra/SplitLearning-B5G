import pandas as pd
import os

# Definir os caminhos das pastas onde estão os arquivos
pasta1 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/1'
pasta2 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/2'
pasta3 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/3'
pasta4 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/4'
pasta5 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/5'
pasta6 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/6'
pasta7 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/7'
pasta8 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/8'
pasta9 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/9'
pasta10 = '/home/cleyber/Documentos/ns-3-dev/scratch/SplitLearning-B5G/plots/merge/high/0/10'


# Definir os nomes dos arquivos
arquivo_nome = 'throughput.csv'

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


# Realizar o merge dos dois DataFrames (concatenação de dados)
df_merged = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], ignore_index=True)

# Salvar o arquivo mergeado
df_merged.to_csv('throughput1.csv', index=False)

print("Merge concluído e salvo.")

import pandas as pd

# Define the input and output file paths
input_file = "throughput1.csv"  # Replace with your input file name
output_file = "throughput.csv"  # Replace with your desired output file name

# Define the mapping for User column
mapping = {
    1: 151.17,
    2: 90.04,
    3: 51.55,
    4: 66.43,
    5: 154.13,
    6: 91.84
}

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Apply the mapping to the 'User' column
df['User'] = df['User'].map(mapping)

# Save the modified DataFrame back to a CSV file
df.to_csv(output_file, index=False)

print(f"File saved successfully to {output_file}")