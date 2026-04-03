#!/usr/bin/env python3

"""
mult_link.py: simple link between terminals & switches
h1 ----- s3 ---s1 -- s2 --- s4 -- h2
h2 ---_/                     \_---- hn
Use ./config-multi_link.sh
This is very close to the simplest fully emulated packet
network that we can create.

"""
from time import sleep, mktime
import csv
from datetime import datetime
import matplotlib
matplotlib.use('Agg')   # Force matplotlib to not use any Xwindows backend.
import matplotlib.pyplot as plt


from mininet.node import OVSBridge, Host
from mininet.topo import Topo

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections, quietRun
from mininet.log import info, lg, setLogLevel
from mininet.log import setLogLevel, info
from mininet.clean import cleanup

from os.path import dirname, realpath, join
from subprocess import run
from sys import argv
import argparse
import os
import subprocess


import sys
import time
import threading
import socket
import numpy as np
from mininet.cli import CLI


iperf_csv_header = ['time', 'src_addr', 'src_port', 'dst_addr' ,'dst_port', 'other', 'interval', 'B_sent', 'bps']

#########################################################################
################ DELETA AS INFERFACES CRIADAS ###########################
#########################################################################
def limpa_int():
	os.system("sudo mn -c")
	interfaces = ["s1-eth1","s1-eth2","s2-eth1","s2-eth2","s3-eth1","s4-eth1"]
	for interface in interfaces:
		subprocess.run(["sudo","ip","link","delete", interface])



#################################################################
#################### DEFINIÇÃO DA REDE  ######################### 
#################################################################

class SimpleLinkTopo(Topo):

    def build(self, delay=2, loss = 0, queue = 100):


        br_params = dict(bw=100, delay='{0}ms'.format(delay[0]), max_queue_size=8.33*(queue/100)*10, use_htb=True)  
        ar_params = dict(bw=100, delay='0ms', max_queue_size=(21*v_delay[0]*20)/100, use_htb=True)  # access router intf tc params

        
        # TODO: remove queue size from hosts and try.
        hi_params = dict(bw=100, delay='0ms', max_queue_size=100*v_delay[0], loss = 0, use_htb=True)  # host interface
        hi_params_others = dict(bw=100, delay='{0}ms'.format(v_delay_link[0]), max_queue_size=100*v_delay[0], use_htb=True)  # host interface


        """ Create the topology by overriding the class parent's method.

            :param  delay   One way propagation delay, delay = RTT / 2. Default is 2ms.
            Obs: 
        """
                
        # Create routers s1 to s4
        s1 = self.addSwitch('s1', failMode='standalone', stp=True)
        s2 = self.addSwitch('s2', failMode='standalone', stp=True)
        s3 = self.addSwitch('s3', failMode='standalone', stp=True)
        s4 = self.addSwitch('s4', failMode='standalone', stp=True)
        

       
        h10 = self.addHost('h10',ip='10.0.0.10')
        h11 = self.addHost('h11',ip='10.0.0.11')
        
        h20 = self.addHost('h20',ip='10.0.0.20')
        h21 = self.addHost('h21',ip='10.0.0.21')
           

        # Link the source hosts (h1 & h3) to access router 1 (s3)
        self.addLink(s3, h10, cls=TCLink, **hi_params)
        self.addLink(s3, h11, cls=TCLink, **hi_params)      
   

        # Link the receiver hosts (h2 & h4) to access router 2 (s4)
        self.addLink(s4, h20, cls=TCLink, **hi_params)
        self.addLink(s4, h21, cls=TCLink, **hi_params)
        
        
        self.addLink( 's3','s1' , cls=TCLink, loss = (v_loss_link)/100, **ar_params )
        self.addLink( 's4','s2' , cls=TCLink, **ar_params )
        self.addLink( 's1','s2' , cls=TCLink, loss = (v_loss[0])/100, **br_params )

topos = {'mytopo': (lambda: SimpleLinkTopo())}


def tcp_test(algs, delays, p_loss, queue, delays_link, loss_link):

    limpa_int()
    global v_loss
    global v_delay
    global v_queue
    global v_delay_link
    global v_loss_link
    v_loss = p_loss
    v_delay = delays
    v_queue = float(queue[0])
    v_delay_link = delays_link
    v_loss_link = float(loss_link[0])
    
    topo = SimpleLinkTopo(delay=v_delay,loss=v_loss, queue = v_queue)
    net = Mininet(topo=topo, switch=OVSBridge,controller=None)
    h10, h11 = net.get('h10','h11')
    h20, h21 = net.get('h20','h21')
    host_addrs = dict({'h10': h10.IP(), 'h11': h11.IP(), 'h20': h20.IP(), 'h21': h21.IP()})
    print('Host addrs: {0}'.format(host_addrs))        
    
    #net = Mininet(topo)
    net.start()
    net.pingAll()

    popens = dict()
    
    alg_ajustado = set(algs)
    for a in alg_ajustado:
        print("*** Descobrindo as interfaces do hosts ...")      

        print("*** Starting teste de capacidade de canal para  ...")
        print("*** Starting iperf alg {}...".format(a))
        
        popens[h20] = h20.popen(['iperf3', '-s', '-p', '5001'])
        delay = v_delay[0]

        runtime = 50
        popens[h10] = h10.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -Z {1} -t {2} --json >> iperf_taxa_max_{1}_{4}_loss_{3}ms.txt'.format(h20.IP(), a, runtime, delay, v_loss), shell=True)
        popens[h10].wait()
        popens[h20].terminate()
        popens[h20].wait()

    
    print("*** Starting iperf servers ...")
    popens[h20] = h20.popen(['iperf3', '-s', '-p', '5001'])
    popens[h21] = h21.popen(['iperf3', '-s', '-p', '5001'])
    
    #delay = delays
    delay = v_delay[0]
    delay_h11_h21 = int(v_delay[0]) + int(v_delay_link[0])
    iperf_runtime = 150
    #alg = ['cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic']
    alg = algs
    print("*** Starting iperf client h1...")
    popens[h10] = h10.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1500 -N -C {1} -t {2} --json >> iperf_{1}_{3}-{4}_{6}_loss_{5}ms.txt'.format(h20.IP(), alg[0], iperf_runtime, 'h10', 'h20', delay, v_loss), shell=True)
    popens[h11] = h11.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 5000 -N -C {1} -t {2} --json >> iperf_{1}_{3}-{4}_{6}_loss_{5}ms.txt'.format(h21.IP(), alg[1], iperf_runtime, 'h11', 'h21', delay, v_loss), shell=True)
  
    
    
    print("*** Waiting {0}sec for iperf clients to finish...".format(iperf_runtime))
    popens[h10].wait()
    popens[h11].wait()

    
    # Terminate the servers and tcpprobe subprocesses
    print('*** Terminate the iperf servers and tcpprobe processes...')
    popens[h20].terminate()
    popens[h21].terminate()
    
    popens[h20].wait()
    popens[h21].wait()
    
    print("*** Stopping test...")
    print('*** Processing data...')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    parser = argparse.ArgumentParser(description='TCP Congestion Control tests in a dumbbell topology.')
    parser.add_argument('-a', '--algorithms', nargs='+', default=['cubic','cubic'], help='List TCP Congestion Control algorithms to test.')
    parser.add_argument('-d', '--delays', nargs='+', type=int, default=[10])
    parser.add_argument('-dl', '--delays_link', nargs='+', type=int, default=[0])
    parser.add_argument('-l', '--loss', nargs='+', type=int, default=[0])
    parser.add_argument('-ll', '--loss_link', nargs='+', type=int, default=[0])
    parser.add_argument('-q', '--queue', nargs='+', type=int, default=[100])
    args = parser.parse_args()

    tcp_test(args.algorithms, args.delays, args.loss, args.queue, args.delays_link, args.loss_link)


