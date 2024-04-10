from p4utils.mininetlib.network_API import NetworkAPI
import json
net = NetworkAPI()

# Network general options
net.setLogLevel('info')

# Network definition
#------------------------------------------
net.addHost('h162')
net.addHost('h164')
net.addHost('h166')
net.addHost('h168')
net.addHost('h170')
net.addHost('h172')
net.addHost('h174')
net.addHost('h180')
#------------------------------------------
net.addP4Switch('s176')
net.setP4Source('s176', 'intmultipath.p4')
net.setP4CliInput('s176', 's176-commands.txt')

net.addP4Switch('s178')
net.setP4Source('s178', 'intmultipath.p4')
net.setP4CliInput('s178', 's178-commands.txt')

net.addP4Switch('s182')
net.setP4Source('s182', 'intmultipath.p4')
net.setP4CliInput('s182', 's182-commands.txt')

net.addP4Switch('s184')
net.setP4Source('s184', 'intmultipath.p4')
net.setP4CliInput('s184', 's184-commands.txt')

net.addP4Switch('s186')
net.setP4Source('s186', 'intmultipath.p4')
net.setP4CliInput('s186', 's186-commands.txt')

net.addP4Switch('s188')
net.setP4Source('s188', 'intmultipath.p4')
net.setP4CliInput('s188', 's188-commands.txt')
#------------------------------------------
#net.addLink('h162', 's182', 0, 1, None, intfName1='', intfName2='', addr1='', addr2='')
net.addLink('h162', 's182', 0, 1, None)
net.addLink('h164', 's184', 0, 1, None)
net.addLink('h166', 's186', 0, 1, None)
net.addLink('h168', 's188', 0, 1, None)
net.addLink('h170', 's176', 0, 4, None)
net.addLink('h172', 's176', 0, 1, None)
net.addLink('h174', 's178', 0, 1, None)
net.addLink('s176', 's182', 2, 5, None)
net.addLink('s176', 's186', 3, 2, None)
net.addLink('s178', 'h180', 2, 0, None)
net.addLink('s178', 's184', 4, 2, None)
net.addLink('s178', 's188', 3, 5, None)
net.addLink('s182', 's184', 2, 5, None)
net.addLink('s182', 's186', 4, 3, None)
net.addLink('s182', 's188', 3, 3, None)
net.addLink('s184', 's186', 4, 4, None)
net.addLink('s184', 's188', 3, 4, None)
net.addLink('s186', 's188', 5, 2, None)
#------------------------------------------
net.setIntfMac('h170', 's176', '00:00:00:00:01:70')
net.setIntfMac('s176', 'h170', '00:00:00:00:01:76')
net.setIntfMac('h180', 's178', '00:00:00:00:01:80')
net.setIntfMac('s178', 'h180', '00:00:00:00:01:78')
#------------------------------------------
net.setIntfIp('h162', 's182', '10.162.162.2/24')
net.setIntfIp('h164', 's184', '10.164.164.2/24')
net.setIntfIp('h166', 's186', '10.166.166.2/24')
net.setIntfIp('h168', 's188', '10.168.168.2/24')
net.setIntfIp('h170', 's176', '10.170.170.2/24')
net.setIntfIp('h172', 's176', '10.172.172.2/24')
net.setIntfIp('h174', 's178', '10.174.174.2/24')
net.setIntfIp('h180', 's178', '10.180.180.2/24')
#------------------------------------------
net.setDefaultRoute('h162', '10.162.162.1')
net.setDefaultRoute('h164', '10.164.164.1')
net.setDefaultRoute('h166', '10.166.166.1')
net.setDefaultRoute('h168', '10.168.168.1')
net.setDefaultRoute('h170', '10.170.170.1')
net.setDefaultRoute('h172', '10.172.172.1')
net.setDefaultRoute('h174', '10.174.174.1')
net.setDefaultRoute('h180', '10.180.180.1')
#------------------------------------------
# Assignment predefined strategy
#net.mixed()

# Nodes general options
net.enablePcapDumpAll()
net.enableLogAll()

# Start network
net.enableCli()
net.startNetwork()
