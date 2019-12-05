from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import OVSController, RemoteController,Node
from mininet.cli import CLI

class SimplePktSwitch(Topo):
   """Simple topology example."""
   def __init__(self, **opts):
      """Create custom topo."""
      import os
      os.system ('sudo mn -c')
      # Initialize topology
      # It uses the constructor for the Topo cloass
      super(SimplePktSwitch, self).__init__(**opts)
      # Adding hosts and setting IP and MAC addresses
      h3 = self.addHost('h3', ip='10.0.0.3',mac='00:00:00:00:00:03')
      h4 = self.addHost('h4', ip='10.0.0.4',mac='00:00:00:00:00:04')
 
      # Adding switches
      s2 = self.addSwitch('s2')
      # Add links
      self.addLink(h3, s2)
      self.addLink(h4, s2)

def run():
    net = Mininet(topo=SimplePktSwitch(),controller=OVSController)
    net.start()
    import os
    # command to setup tunneling port from terminal.
    os.system ('sudo ovs-vsctl add-port s2 gtp2 -- set interface gtp2 type=gtp option:remote_ip=172.31.171.251 option:key=flow ofport_request=10')
    os.system ('sudo ovs-ofctl add-flows s2 VM2flow.txt')
    # following commands are to connect eth1 to the OVS to enable communication between VMs directly
    os.system ('sudo ovs-vsctl add-port s2 eth1')
    os.system ('sudo ifconfig eth1 0.0.0.0')
    os.system ('sudo ifconfig s2 172.31.171.185')
    CLI(net)
    net.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
run()
