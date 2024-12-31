import pandas as pd

def calcular_percentual_EnergyConsumption(input_csv, output_csv):
    # Ler o arquivo CSV de entrada
    data = pd.read_csv(input_csv)

    # Calcular o EnergyConsumption total
    total_EnergyConsumption = data['EnergyConsumption'].sum()

    # Adicionar uma nova coluna com o percentual de EnergyConsumption
    data['Percentage'] = (data['EnergyConsumption'] / total_EnergyConsumption) * 100

    # Arredondar o percentual para duas casas decimais
    data['Percentage'] = data['Percentage'].round(2)

    # Salvar o novo arquivo CSV com os resultados
    data.to_csv(output_csv, index=False)
    print(f"Arquivo salvo com sucesso em: {output_csv}")

# Exemplo de uso
input_file = 'energyConsumption1.csv'  # Substitua pelo caminho do arquivo de entrada
output_file = 'energyConsumption.csv'  # Substitua pelo caminho do arquivo de saída
calcular_percentual_EnergyConsumption(input_file, output_file)
