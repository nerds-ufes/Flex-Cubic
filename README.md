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

**Index Terms** — *Congestion Control Algorithms, Physical Layer Impairments, Optical Networks.*

![Topology adopted and results of competition between two (partially overlapping) flows using standard TCP Cubic vs. Flex-Cubic with losses
and queue bottlenecks.](Images/eBPF-Link.png)

**Fig 1** - *Setup: Setup created for flow testing with competition between 10 TCP flows.*


## Results
![Throughput comparison between Cubic and Flex-Cubic (β = 0.3,C = 41)](Images/throughput_all_delays_b03_s41.jpeg)

**Fig. 2** - *Throughput comparison between Cubic and Flex-Cubic (β = 0.3,C = 41)*

![Throughput comparison between Cubic and Flex-Cubic (β = 0.7,C = 41)](Images/throughput_all_delays_b07_s41.jpeg) 

**Fig. 3** - *Throughput comparison between Cubic and Flex-Cubic (β = 0.7,C = 41)*

![Throughput comparison between Cubic and Flex-Cubic (β = 0.9,C = 41)](Images/throughput_all_delays_b09_s41.jpeg)

**Fig. 4** - * Throughput comparison between Cubic and Flex-Cubic (β = 0.9,C = 41)*

![Retransmission and Throughput average per Queue Variation by TCP congestion control algorithm with 0.2% losses - gOSNR ≈ 19.45 dB](Images/Retr_02_loss.png)

**Fig. 5** - *Retransmission and Throughput average per Queue Variation by TCP congestion control algorithm with 0.2% losses - gOSNR ≈ 19.45 dB*

![Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.5% losses - gOSNR ≈ 19.15 dBs](Images/Thoughput_05_loss.png)

**Fig. 6** - *Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.5% losses - gOSNR ≈ 19.15 dBs*

![Retransmission and Throughput average per Queue Variation by TCP congestion control algorithm with 0.5% losses - gOSNR ≈ 19.15 dB](Images/Retr_05_loss.png)

**Fig. 7** - *Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.8% losses - gOSNR ≈ 18.95 dB*

![Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.8% losses - gOSNR ≈ 18.95 dB](Images/Thoughput_08_loss.png)

**Fig. 8** - *Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.8% losses - gOSNR ≈ 18.95 dB*
