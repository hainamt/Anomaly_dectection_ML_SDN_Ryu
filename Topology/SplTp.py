from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch
from mininet.topo import Topo

class SimpleTopo(Topo):
    
    def __init__(self):
        Topo.__init__(self)

        #Add Switchs
        s01 = self.addSwitch('s01', cls=OVSKernelSwitch, protocols='OpenFlow13')
        s02 = self.addSwitch('s02', cls=OVSKernelSwitch, protocols='OpenFlow13')
        s03 = self.addSwitch('s03', cls=OVSKernelSwitch, protocols='OpenFlow13')

        #Add Hosts
        h01 = self.addHost('h01', cls=Host, ip='10.0.0.11', defaultRoute = None)
        h02 = self.addHost('h02', cls=Host, ip='10.0.0.12', defaultRoute = None)
        h03 = self.addHost('h03', cls=Host, ip='10.0.0.13', defaultRoute = None)
        h04 = self.addHost('h04', cls=Host, ip='10.0.0.14', defaultRoute = None)
        h05 = self.addHost('h05', cls=Host, ip='10.0.0.15', defaultRoute = None)
        h06 = self.addHost('h06', cls=Host, ip='10.0.0.16', defaultRoute = None)

        #Add Links
        self.addLink(h01, s01)
        self.addLink(h02, s01)
        self.addLink(h03, s02)
        self.addLink(h04, s02)
        self.addLink(h05, s03)
        self.addLink(h06, s03)
        self.addLink(s01, s02)
        self.addLink(s02, s03)

topos = {'Simple_Topo': (lambda: SimpleTopo())}

#sudo mn --custom SplTp.py --topo Simple_Topo --controller=remote,ip=10.0.0.x

