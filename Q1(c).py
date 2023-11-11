

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        r1 = self.addNode('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addNode('r2', cls=LinuxRouter, ip='10.1.0.1/24')
        r3= self.addNode('r3', cls=LinuxRouter, ip='10.2.0.1/24')
        

        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add host-switch links in the same subnet
        self.addLink(s1,
                     r1,
                     intfName2='rs1',
                     params2={'ip': '10.0.0.1/25'})

        self.addLink(s2,
                     r2,
                     intfName2='rs2',
                     params2={'ip': '10.1.0.1/25'})
                     
        self.addLink(s3,
                     r3,
                     intfName2='rs3',
                     params2={'ip': '10.2.0.1/25'})

        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1,
                     r2,
                     intfName1='r12',
                     intfName2='r21',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})
         
        self.addLink(r1,
                     r3,
                     intfName1='r13',
                     intfName2='r31',
                     params1={'ip': '10.101.0.3/24'},
                     params2={'ip': '10.101.0.4/24'})
                     
        self.addLink(r2,
                     r3,
                     intfName1='r23',
                     intfName2='r32',
                     params1={'ip': '10.102.0.5/24'},
                     params2={'ip': '10.102.0.6/24'})

        # Adding hosts specifying the default route
        d1 = self.addHost(name='d1',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1')
        d2 = self.addHost(name='d2',
                          ip='10.0.0.252/24',
                          defaultRoute='via 10.0.0.1')
        d3 = self.addHost(name='d3',
                          ip='10.1.0.251/24',
                          defaultRoute='via 10.1.0.1')
        d4 = self.addHost(name='d4',
                          ip='10.1.0.252/24',
                          defaultRoute='via 10.1.0.1')
        d5 = self.addHost(name='d5',
                          ip='10.2.0.251/24',
                          defaultRoute='via 10.2.0.1')
        d6 = self.addHost(name='d6',
                          ip='10.2.0.252/24',
                          defaultRoute='via 10.2.0.1')

        # Add host-switch links
        self.addLink(d1, s1)
        self.addLink(d2, s1)
        self.addLink(d3, s2)
        self.addLink(d4, s2)
        self.addLink(d5, s3)
        self.addLink(d6, s3)
def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r12"))#12
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r21"))#21
    info(net['r3'].cmd("ip route add 10.0.0.0/24 via 10.101.0.3 dev r31"))#31
    #info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.101.0.4 dev r13"))#13
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.100.0.2 dev r12"))#123
    info(net['r2'].cmd("ip route add 10.2.0.0/24 via 10.102.0.6 dev r23"))#23
    info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.102.0.5 dev r32"))#32

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
topos = { 'custom' : NetworkTopo}
