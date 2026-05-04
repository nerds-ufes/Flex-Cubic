# BPF CUBIC — TCP Congestion Control via eBPF `struct_ops`

Tutorial completo para compilar, carregar e configurar dinamicamente o algoritmo de controle de congestionamento TCP CUBIC implementado como um programa eBPF usando `struct_ops`.

---

## Sumário

1. [Pré-requisitos](#1-pré-requisitos)
2. [Compilação do código eBPF](#2-compilação-do-código-ebpf)
3. [Registro do congestion control](#3-registro-do-congestion-control-struct_ops)
4. [Ativando o algoritmo bpf_cubic](#4-ativando-o-algoritmo-bpf_cubic)
5. [Entendendo o map `cubic_cfg`](#5-entendendo-o-map-cubic_cfg)
6. [Localizando o map](#6-localizando-o-map-cubic_cfg)
7. [Listando o conteúdo do map](#7-listando-dump-o-conteúdo-do-map)
8. [Alterando parâmetros dinamicamente](#8-alterando-valores-do-map-cubic_cfg)
9. [Reset para valores padrão](#9-reset-para-valores-padrão)
10. [Removendo o congestion control](#10-removendo-o-congestion-control)
11. [Boas práticas e observações](#11-boas-práticas-e-observações)

---

## 1. Pré-requisitos

### Kernel

Você precisa de um kernel com suporte a:

- eBPF `struct_ops`
- TCP congestion control via BPF

> **Recomendado:** Linux ≥ 6.1 (idealmente 6.5+)

Verifique a versão do kernel:

```bash
uname -r
```
OBS: caso o sistemas já possua todos os requisitos, o objeto 'bpf_cubic.o' pode ser carregado diretamente via:
```bash
cd ../bpf_cubic/
sudo bpftool struct_ops register bpf_cubic.o
```
### Pacotes necessários

Python3
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip git
```

Bibliotecas python
```bash
time
datetime
os
sys
subprocess
argparse
threading
socket
matplotlib
numpy
```

Mininet
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip git
git clone https://github.com/mininet/mininet
cd mininet
git tag  # list available versions
git checkout -b mininet-2.3.1b4 2.3.1b4  # Or later
cd ..
./mininet/util/install.sh -nv
```

Iperf3
```bash
sudo apt update
udo apt install -y iperf3
```

Iproute2
```bash
sudo apt update
sudo apt install iproute2
```


```bash
sudo apt update
sudo apt install -y clang-14 llvm-14 libbpf-dev bpftool linux-headers-$(uname -r)
```

Verifique as instalações:

```bash
clang-14 --version
bpftool version
```

### Geração do `vmlinux.h`

O código depende de BTF. Gere o `vmlinux.h` com:

```bash
sudo bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
```

> Coloque `vmlinux.h` no mesmo diretório do `bpf_cubic.c`.

---

## 2. Compilação do código eBPF

Compile com os flags indicados no cabeçalho do código:

```bash
sudo clang-14 -target bpf -D__TARGET_ARCH_x86 -g -O2 -Wall -c bpf_cubic.c -o bpf_cubic.o
```

Se tudo estiver correto, nenhum erro será exibido (apenas warnings, se houver).

Verifique o ELF gerado:

```bash
llvm-objdump -h bpf_cubic.o
```

Você deve ver seções como `.struct_ops` e `.maps`.

---
OBS: Em caso de falhas na compilação 'bpf_cubic.c' e/ ou posterior registro do objeto 'bpf_cubic.o' com a ferramenta bpftool,
basta executar o script de configuração do sistema e instalação do mininet:

```bash
chmod +x setup_ebpf_env.sh
sudo ./setup_ebpf_env.sh
```
A execução do script pode demorar alguns minutos!

## 3. Registro do congestion control (`struct_ops`)

Registre o CCA no kernel:

```bash
sudo bpftool struct_ops register bpf_cubic.o
```

**Saída esperada:**

```
Registered tcp_congestion_ops cubic id <N>
```

Confirme o registro:

```bash
sudo bpftool struct_ops show
```

**Exemplo de saída:**

```
tcp_congestion_ops cubic id 101 name bpf_cubic
```

---

## 4. Ativando o algoritmo `bpf_cubic`

Defina o congestion control padrão do sistema:

```bash
sudo sysctl -w net.ipv4.tcp_congestion_control=bpf_cubic
```

Confirme:

```bash
sysctl net.ipv4.tcp_congestion_control
```

**Saída esperada:**

```
net.ipv4.tcp_congestion_control = bpf_cubic
```

> ⚠️ Apenas **novas conexões TCP** passarão a usar o `bpf_cubic`.

---

## 5. Entendendo o map `cubic_cfg`

O map é definido no código como:

```c
struct cubic_config {
    __u32 beta;
    __u32 bic_scale;
    __u32 mult_rtt;
};

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct cubic_config);
} cubic_cfg SEC(".maps");
```

### Características

| Propriedade   | Valor              |
|---------------|--------------------|
| Tipo          | `BPF_MAP_TYPE_ARRAY` |
| Entradas      | 1                  |
| Chave         | `key = 0` (fixa)   |

### Campos e função

| Campo       | Função                                          |
|-------------|--------------------------------------------------|
| `beta`      | Fator de redução do `cwnd` após perda            |
| `bic_scale` | Escala do crescimento cúbico                     |
| `mult_rtt`  | Multiplicador de RTT para reset em caso de perda |

### Valores padrão (quando o map retorna 0)

| Campo       | Default |
|-------------|---------|
| `beta`      | `717`   |
| `bic_scale` | `41`    |
| `mult_rtt`  | `2`     |

---

## 6. Localizando o map `cubic_cfg`

Liste todos os maps eBPF carregados:

```bash
sudo bpftool map show
```

**Exemplo de saída:**

```
123: array  name cubic_cfg  flags 0x0
    key 4B  value 12B  max_entries 1
```

> Anote o **ID do map** (ex: `123`) para os próximos comandos.

---

## 7. Listando (dump) o conteúdo do map

### Dump bruto

```bash
sudo bpftool map dump id 123
```

**Exemplo de saída:**

```
key: 00 00 00 00
value:
  cd 02 00 00   29 00 00 00   02 00 00 00
```

Interpretando em **little-endian**:

| Campo       | Valor |
|-------------|-------|
| `beta`      | `717` |
| `bic_scale` | `41`  |
| `mult_rtt`  | `2`   |

### Dump em formato JSON

```bash
sudo bpftool -j map dump id 123
```

---

## 8. Alterando valores do map `cubic_cfg`

Como é um `ARRAY`, a chave é **sempre `0`**.

### Sintaxe geral

```bash
sudo bpftool map update id <MAP_ID> \
  key hex 00 00 00 00 \
  value hex <12 bytes em little-endian>
```

---

### Exemplo 1 — CUBIC mais agressivo

| Campo       | Decimal | Hex (little-endian) |
|-------------|---------|----------------------|
| `beta`      | `800`   | `20 03 00 00`        |
| `bic_scale` | `50`    | `32 00 00 00`        |
| `mult_rtt`  | `2`     | `02 00 00 00`        |

```bash
sudo bpftool map update id 123 \
  key hex 00 00 00 00 \
  value hex 20 03 00 00 32 00 00 00 02 00 00 00
```

---

### Exemplo 2 — CUBIC mais conservador

| Campo       | Decimal | Hex (little-endian) |
|-------------|---------|----------------------|
| `beta`      | `650`   | `8a 02 00 00`        |
| `bic_scale` | `30`    | `1e 00 00 00`        |
| `mult_rtt`  | `2`     | `02 00 00 00`        |

```bash
sudo bpftool map update id 123 \
  key hex 00 00 00 00 \
  value hex 8a 02 00 00 1e 00 00 00 02 00 00 00
```

---

### Verificando após a alteração

```bash
sudo bpftool map dump id 123
```

> ✅ As mudanças entram em vigor **imediatamente**, sem necessidade de recarregar o programa eBPF.

---

## 9. Reset para valores padrão

Para restaurar o comportamento padrão, zere o map:

```bash
sudo bpftool map update id 123 \
  key hex 00 00 00 00 \
  value hex 00 00 00 00 00 00 00 00 00 00 00 00
```

O código automaticamente assumirá os valores definidos via `#define`.

---

## 10. Removendo o congestion control

Ao finalizar os testes, desregistre o CCA:

```bash
sudo bpftool struct_ops unregister name cubic
```

Confirme a remoção:

```bash
bpftool struct_ops show
```

---

## 11. Boas práticas e observações

### Validação com `iperf3`

```bash
iperf3 -c <destino> -t 30
```

### Inspeção de conexões TCP ativas

```bash
ss -ti
```

Métricas úteis para observar:

- `cwnd` — janela de congestionamento atual
- `rtt` — round-trip time
- `pacing_rate` — taxa de envio

### ⚠️ Cuidados com valores extremos

Valores muito altos ou baixos de `bic_scale` ou `beta` podem:

- Causar **unfairness** entre fluxos concorrentes
- Induzir **bursts excessivos** de tráfego
- Aumentar **perdas de pacotes** em redes com bufferbloat
