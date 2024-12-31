import pandas as pd

def calcular_percentual_Delay(input_csv, output_csv):
    # Ler o arquivo CSV de entrada
    data = pd.read_csv(input_csv)

    # Calcular o Delay total
    total_Delay = data['Delay'].sum()

    # Adicionar uma nova coluna com o percentual de Delay
    data['Percentage'] = (data['Delay'] / total_Delay) * 100

    # Arredondar o percentual para duas casas decimais
    data['Percentage'] = data['Percentage'].round(2)

    # Salvar o novo arquivo CSV com os resultados
    data.to_csv(output_csv, index=False)
    print(f"Arquivo salvo com sucesso em: {output_csv}")

# Exemplo de uso
input_file = 'delay1.csv'  # Substitua pelo caminho do arquivo de entrada
output_file = 'delay.csv'  # Substitua pelo caminho do arquivo de saída
calcular_percentual_Delay(input_file, output_file)
