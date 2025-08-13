#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, Host
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def setup_topology():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSSwitch)

    info("*** Adding controllers\n")
    c0 = net.addController('c0', ip='127.0.0.1', port=6653)
    c1 = net.addController('c1', ip='127.0.0.1', port=6654)
    c2 = net.addController('c2', ip='127.0.0.1', port=6655)

    info("*** Adding switches\n")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    info("*** Adding hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')

    info("*** Creating links\n")
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(s1, s2)
    net.addLink(s2, s3)

    info("*** Starting network\n")
    net.build()
    c0.start()
    c1.start()
    c2.start()
    s1.start([c0])
    s2.start([c1])
    s3.start([c2])

    info("*** Running CLI\n")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_topology()
