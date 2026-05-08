## Execução dos testes

### 1. Preparação do ambiente

Clonando o repositório:
```bash
git clone https://github.com/nerds-ufes/Flex-Cubic.git
cd Flex-Cubic/
```
Obs.: É necessária a permissão de root para reprodução total ou parcial.

Com a o Mininet e OpenVSwitch instalados e configurados, registre o 'bpf_cubic.o' (Flex-Cubic) via:

```bash
cd /bpf_cubic
sudo bpftool struct_ops register bpf_cubic.o
cd ..
```
Obs1.: Para mais detalhes, siga as instruções em [Install/README](../Install/README.md) .

### 2. Execução dos testes no Mininet:

Basta executar o script 'exe.sh' e aguardar!
```bash
cd Scripts
sudo chmod +x *.sh
sudo ./exe.sh
```
Obs2.: A conclusão do script exe.sh leva por volta de 4h, considerando que cada seção do iperf dura 200 segundos (50 segundos iniciais de teste de conexão + 150 segundos de transmissão de fato). O tempo de execução pode ser reduzido com a alteração das variáveis runtime (linha 166) e iperf_runtime (linha 180) do script [topo_beta.py](topo_beta.py) .

### 3. Avaliação de resultados - Gáficos e tabelas

Após o término, os gráficos de Throughput, Retransmissões, RTT e cwnd podem ser gerados no mesmo 
diretório 'Scripts/' via:

```bash
sudo ./exe_plot.sh
```
Obs3.: Os gráficos serão salvos nos sub-diretórios do tipo:
```
cubic_b03_s41_m02/bpf_cubic/output_plots/
cubic_b07_s41_m02/bpf_cubic/output_plots/
cubic_b09_s41_m02/bpf_cubic/output_plots/
```

### 4. Mapeamento figura → script

Cada figura do artigo corresponde a uma configuração do script `exe.sh` e um diretório de saída:

| Figura do artigo | β (Flex-Cubic) | Diretório gerado | Gráficos em |
|---|---|---|---|
| Fig. 3 (β ≈ 0.3) | 358/1024 ≈ 0.35 | `cubic_b03_s41_m02/` | `cubic_b03_s41_m02/bpf_cubic/output_plots/` |
| Fig. 4 (β ≈ 0.7) | 717/1024 ≈ 0.70 | `cubic_b07_s41_m02/` | `cubic_b07_s41_m02/bpf_cubic/output_plots/` |
| Fig. 5 (β ≈ 0.9) | valor configurado | `cubic_b09_s41_m02/` | `cubic_b09_s41_m02/bpf_cubic/output_plots/` |

Cada figura compara TCP Cubic vs. Flex-Cubic sob as seguintes condições experimentais:
- **OWD (delays):** 10, 25 e 50 ms (RTT mínimo: 20, 50 e 100 ms)
- **Perdas de pacotes:** 0%, 0.5%, 1%, 1.5% e 2% (injetadas via `tc netem`; parâmetro `seq 0 50 200` dividido por 100)
- **Tamanho de fila:** 25%, 50%, 75% e 100% do BDP
- **Repetições por cenário:** 150 segundos de transmissão iperf3 por execução

**Estrutura dos dados brutos gerados:**
```
cubic_bXX_s41_m02/
└── bpf_cubic/
    ├── QUEUE_100/
    │   ├── iperf3_cubic_h10-h20_<loss>_loss_<delay>ms.txt   # JSON iperf3 TCP Cubic
    │   └── iperf3_bpf_cubic_h11-h21_<loss>_loss_<delay>ms.txt  # JSON iperf3 Flex-Cubic
    ├── QUEUE_75/
    ├── QUEUE_50/
    ├── QUEUE_25/
    └── output_plots/   # Gráficos gerados por exe_plot.sh
```

Para alterar o número de repetições ou duração de cada teste, edite em [topo_beta.py](topo_beta.py):
- Linha 152: `runtime = 50` — duração do teste de capacidade inicial (segundos)
- Linha 166: `iperf_runtime = 150` — duração do teste de throughput principal (segundos)

### 5. Rápido teste de execução:
Com o ambiente preparado e o bpf_cubic.o carregado, basta executar como root o script [topo_beta.py](topo_beta.py) :

```bash
python3 topo_beta.py -a cubic bpf_cubic -d 10 -l 0.5 -q 100 -dl 0 -ll 0

```
Onde: 
###### `-a` indica algoritmos TCP a serem usados (Ex.: cubic, bbr, reno, bpf_cubic)
###### `-d` indica o delay inserico, em mseg, via tc netem no link (Ex.: 10)
###### `-l` indica a porcentagem de perda de pacotes
###### `-q`, a fração de fila na interface do switch 
###### `-dl` e `-ll`, emulam valores diferentes de delay e perdas entre os links dos pares.


