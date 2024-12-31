import pandas as pd

def process_throughput(input_file, output_file):
    # Lê o arquivo CSV
    df = pd.read_csv(input_file)
    
    # Agrupa por 'User', somando os valores de 'Throughput'
    grouped_df = df.groupby('User', as_index=False)['Throughput'].sum()
    
    # Calcula o percentual sobre o total
    total_throughput = grouped_df['Throughput'].sum()
    grouped_df['Percentage'] = (grouped_df['Throughput'] / total_throughput * 100).round(2)
    
    # Salva o resultado em um novo arquivo CSV
    grouped_df.to_csv(output_file, index=False)
    print(f"Arquivo salvo com sucesso em: {output_file}")

# Caminhos dos arquivos de entrada e saída
input_file = 'lostPacketsVector1.csv'  # Substitua pelo caminho do seu arquivo de entrada
output_file = 'lostPacketsVector.csv'  # Arquivo de saída

# Executa a função
process_throughput(input_file, output_file)
