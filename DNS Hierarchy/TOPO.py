"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        telnet = self.addHost( 'telnet' )
        agent = self.addHost( 'agent' )
        root = self.addHost( 'root' )
        new_com = self.addHost( 'new_com' )
        new_org = self.addHost( 'new_org' )
	ut= self.addHost( 'ut' )
	sut= self.addHost( 'sut')
	wiki1= self.addHost( 'wiki1')
	wiki2= self.addHost( 'wiki2')

        s1 = self.addSwitch( 's1' )
        # Add links
        self.addLink( telnet, s1)
	self.addLink( agent, s1)
	self.addLink(root, s1)
	self.addLink(new_com, s1)
	self.addLink(new_org, s1)
	self.addLink(ut, s1)
	self.addLink(sut, s1)
	self.addLink(wiki1, s1)
	self.addLink(wiki2, s1)


topos = { 'mytopo': ( lambda: MyTopo() ) }
