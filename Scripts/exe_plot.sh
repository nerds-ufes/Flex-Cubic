#!/bin/bash

cp plot_iperf_multi_queue.py cubic_b03_s41_m02/bpf_cubic/
cp plot_iperf_multi_queue.py cubic_b07_s41_m02/bpf_cubic/
cp plot_iperf_multi_queue.py cubic_b09_s41_m02/bpf_cubic/

cd cubic_b03_s41_m02/bpf_cubic/
python3 plot_iperf_multi_queue.py
rm plot_iperf_multi_queue.py
cd ../..

cd cubic_b07_s41_m02/bpf_cubic/
python3 plot_iperf_multi_queue.py
rm plot_iperf_multi_queue.py
cd ../..

cd cubic_b09_s41_m02/bpf_cubic/
python3 plot_iperf_multi_queue.py
rm plot_iperf_multi_queue.py
cd ../..
