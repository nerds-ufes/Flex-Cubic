# Flex-Cubic: A Runtime-Adaptive Loss-Tolerant TCP Cubic

**Abstract**—Traditional TCP still lacks the ability to differentiate between losses primarily caused by congestion
from those caused by physical layer errors. This may severely impair performance, especially in data-intensive 
science applications over high-capacity and long-distance dynamically reconfigurable transparent optical networks. 
This work proposes and experimentally implements a variant of TCP Cubic designed for reconfigurable networks to 
turn transport layer tolerant to non-congestion losses and variable RTT exploiting available bandwidth more efficiently. 
This is done by designing a congestion window (cwnd) reduction mechanism that conditions loss reactions on evidence 
of congestion, given by RTT measurements. In addition, Flex-Cubic aims to supports dynamic parameter tuning and 
higherprecision timing, resulting in greater stability and improved bandwidth utilization. Thus, eBPF has been used 
as a platform for TCP congestion control algorithm (CCA) implementation, enabling new algorithms to be loaded into 
the kernel via JIT at runtime, without recompilation. Through struct ops and maps, eBPF allows per-flow instrumentation
and dynamically CCA adaptation.

**Index Terms** — *Congestion Control Algorithms, eBPF*

## Background and Related Work
A structural limitation remains in most CCAs in the differentiation between losses caused by congestion events, illustrated in Fig 1 (a), and those caused by corrupted bits at physical layer by noise and interference, which is depicted in Fig 2 (b). In long-distance optical fibers, free-space optical (FSO) links subject to atmospheric turbulence, and satellite communications links under noise and interference, a non-negligible fraction of packet losses stems from residual bit errors rate (BER), and not from buffer overload. 

![Discarding of packets due to: (a) buffer overload, (b) packet corruption, and (c) packet timeout.](Images/rnp-400-Packet_loss.png)

**Fig 1** - *Discarding of packets due to: (a) buffer overload, (b) packet corruption, and (c) packet timeout.*

As a result, losses caused by corrupted packets are interpreted as congestion signals, causing cwnd reductions, unwarranted rate oscillations, and systematic under-utilization of available bandwidth. In this work, we focus on networks composed of high Bandwidth-Delay Product (BDP) links, where this effect is particularly severe, as window recovery after a reduction may require tens or hundreds of RTTs, significantly degrading average throughput, while also highlighting the behavior of loss-based algorithms.

In addition, there are strong dependence of congestion control on RTT. Route reconfigurations in adaptable networks may impose different propagation delays to in-flight packets of a given flow, as illustrated in Fig 1 (c) triggering a loss event. Classic performance models show that TCP throughput is proportional to cwnd/RTT and inversely proportional to $RTT \cdot \sqrt{p}$, where \textit{p} denotes the packet loss probability. Thus, links with high RTT require proportionally larger windows to fully exploit the available capacity. However, in modern networks, particularly in optical networks and Low Earth Orbit (LEO) satellite networks, this assumption is no longer valid. In these systems, RTT becomes a dynamic variable, subject to frequent sudden changes; and modern CCAs must be equipped with tools for facing such challenges. 

## Topology: TCP Cubic association with eBPF
![Topology adopted and results of competition between two (partially overlapping) flows using standard TCP Cubic vs. Flex-Cubic with losses
and queue bottlenecks.](Images/eBPF-Link.png)

**Fig 2** - *Setup: Setup created for flow testing with competition between 10 TCP flows.*


## Results
![Throughput comparison between Cubic and Flex-Cubic (β = 0.3,C = 41)](Images/throughput_all_delays_b03_s41.jpeg)

**Fig. 3** - *Throughput comparison between Cubic and Flex-Cubic (β = 0.3,C = 41)*

![Throughput comparison between Cubic and Flex-Cubic (β = 0.7,C = 41)](Images/throughput_all_delays_b07_s41.jpeg) 

**Fig. 4** - *Throughput comparison between Cubic and Flex-Cubic (β = 0.7,C = 41)*

![Throughput comparison between Cubic and Flex-Cubic (β = 0.9,C = 41)](Images/throughput_all_delays_b09_s41.jpeg)
