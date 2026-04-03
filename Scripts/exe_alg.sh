#!/bin/bash

SHELL=/bin/sh
PATH=/sbin:/usr/sbin:/usr/bin:/bin

# Conjunto de variantes para o algoritmo cubic_d
ALG_VARIANTS=("bpf_cubic")
# ALG_VARIANTS=("bpf_cubic" "cubic")

# Loop pelos algoritmos variantes
for alg_d in "${ALG_VARIANTS[@]}"; do
    alg_dir="${alg_d}" 
    mkdir -p "$alg_dir"

    # Loop pelos valores de fila
    for queue in 100 75 50 25; do
        queue_dir="$alg_dir/QUEUE_${queue}"
        mkdir -p "$queue_dir"

        # Loop pelos valores de delay e perda
        for delay in 10 25 50; do
        # for delay in 10; do
            for loss in $(seq 0 50 200); do
			# for loss in $(seq 0 100 100); do
                echo "Executando: queue=${queue}, delay=${delay}, loss=${loss}, algoritmo=${alg_d}"

                # Executa o script Python com os dois algoritmos
				python3 topo_beta.py -a cubic "$alg_d" -d "$delay" -l "$loss" -q "$queue" -dl 0 -ll 0
                # python3 topo_cubic_beta.py \
                #     --alg1 cubic \
                #     --alg2 "$alg_d" \
                #     --delay "$delay" \
                #     --loss "$loss" \
                #     --queue "$queue"

                # Move os arquivos gerados para o diretório correspondente
                mv iperf3_*_h11-h21_*_queue-"$queue".txt "$queue_dir"/ 2>/dev/null
                mv iperf3_*_h12-h22_*_queue-"$queue".txt "$queue_dir"/ 2>/dev/null
            done
        done
		mv *.txt "$queue_dir"
    done
done
