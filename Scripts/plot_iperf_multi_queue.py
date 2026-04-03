#!/usr/bin/env python3
import os
import json
import re
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

import csv

# =============================
# CONFIGURAÇÃO
# =============================

QUEUE_DIRS = ["QUEUE_25", "QUEUE_50", "QUEUE_75", "QUEUE_100"]
ALGORITHMS = ["cubic", "bpf_cubic"]

OUTPUT_DIR = "output_plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TABLE_DIR = "output_tables"
os.makedirs(TABLE_DIR, exist_ok=True)


QUEUE_COLORS = {
    "QUEUE_25":  "#1f77b4",
    "QUEUE_50":  "#ff7f0e",
    "QUEUE_75":  "#2ca02c",
    "QUEUE_100": "#d62728",
}

# =============================
# EXPRESSÃO REGULAR DO ARQUIVO
# =============================

FILENAME_RE = re.compile(
    r"iperf_(?P<alg>bpf_cubic|cubic)_.*_\[(?P<loss>\d+)\]_loss_(?P<delay>\d+)ms\.txt"
)

# =============================
# FUNÇÕES ESTATÍSTICAS
# =============================

def mean_std(values):
    n = len(values)
    if n < 2:
        return (values[0] if n == 1 else 0.0), 0.0
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, math.sqrt(var)

# =============================
# PARSER IPERF3 JSON
# =============================

def parse_iperf_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    rates, rtts, cwnds, retrans = [], [], [], []
    prev_retrans = None

    for interval in data.get("intervals", []):
        s = interval.get("sum", {})

        if "bits_per_second" in s:
            rates.append(s["bits_per_second"] / 1e6)

        if "retransmits" in s:
            curr = s["retransmits"]
            if prev_retrans is not None:
                retrans.append(max(0, curr - prev_retrans))
            prev_retrans = curr

        for stream in interval.get("streams", []):
            if stream.get("sender", False):
                if "rtt" in stream:
                    rtts.append(stream["rtt"] / 1000.0)
                if "snd_cwnd" in stream:
                    cwnds.append(stream["snd_cwnd"] / 1024)

    return {
        "throughput": mean_std(rates),
        "rtt": mean_std(rtts),
        "retrans": mean_std(retrans),
        "cwnd": mean_std(cwnds),
    }

# =============================
# COLETA DOS DADOS
# data[(loss, delay)][alg][queue]
# =============================

data = defaultdict(lambda: defaultdict(dict))

for qdir in QUEUE_DIRS:
    if not os.path.isdir(qdir):
        continue

    for fname in os.listdir(qdir):
        m = FILENAME_RE.match(fname)
        if not m:
            continue

        alg = m.group("alg")
        loss = int(m.group("loss"))
        delay = int(m.group("delay"))

        path = os.path.join(qdir, fname)
        data[(loss, delay)][alg][qdir] = parse_iperf_json(path)

losses = sorted({k[0] for k in data.keys()})
delays = sorted({k[1] for k in data.keys()})

# =============================
# FUNÇÃO DE PLOT
# =============================

# import csv

def plot_metric(metric, ylabel):

    losses = sorted({k[0] for k in data.keys()})
    delays = sorted({k[1] for k in data.keys()})

    losses_real = [l / 100.0 for l in losses]
    x = np.arange(len(losses_real))

    fig, axes = plt.subplots(
        nrows=len(delays),
        ncols=1,
        figsize=(14, 4 * len(delays)),
        sharex=True,
        sharey=True
    )

    if len(delays) == 1:
        axes = [axes]

    n_groups = len(QUEUE_DIRS) * len(ALGORITHMS)
    width = 0.8 / n_groups

    legend_used = set()

    # =============================
    # COLETOR DE TABELA
    # =============================
    table_rows = []

    for ax, delay in zip(axes, delays):

        bar_index = 0

        for qdir in QUEUE_DIRS:
            for alg in ALGORITHMS:

                means, stds = [], []

                for loss in losses:
                    stats = data.get((loss, delay), {}).get(alg, {}).get(qdir)
                    if stats:
                        m, s = stats[metric]
                    else:
                        m, s = 0.0, 0.0

                    means.append(m)
                    stds.append(s)

                    # ===== adiciona linha na tabela =====
                    table_rows.append({
                        "delay_ms": delay,
                        "loss_percent": loss / 100.0,
                        "queue": qdir,
                        "algorithm": alg,
                        "mean": m,
                        "std": s
                    })

                positions = x - 0.4 + bar_index * width

                if metric in ("throughput", "retrans"):
                    lower = [min(s, m) for m, s in zip(means, stds)]
                    yerr = [lower, stds]
                else:
                    yerr = stds

                alg_label = "FLEX-CUBIC" if alg.lower() == "bpf_cubic" else alg.upper()
                label = f"{alg_label} | {qdir}"

                show_label = label not in legend_used
                legend_used.add(label)

                ax.bar(
                    positions,
                    means,
                    width,
                    yerr=yerr,
                    capsize=4,
                    color=QUEUE_COLORS[qdir],
                    hatch="///" if alg == "cubic" else None,
                    edgecolor="black",
                    label=label if show_label else None
                )

                bar_index += 1

        # ax.set_title(f"Delay = {delay} ms")
        ax.text(
                0.02, 0.92,
                f"OWD = {delay} ms",
                transform=ax.transAxes,
                fontsize=15,              # fonte maior
                fontweight="bold",
                verticalalignment="top",
                horizontalalignment="left",
                bbox=dict(
                    facecolor="white",
                    edgecolor="none",
                    alpha=0.75
                )
            )

        ax.grid(axis="y", linestyle="--", alpha=0.6)

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels([f"{l:.2f} %" for l in losses_real])
    # axes[-1].set_xlabel("Loss [%]")
    axes[-1].set_xlabel("Loss [%]", fontsize=15, fontweight="bold")
    fig.supylabel(ylabel ,fontsize=15, fontweight="bold")

    for ax in axes:
        ax.tick_params(axis="both", which="major", labelsize=13)



    fig.supylabel(ylabel, fontsize=15, fontweight="bold")

    handles, labels = axes[0].get_legend_handles_labels()

    fig.legend(
        handles,
        labels,
        ncol=4,
        fontsize=13,        # ↑ fonte maior
        loc="upper right", #"upper center"
        frameon=True,
        handlelength=2.8,   # ↑ tamanho dos traços/retângulos
        handleheight=1.4,
        labelspacing=0.8,
        borderpad=0.8,
        markerscale=1.4     # ↑ tamanho dos marcadores na legenda

    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # =============================
    # SALVA FIGURA
    # =============================
    plt.savefig(
        os.path.join(OUTPUT_DIR, f"{metric}_all_delays.jpeg"),
        dpi=300,
        format="jpeg"
    )
    plt.close()

    # =============================
    # EXPORTA TABELA CSV
    # =============================
    csv_path = os.path.join(TABLE_DIR, f"{metric}_all_delays.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "delay_ms",
                "loss_percent",
                "queue",
                "algorithm",
                "mean",
                "std"
            ]
        )
        writer.writeheader()
        writer.writerows(table_rows)

    print(f"✔ Tabela exportada: {csv_path}")


# =============================
# GERAÇÃO DOS GRÁFICOS
# =============================

plot_metric("throughput", "Average Throughput [Mbps]")
plot_metric("rtt", "Average RTT [ms]")
plot_metric("retrans", "Average Retransmissions")
plot_metric("cwnd", "Average CWND [KB]")

print("✔ Gráficos gerados corretamente para todos os delays.")
