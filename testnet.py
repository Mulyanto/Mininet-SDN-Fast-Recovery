from mininet.topo import Topo
from mininet.node import OVSSwitch
from mininet.node import CPULimitedHost, Host, Node


class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        leftHost = self.addHost( 'h1', cls=Host, ip='10.0.0.1', defaultRoute=None )
        rightHost = self.addHost( 'h2', cls=Host, ip='10.0.0.2', defaultRoute=None )
        topSwitch = self.addSwitch( 's1', cls=OVSSwitch )
        rightSwitch = self.addSwitch( 's2', cls=OVSSwitch )
        botrightSwitch = self.addSwitch ( 's3', cls=OVSSwitch )
        botleftSwitch = self.addSwitch ( 's4', cls=OVSSwitch )
        leftSwitch = self.addSwitch( 's5', cls=OVSSwitch )
        


        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink(leftSwitch, topSwitch)
        self.addLink(topSwitch,rightSwitch)
        #self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )
        self.addLink(rightSwitch, botrightSwitch)
        self.addLink(botrightSwitch, botleftSwitch)
        self.addLink(botleftSwitch, leftSwitch)


topos = { 'mytopo': ( lambda: MyTopo() ) }
