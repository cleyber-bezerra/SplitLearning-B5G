import pandas as pd

# Carregar o arquivo CSV
file_path = 'delay.csv'
df = pd.read_csv(file_path)

# Multiplicar a coluna 'Delay' por 10^4 - Decasegundo
df['Delay'] = df['Delay'] * 10**4

# Salvar o resultado em um novo arquivo ou substituir o arquivo existente
df.to_csv('delay_modified.csv', index=False)

# Carregar o arquivo CSV
#file_path2 = 'throughput.csv'
#df2 = pd.read_csv(file_path2)

# Multiplicar a coluna 'Throughput' por 10^4 - Decasegundo
#df2['Throughput'] = df2['Throughput'] * 10**5

# Salvar o resultado em um novo arquivo ou substituir o arquivo existente
#df2.to_csv('throughput_modified.csv', index=False)