#!/bin/bash

# Caminho da pasta principal
dir="merge"

# Verificar se a pasta principal existe
if [ ! -d "$dir" ]; then
  echo "Criando pasta $dir"
  mkdir "$dir"
fi

# Lista de pastas a serem verificadas
subdirs=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")

# Verificar e criar as subpastas, se necessário
for subdir in "${subdirs[@]}"; do
  if [ ! -d "$dir/$subdir" ]; then
    echo "Criando pasta $dir/$subdir"
    mkdir "$dir/$subdir"
  else
    echo "A pasta $dir/$subdir já existe"
  fi

#TREINAMENTO
if [ ! -f "accuracy/1/result_train_sync.csv" ]; then
   mv result_train_sync.csv ./accuracy/1/ 
fi
if [ ! -f "accuracy/2/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/2/ 
fi
if [ ! -f "accuracy/3/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/3/ 
fi
if [ ! -f "accuracy/4/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/4/ 
fi
if [ ! -f "accuracy/5/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/5/ 
fi
if [ ! -f "accuracy/6/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/6/ 
fi
if [ ! -f "accuracy/7/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/7/ 
fi
if [ ! -f "accuracy/8/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/8/ 
fi
if [ ! -f "accuracy/9/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/9/ 
fi
if [ ! -f "accuracy/10/result_train_sync.csv" ]; then 
   mv result_train_sync.csv accuracy/10/ 
fi


#REDE
if [ ! -f "merge/1/delay.csv" ]; then 
   mv *.csv merge/1/ 
fi
if [ ! -f "merge/2/delay.csv" ]; then 
   mv *.csv merge/2/ 
fi
if [ ! -f "merge/3/delay.csv" ]; then 
   mv *.csv merge/3/ 
fi
if [ ! -f "merge/4/delay.csv" ]; then 
   mv *.csv merge/4/ 
fi
if [ ! -f "merge/5/delay.csv" ]; then 
   mv *.csv merge/5/ 
fi
if [ ! -f "merge/6/delay.csv" ]; then 
   mv *.csv merge/6/ 
fi
if [ ! -f "merge/7/delay.csv" ]; then 
   mv *.csv merge/7/ 
fi
if [ ! -f "merge/8/delay.csv" ]; then 
   mv *.csv merge/8/ 
fi
if [ ! -f "merge/9/delay.csv" ]; then 
   mv *.csv merge/9/ 
fi
if [ ! -f "merge/10/delay.csv" ]; then 
   mv *.csv merge/10/ 
fi

done

exit 0