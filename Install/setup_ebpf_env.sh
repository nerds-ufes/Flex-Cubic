#!/usr/bin/env bash

set -e

echo "=============================="
echo " eBPF + struct_ops + Mininet Setup"
echo "=============================="

# =========================
# 1. Verificar kernel
# =========================
echo "[*] Kernel em execução:"
uname -r

# =========================
# 2. Instalar dependências
# =========================
echo "[*] Instalando dependências base..."

sudo apt update

sudo apt install -y \
  build-essential \
  clang \
  llvm \
  gcc \
  make \
  git \
  pkg-config \
  cmake \
  flex \
  bison \
  libelf-dev \
  libbpf-dev \
  zlib1g-dev \
  dwarves \
  iproute2 \
  iputils-ping \
  net-tools \
  iperf3 \
  python3 \
  python3-matplotlib\
  python3-pip \
  linux-headers-$(uname -r)

# =========================
# 3. Verificar pahole
# =========================
echo "[*] Verificando pahole..."
pahole --version

# =========================
# 4. Verificar BTF
# =========================
echo "[*] Verificando BTF do kernel..."

if [ ! -f /sys/kernel/btf/vmlinux ]; then
    echo "[ERRO] Kernel sem BTF (/sys/kernel/btf/vmlinux não encontrado)"
    exit 1
fi

echo "[OK] BTF disponível"

# =========================
# 5. Preparar diretório
# =========================
WORKDIR=$HOME/ebpf-lab
mkdir -p $WORKDIR
cd $WORKDIR

# =========================
# 6. Baixar kernel upstream (v6.8)
# =========================
if [ ! -d "linux" ]; then
    echo "[*] Clonando kernel upstream..."
    git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
fi

cd linux
git fetch --all
git checkout v6.8

# =========================
# 7. Compilar bpftool
# =========================
echo "[*] Compilando bpftool..."

cd tools/bpf/bpftool
make -j$(nproc)

# =========================
# 8. Instalar bpftool no PATH
# =========================
echo "[*] Instalando bpftool..."

sudo cp bpftool /usr/local/bin/
sudo chmod +x /usr/local/bin/bpftool

# =========================
# 9. Validar bpftool
# =========================
echo "[*] Validando bpftool..."

which bpftool
bpftool version

# =========================
# 10. Gerar vmlinux.h
# =========================
cd $WORKDIR

echo "[*] Gerando vmlinux.h..."

bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

echo "[OK] vmlinux.h gerado em $WORKDIR"

# =========================
# 11. Instalar Mininet
# =========================
echo "[*] Instalando Mininet..."

cd $WORKDIR

if [ ! -d "mininet" ]; then
    git clone https://github.com/mininet/mininet
fi

cd mininet

echo "[*] Versões disponíveis:"
git tag | tail -n 10

echo "[*] Checkout Mininet 2.3.0..."
git checkout -B mininet-2.3.0 2.3.0

cd ..

echo "[*] Executando instalação do Mininet..."
sudo ./mininet/util/install.sh -nv

# =========================
# 12. Instalando e configurando o OpenVSwitch
# =========================

sudo apt install -y openvswitch-switch

sudo systemctl start openvswitch-switch
sudo systemctl enable openvswitch-switch

sudo ovs-vsctl show

# =========================
# 13. Teste do Mininet
# =========================
echo "[*] Testando Mininet..."

sudo mn --test pingall

# =========================
# 14. Final
# =========================
echo "=============================="
echo " Setup completo!"
echo "=============================="

echo ""
echo "Ambiente pronto para:"
echo "- eBPF (struct_ops)"
echo "- bpftool v6.8"
echo "- Mininet 2.3.0"
echo ""

echo "Próximos passos:"
echo "1) Copiar seu bpf_cubic.c para $WORKDIR"
echo "2) Compilar:"
echo "   clang -O2 -g -target bpf -D__TARGET_ARCH_x86 -I. -c bpf_cubic.c -o bpf_cubic.o"
echo ""
echo "3) Registrar:"
echo "   sudo bpftool struct_ops register bpf_cubic.o"
echo ""
