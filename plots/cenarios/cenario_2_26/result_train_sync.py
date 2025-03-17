import pandas as pd

# Nome do arquivo de entrada
arquivo_entrada = "result_train_sync.csv"

# Nome do arquivo de saída
arquivo_saida = "acuracia.csv"  # Nome atualizado

# Carregar o CSV
df = pd.read_csv(arquivo_entrada)

# Dicionário de substituição para a coluna "User"
substituicoes = {
    'user 1': 125.49,
    'user 2': 100.67,
    'user 3': 96.54,
    'user 4': 87.12,
    'user 5': 64.88,
    'user 6': 116.10,
    'user 7': 58.45,
    'user 8': 20.92,
    'user 9': 145.77,
    'user 10': 146.08
}

# Substituir os valores na coluna "User"
df["User"] = df["User"].replace(substituicoes)

# Multiplicar os valores da coluna "Validation Accuracy" por 100 e formatar para 2 casas decimais
df["Validation Accuracy"] = (df["Validation Accuracy"] * 100).round(2)

# Salvar o arquivo modificado com o novo nome
df.to_csv(arquivo_saida, index=False)

print(f"Arquivo atualizado salvo como: {arquivo_saida}")
