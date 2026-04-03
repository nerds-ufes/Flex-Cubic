#!/bin/bash
set -euo pipefail

# Script principal simplificado

# Caminho do script a ser executado
SCRIPT_ALVO="exe_alg.sh"

# Verifica se o arquivo existe
if [ ! -f "$SCRIPT_ALVO" ]; then
    echo "Erro: Arquivo '$SCRIPT_ALVO' não encontrado!"
    exit 1
fi

# Dá permissão de execução se necessário
if [ ! -x "$SCRIPT_ALVO" ]; then
    chmod +x "$SCRIPT_ALVO"
fi

############### TESTE beta = 717; bic_scale = 41; mult_rtt = 2 ##################
#Cria o diretório
mkdir -p cubic_b07_s41_m02
cp exe_alg.sh cubic_b07_s41_m02
cp topo_beta.py cubic_b07_s41_m02
cd cubic_b07_s41_m02

bpftool map update name cubic_cfg key hex 00 00 00 00 value hex cd 02 00 00 29 00 00 00 02 00 00 00

# Executa o script
echo "Executando $SCRIPT_ALVO..."
./$SCRIPT_ALVO
rm topo_beta.py
cd ..

################################ FIM TESTE #######################################

############### TESTE beta = 358; bic_scale = 41; mult_rtt = 2 ##################
#Cria o diretório
mkdir -p cubic_b03_s41_m02
cp exe_alg.sh cubic_b03_s41_m02
cp topo_beta.py cubic_b03_s41_m02
cd cubic_b03_s41_m02

bpftool map update name cubic_cfg key hex 00 00 00 00 value hex 66 01 00 00 29 00 00 00 02 00 00 00

# Executa o script
echo "Executando $SCRIPT_ALVO..."
./$SCRIPT_ALVO
rm topo_beta.py
cd ..

################################ FIM TESTE #######################################

############### TESTE beta = 922; bic_scale = 41; mult_rtt = 2 ##################
#Cria o diretório
mkdir -p cubic_b09_s41_m02
cp exe_alg.sh cubic_b09_s41_m02
cp topo_beta.py cubic_b09_s41_m02
cd cubic_b09_s41_m02

bpftool map update name cubic_cfg key hex 00 00 00 00 value hex 39 0a 00 00 29 00 00 00 02 00 00 00

# Executa o script
echo "Executando $SCRIPT_ALVO..."
./$SCRIPT_ALVO
rm topo_beta.py
cd ..

################################ FIM TESTE #######################################


# Verifica se a execução foi bem sucedida
if [ $? -eq 0 ]; then
    echo "Script executado com sucesso!"
else
    echo "O script retornou um erro!"
fi
