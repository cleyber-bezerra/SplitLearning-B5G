import pandas as pd

# Nome do arquivo de entrada
arquivo_entrada = "result_train_sync.csv"

# Nome do arquivo de saída
arquivo_saida = "acuracia.csv"  # Nome atualizado

# Carregar o CSV
df = pd.read_csv(arquivo_entrada)

# Dicionário de substituição para a coluna "User"
substituicoes = {
    'user 1': 151.17,
    'user 2': 90.04,
    'user 3': 51.55,
    'user 4': 66.43,
    'user 5': 154.13,
    'user 6': 91.84
}

# Substituir os valores na coluna "User"
df["User"] = df["User"].replace(substituicoes)

# Multiplicar os valores da coluna "Validation Accuracy" por 100 e formatar para 2 casas decimais
df["Validation Accuracy"] = (df["Validation Accuracy"] * 100).round(2)

# Salvar o arquivo modificado com o novo nome
df.to_csv(arquivo_saida, index=False)

print(f"Arquivo atualizado salvo como: {arquivo_saida}")
