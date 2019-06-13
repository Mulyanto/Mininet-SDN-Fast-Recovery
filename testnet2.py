from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        topSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )
        botrightSwitch = self.addSwitch ( 's3' )
        botleftSwitch = self.addSwitch ( 's4' )
        leftSwitch = self.addSwitch( 's5' )
        


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
