from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.link import Link, TCLink

def topology():
    net = Mininet()
    #net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
    # Add hosts and switches
    #h1= net.addHost( 'h1', mac="00:00:00:00:00:01" )
    #h2 = net.addHost( 'h2', mac="00:00:00:00:00:02" )

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    S1 = net.addSwitch('s1')
    S2 = net.addSwitch('s2')
    S3 = net.addSwitch('s3')
    S4 = net.addSwitch('s4')
    S5 = net.addSwitch('s5')
    S6 = net.addSwitch('s6')

    # c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
    c0 = net.addController('c0')

    # Add links
    net.addLink(h1, S1)  # s1 is the source switch
    net.addLink(h2, S6)  # s36 is the destination switch

    net.addLink(S1, S2)
    net.addLink(S1, S4)

    net.addLink(S2, S3)
    net.addLink(S4, S5)

    net.addLink(S3, S6)
    net.addLink(S5, S6)

    net.build()
    c0.start()
    S1.start([c0])
    S2.start([c0])
    S3.start([c0])
    S4.start([c0])
    S5.start([c0])
    S6.start([c0])

    # h1.cmd("arp -s 10.0.0.2 00:00:00:00:00:02")
    # h2.cmd("arp -s 10.0.0.1 00:00:00:00:00:01")
    # h1.cmd("tcpdump -i h1-eth0 -nn -X 'icmp' -w send &")
    # h2.cmd("tcpdump -i h2-eth0 -nn -X 'icmp' -w receive &")

    print("*** Running CLI")
    CLI(net)

    # print "*** Stopping network"
    # net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()


