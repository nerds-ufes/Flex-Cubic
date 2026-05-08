## Execução dos testes

### 1. Preparação do ambiente

Clone do repositório:
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
Obs2.: A conclusão do script 'exe.sh' leva por volta de 3h e 20 min! 

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
