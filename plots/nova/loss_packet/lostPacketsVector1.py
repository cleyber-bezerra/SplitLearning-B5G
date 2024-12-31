import pandas as pd

def calcular_percentual_throughput(input_csv, output_csv):
    # Ler o arquivo CSV de entrada
    data = pd.read_csv(input_csv)

    # Calcular o throughput total
    total_throughput = data['Throughput'].sum()

    # Adicionar uma nova coluna com o percentual de throughput
    data['Percentage'] = (data['Throughput'] / total_throughput) * 100

    # Arredondar o percentual para duas casas decimais
    data['Percentage'] = data['Percentage'].round(2)

    # Salvar o novo arquivo CSV com os resultados
    data.to_csv(output_csv, index=False)
    print(f"Arquivo salvo com sucesso em: {output_csv}")

# Exemplo de uso
input_file = 'lostPacketsVector1.csv'  # Substitua pelo caminho do arquivo de entrada
output_file = 'lostPacketsVector.csv'  # Substitua pelo caminho do arquivo de saída
calcular_percentual_throughput(input_file, output_file)
