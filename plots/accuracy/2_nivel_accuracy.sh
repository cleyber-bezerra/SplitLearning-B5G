#!/bin/bash

# Exibe o menu de opções
echo "Escolha uma opção para renomear o arquivo result_train_sync.csv:"
echo "1 - low_accuracy"
echo "2 - medium_accuracy"
echo "3 - high_accuracy"
echo -n "Digite o número da opção desejada: "
read opcao

# Define o novo nome do arquivo com base na opção escolhida
case $opcao in
    1)
        novo_nome="low_accuracy1.csv"
        ;;
    2)
        novo_nome="medium_accuracy1.csv"
        ;;
    3)
        novo_nome="high_accuracy1.csv"
        ;;
    *)
        echo "Opção inválida."
        exit 1
        ;;
esac

#mv ../result_train_sync.csv ../accuracy/result_train_sync.csv

# Verifica se o arquivo original existe
if [ -f "result_train_sync.csv" ]; then
    # Renomeia e move o arquivo para a pasta accuracy
    mv "result_train_sync.csv" "$novo_nome"
    echo "Arquivo renomeado para $novo_nome e movido para a pasta accuracy."
else
    echo "Arquivo result_train_sync.csv não encontrado."
fi

#source run.sh
