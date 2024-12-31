import pandas as pd

def process_Train_Accuracy(input_file, output_file):
    # Lê o arquivo CSV
    df = pd.read_csv(input_file)
    
    # Agrupa por 'User', somando os valores de 'Train Accuracy'
    grouped_df = df.groupby('User', as_index=False)['Train Accuracy'].sum()
    
    # Calcula o percentual sobre o total
    total_Train_Accuracy = grouped_df['Train Accuracy'].sum()
    grouped_df['Percentage'] = (grouped_df['Train Accuracy'] / total_Train_Accuracy * 100).round(2)
    
    # Salva o resultado em um novo arquivo CSV
    grouped_df.to_csv(output_file, index=False)
    print(f"Arquivo salvo com sucesso em: {output_file}")

# Caminhos dos arquivos de entrada e saída
input_file = 'accuracy1.csv'  # Substitua pelo caminho do seu arquivo de entrada
output_file = 'accuracy.csv'  # Arquivo de saída

# Executa a função
process_Train_Accuracy(input_file, output_file)
