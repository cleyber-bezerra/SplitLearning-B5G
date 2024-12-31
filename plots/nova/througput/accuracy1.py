import pandas as pd

def calcular_percentual_Train_Accuracy(input_csv, output_csv):
    # Ler o arquivo CSV de entrada
    data = pd.read_csv(input_csv)

    # Calcular o Train Accuracy total
    total_Train_Accuracy = data['Train Accuracy'].sum()

    # Adicionar uma nova coluna com o percentual de Train Accuracy
    data['Percentage'] = (data['Train Accuracy'] / total_Train_Accuracy) * 100

    # Arredondar o percentual para duas casas decimais
    data['Percentage'] = data['Percentage'].round(2)

    # Salvar o novo arquivo CSV com os resultados
    data.to_csv(output_csv, index=False)
    print(f"Arquivo salvo com sucesso em: {output_csv}")

# Exemplo de uso
input_file = 'accuracy1.csv'  # Substitua pelo caminho do arquivo de entrada
output_file = 'accuracy.csv'  # Substitua pelo caminho do arquivo de saída
calcular_percentual_Train_Accuracy(input_file, output_file)
