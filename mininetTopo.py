# Import necessary Mininet modules
from mininet.topo import Topo
from mininet.node import OVSSwitch
from mininet.node import OVSBridge
from mininet.link import TCLink

# Define a custom topology class MyTopo that inherits from Mininet's Topo class
class MyTopo(Topo):
    "Simple topology example."

    def build(self):
        "Create custom topology."

        # Add hosts and switches to the topology
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add links between hosts and switches with specified bandwidths
        self.addLink(h1, s1, cls=TCLink) 
        self.addLink(h2, s1, cls=TCLink)
        self.addLink(h3, s2, cls=TCLink)  
        self.addLink(h4, s2, cls=TCLink)

        # Add a link between switches with specified bandwidth and packet loss
        self.addLink(s1, s2, cls=TCLink)  

# Define a dictionary 'topos' where the key is 'custom' and the value is a lambda function
# that creates an instance of the MyTopo class
topos = {'custom': (lambda: MyTopo())}
