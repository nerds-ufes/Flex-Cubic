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
Obs1.: Para mais detalhes, siga as instruções em '/Install/README.md'

### 2. Execução dos testes no Mininet:

Basta executar o script 'exe.sh' e aguardar!
```bash
cd Scripts
sudo chmod +x *.sh
sudo ./exe.sh
```
Obs2.: A conclusão do script exe.sh leva por volta de 4h, considerando que cada seção do iperf dura 200 segundos (50 segundos iniciais de teste de conexão + 150 segundos de transmissão de fato). O tempo de execução pode ser reduzido com a alteração das variáveis runtime (linha 166) e iperf_runtime (linha 180) do script [topo_beta.py](Scripts/topo_beta.py).

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
