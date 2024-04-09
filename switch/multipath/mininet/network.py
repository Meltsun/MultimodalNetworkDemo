from p4utils.mininetlib.network_API import NetworkAPI
import json
net = NetworkAPI()

# Network general options
net.setLogLevel('info')

# Network definition
#------------------------------------------
net.addHost('h169')
net.addHost('h179')
#------------------------------------------
net.addP4Switch('s175')
net.setP4Source('s175', 'multipath.p4')
net.setP4CliInput('s175', 's175-commands.txt')

net.addP4Switch('s181')
net.setP4Source('s181', 'multipath.p4')
net.setP4CliInput('s181', 's181-commands.txt')

net.addP4Switch('s183')
net.setP4Source('s183', 'multipath.p4')
net.setP4CliInput('s183', 's183-commands.txt')

net.addP4Switch('s185')
net.setP4Source('s185', 'multipath.p4')
net.setP4CliInput('s185', 's185-commands.txt')

net.addP4Switch('s187')
net.setP4Source('s187', 'multipath.p4')
net.setP4CliInput('s187', 's187-commands.txt')

net.addP4Switch('s177')
net.setP4Source('s177', 'multipath.p4')
net.setP4CliInput('s177', 's177-commands.txt')
#------------------------------------------
net.addLink('h169', 's175')
net.addLink('s175', 's181')
net.addLink('s181', 's183')
net.addLink('s181', 's185')
net.addLink('s181', 's187')
net.addLink('s183', 's187')
net.addLink('s185', 's187')
net.addLink('s187', 's177')
net.addLink('s177', 'h179')
#------------------------------------------
net.setIntfPort('h169', 's175', 0)
net.setIntfPort('s175', 'h169', 1)
net.setIntfPort('s175', 's181', 2)
net.setIntfPort('s181', 's175', 1)
net.setIntfPort('s181', 's183', 2)
net.setIntfPort('s181', 's187', 3)
net.setIntfPort('s181', 's185', 4)
net.setIntfPort('s183', 's181', 1)
net.setIntfPort('s183', 's187', 2)
net.setIntfPort('s185', 's181', 1)
net.setIntfPort('s185', 's187', 2)
net.setIntfPort('s187', 's177', 1)
net.setIntfPort('s187', 's183', 2)
net.setIntfPort('s187', 's181', 3)
net.setIntfPort('s187', 's185', 4)
net.setIntfPort('s177', 'h179', 1)
net.setIntfPort('s177', 's187', 2)
net.setIntfPort('h179', 's177', 0)
#------------------------------------------
net.setIntfMac('h169', 's175', '00:00:0A:AA:AA:02')
net.setIntfMac('s175', 'h169', '00:00:0A:AA:AA:01')
net.setIntfMac('h179', 's177', '00:00:0A:B4:B4:02')
net.setIntfMac('s177', 'h179', '00:00:0A:B4:B4:01')
#------------------------------------------
net.setIntfIp('h169', 's175', '10.170.170.2/24')
net.setIntfIp('h179', 's177', '10.180.180.2/24')
#------------------------------------------
net.setDefaultRoute('h169', '10.170.170.1')
net.setDefaultRoute('h179', '10.180.180.1')
#------------------------------------------
# Assignment predefined strategy
#net.mixed()

# Nodes general options
net.enablePcapDumpAll()
net.enableLogAll()

# Start network
net.enableCli()
net.startNetwork()
