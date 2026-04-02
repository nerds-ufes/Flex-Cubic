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

![Setup de testes](Images/Diagram_CC_TCP_BW2.png)

**Fig 1** - *Setup: Setup created for flow testing with competition between 10 TCP flows.*


## Results
![Average throughput and Jain Fairness Index by TCP congestion control lossless algorithm, gOSNR ≥ 20 dB](Images/Thoughput_00_loss.png)

**Fig. 2** - *Average throughput and Jain Fairness Index by TCP congestion control lossless algorithm, gOSNR ≥ 20 dB*

![Retransmission and Throughput average per Queue Variation by TCP congestion control lossless algorithm, gOSNR ≥ 20 dB](Images/Retr_00_loss.png) 

**Fig. 3** - *Retransmission and Throughput average per Queue Variation by TCP congestion control lossless algorithm, gOSNR ≥ 20 dB*

![Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.2% losses - gOSNR ≈ 19.45 dB](Images/Thoughput_02_loss.png)

**Fig. 4** - *Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.2% losses - gOSNR ≈ 19.45 dB*

![Retransmission and Throughput average per Queue Variation by TCP congestion control algorithm with 0.2% losses - gOSNR ≈ 19.45 dB](Images/Retr_02_loss.png)

**Fig. 5** - *Retransmission and Throughput average per Queue Variation by TCP congestion control algorithm with 0.2% losses - gOSNR ≈ 19.45 dB*

![Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.5% losses - gOSNR ≈ 19.15 dBs](Images/Thoughput_05_loss.png)

**Fig. 6** - *Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.5% losses - gOSNR ≈ 19.15 dBs*

![Retransmission and Throughput average per Queue Variation by TCP congestion control algorithm with 0.5% losses - gOSNR ≈ 19.15 dB](Images/Retr_05_loss.png)

**Fig. 7** - *Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.8% losses - gOSNR ≈ 18.95 dB*

![Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.8% losses - gOSNR ≈ 18.95 dB](Images/Thoughput_08_loss.png)

**Fig. 8** - *Average throughput and Jain Fairness Index by TCP congestion control algorithm with 0.8% losses - gOSNR ≈ 18.95 dB*
