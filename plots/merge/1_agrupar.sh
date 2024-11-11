#!/bin/bash

# Exibe o menu de opções
echo "Escolha uma opção para agrupar pastas:"
echo "1 - low"
echo "2 - medium"
echo "3 - high"
echo -n "Digite o número da opção desejada: "
read opcao

# Define o novo nome do arquivo com base na opção escolhida
case $opcao in
    1)
        cd low/
        rm -rf 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        cd ..
        mv 1/ low/
        mv 2/ low/
        mv 3/ low/
        mv 4/ low/
        mv 5/ low/
        mv 6/ low/
        mv 7/ low/
        mv 8/ low/
        mv 9/ low/
        mv 10/ low/
        mv 11/ low/
        mv 12/ low/
        mv 13/ low/
        mv 14/ low/
        mv 15/ low/
        ;;
    2)
        cd medium/
        rm -rf 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        cd ..
        mv 1/ medium/
        mv 2/ medium/
        mv 3/ medium/
        mv 4/ medium/
        mv 5/ medium/
        mv 6/ medium/
        mv 7/ medium/
        mv 8/ medium/
        mv 9/ medium/
        mv 10/ medium/
        mv 11/ medium/
        mv 12/ medium/
        mv 13/ medium/
        mv 14/ medium/
        mv 15/ medium/
        ;;
    3)

        cd high/
        rm -rf 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        cd ..
        mv 1/ high/
        mv 2/ high/
        mv 3/ high/
        mv 4/ high/
        mv 5/ high/
        mv 6/ high/
        mv 7/ high/
        mv 8/ high/
        mv 9/ high/
        mv 10/ high/
        mv 11/ high/
        mv 12/ high/
        mv 13/ high/
        mv 14/ high/
        mv 15/ high/
        ;;
    *)
        echo "Opção inválida."
        exit 1
        ;;
esac

