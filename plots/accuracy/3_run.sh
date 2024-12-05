#!/bin/bash

# Exibe o menu de opções
echo "Escolha o tipo de grafico:"
echo "1 - Somente legendas"
echo "2 - Acuracia com legendas e rotulos"
echo -n "Digite o número da opção desejada: "
read opcao

# Define o novo nome do arquivo com base na opção escolhida
case $opcao in
    1)
        python plot1.py
        ;;
    2)
        python accuracy.py
        ;;
    *)
        echo "Opção inválida."
        exit 1
        ;;
esac

exit
