## Execução dos testes

### 1. Preparação do ambiente

Com a o Mininet e OpenVSwitch instalados e configurados, registre o 'bpf_cubic.o' (Flex-Cubic) via:

'''
cd /bpf_cubic
sudo bpftool struct_ops register bpf_cubic.o
cd ..
'''
Obs1.: Para mais detalhes, siga as instruções em '/Install/README.md'

'''
cd Scripts
sudo chmod +x *.sh
sudo ./exe.sh
'''
Obs2.: A conclusão do script 'exe.sh' leva por volta de 3h e 20 min! 

> **Recomendado:** Linux ≥ 6.1 (idealmente 6.5+)
