# Created By Ali Malik


from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink


def topology():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)
    # Add hosts and switches

    h1 = net.addHost('h1', mac="00:00:00:00:00:01")
    h2 = net.addHost('h2', mac="00:00:00:00:00:02")

    S1 = net.addSwitch('s1')
    S2 = net.addSwitch('s2')
    S3 = net.addSwitch('s3')
    S4 = net.addSwitch('s4')
    S5 = net.addSwitch('s5')
    S6 = net.addSwitch('s6')
    S7 = net.addSwitch('s7')
    S8 = net.addSwitch('s8')
    S9 = net.addSwitch('s9')
    S10 = net.addSwitch('s10')
    S11 = net.addSwitch('s11')
    S12 = net.addSwitch('s12')
    S13 = net.addSwitch('s13')
    S14 = net.addSwitch('s14')
    S15 = net.addSwitch('s15')
    S16 = net.addSwitch('s16')
    S17 = net.addSwitch('s17')
    S18 = net.addSwitch('s18')
    S19 = net.addSwitch('s19')
    S20 = net.addSwitch('s20')
    S21 = net.addSwitch('s21')
    S22 = net.addSwitch('s22')
    S23 = net.addSwitch('s23')
    S24 = net.addSwitch('s24')
    S25 = net.addSwitch('s25')
    S26 = net.addSwitch('s26')
    S27 = net.addSwitch('s27')
    S28 = net.addSwitch('s28')
    S29 = net.addSwitch('s29')
    S30 = net.addSwitch('s30')
    S31 = net.addSwitch('s31')
    S32 = net.addSwitch('s32')
    S33 = net.addSwitch('s33')
    S34 = net.addSwitch('s34')
    S35 = net.addSwitch('s35')
    S36 = net.addSwitch('s36')
    S37 = net.addSwitch('s37')

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Add links
    # 10
    net.addLink(h1, S1)  # s1 is the source switch
    net.addLink(h2, S36)  # s36 is the destination switch
    net.addLink(S1, S2)
    net.addLink(S1, S5)
    net.addLink(S1, S4)
    net.addLink(S3, S5)
    net.addLink(S3, S13)
    net.addLink(S3, S20)
    net.addLink(S12, S14)
    net.addLink(S10, S12)
    net.addLink(S10, S8)
    net.addLink(S10, S11)

    # 20
    net.addLink(S7, S9)
    net.addLink(S2, S3)
    net.addLink(S4, S3)
    net.addLink(S5, S7)
    net.addLink(S5, S6)
    net.addLink(S6, S8)
    net.addLink(S6, S13)
    net.addLink(S13, S15)
    net.addLink(S13, S16)
    net.addLink(S13, S12)

    # 30
    net.addLink(S15, S14)
    net.addLink(S7, S10)
    net.addLink(S20, S19)
    net.addLink(S20, S21)
    net.addLink(S16, S19)
    net.addLink(S16, S17)
    net.addLink(S19, S18)
    net.addLink(S21, S18)
    net.addLink(S18, S17)
    net.addLink(S17, S34)

    # 40
    net.addLink(S17, S15)
    net.addLink(S37, S11)
    net.addLink(S37, S14)
    net.addLink(S37, S34)
    net.addLink(S11, S9)
    net.addLink(S11, S29)
    net.addLink(S9, S25)
    net.addLink(S9, S26)
    net.addLink(S9, S28)
    net.addLink(S28, S29)

    # 50
    net.addLink(S28, S30)
    net.addLink(S29, S31)
    net.addLink(S31, S32)
    net.addLink(S31, S34)
    net.addLink(S31, S35)
    net.addLink(S34, S36)
    net.addLink(S36, S35)
    net.addLink(S35, S33)
    net.addLink(S33, S32)
    net.addLink(S32, S30)

    # 57
    net.addLink(S30, S27)
    net.addLink(S27, S26)
    net.addLink(S26, S23)
    net.addLink(S23, S22)
    net.addLink(S23, S24)
    net.addLink(S22, S25)
    net.addLink(S25, S24)

    net.build()
    c0.start()

    S1.start([c0])
    S2.start([c0])
    S3.start([c0])
    S4.start([c0])
    S5.start([c0])
    S6.start([c0])
    S7.start([c0])
    S8.start([c0])
    S9.start([c0])
    S10.start([c0])
    S11.start([c0])
    S12.start([c0])
    S13.start([c0])
    S14.start([c0])
    S15.start([c0])
    S16.start([c0])
    S17.start([c0])
    S18.start([c0])
    S19.start([c0])
    S20.start([c0])
    S21.start([c0])
    S22.start([c0])
    S23.start([c0])
    S24.start([c0])
    S25.start([c0])
    S26.start([c0])
    S27.start([c0])
    S28.start([c0])
    S29.start([c0])
    S30.start([c0])
    S31.start([c0])
    S32.start([c0])
    S33.start([c0])
    S34.start([c0])
    S35.start([c0])
    S36.start([c0])
    S37.start([c0])

    h1.cmd("arp -s 10.0.0.2 00:00:00:00:00:02")
    h2.cmd("arp -s 10.0.0.1 00:00:00:00:00:01")
    h1.cmd("tcpdump -i h1-eth0 -nn -X 'icmp' -w send &")
    h2.cmd("tcpdump -i h2-eth0 -nn -X 'icmp' -w receive &")

    print
    "*** Running CLI"

    CLI(net)

    print
    "*** Stopping network"

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    topology()
