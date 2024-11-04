import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_graph_from_csv(file_path):
    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return

    try:
        # Carregar o arquivo CSV
        data = pd.read_csv(file_path)

        # Definir o eixo X (primeira coluna) e os valores Y (outras colunas)
        x = data['User'].values  # Converter para numpy array
        y_columns = ['Delay', 'Throughput', 'EnergyConsumption', 'LostPackets']

        # Criar o gráfico de linhas
        plt.figure(figsize=(10, 6))
        for column in y_columns:
            y_values = data[column].values  # Valores Y
            plt.plot(x, y_values, label=column, marker='o')  # Plotar a linha com marcadores
            
            # Adicionar o valor no ponto de interseção
            for i, value in enumerate(y_values):
                plt.text(x[i], value, f'{value:.2f}', fontsize=9, ha='right')

        # Adicionar rótulos e título
        plt.xlabel('Users')
        plt.ylabel('Values')
        plt.title('Network Simulation Metrics')
        plt.legend(['Delay (s)', 'Throughput (Mbps)', 'EnergyConsumption (J)', 'LostPackets (%)'], loc='center left', bbox_to_anchor=(1,0.5), fontsize=12)

        #Ajuste o layout para nao cortar a legenda externa
        plt.tight_layout()

        # Mostrar o gráfico
        plt.grid(True)
        plt.tight_layout()

        # Salvar o gráfico como um arquivo PNG
        plt.savefig('../graph/graph_line_all.png')

        #plt.show()

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo CSV: {e}")

# Exemplo de uso
if __name__ == "__main__":
    csv_file = "../merge/line_all.csv"  # Altere para o caminho correto do seu arquivo CSV
    plot_graph_from_csv(csv_file)
