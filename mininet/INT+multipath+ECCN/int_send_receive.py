#!/usr/bin/env python3

import sys
import time
import threading
from probe_hdrs import *

# 定义数据包格式
"""class Probe(Packet):
    name = "Probe"
    fields_desc = [ByteField("hop_cnt", 0),
                   ByteField("data_cnt", 0)]

class ProbeFwd(Packet):
    name = "ProbeFwd"
    fields_desc = [ByteField("egress_spec", 0)]"""

def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x

# 接收数据包的函数
def receive_probe_pkt(pkt):
    print(pkt)
    #if ProbeData in pkt:
    #    data_layers = [l for l in expand(pkt) if l.name == 'ProbeData']
    #    print(data_layers, "\n")
    #    """for sw in data_layers:
    #        utilization = 0 if sw.cur_time == sw.last_time else 8.0 * sw.byte_cnt / (sw.cur_time - sw.last_time)
    #        length = sw.qdepth
    #        print("Switch {} - Port {}: {} Mbps in-packets {} out-packets {} q-Length: {}".format(sw.swid, sw.port,
    #                                                                                                utilization,
    #                                                                                                sw.pckcont,
    #                                                                                                sw.enpckcont,
    #                                                                                                length))"""
            #bedelay = data_layers[0].cur_time
        #for i in range(0, len(data_layers)):
        #    utilization = 0 if data_layers[i].cur_time == data_layers[i].last_time else 8.0 * data_layers[
        #        i].byte_cnt / (data_layers[i].cur_time - data_layers[i].last_time)
        #    #length = data_layers[i].qdepth
        #    droppkt = data_layers[i].pckcont - data_layers[i - 1].enpckcont
        #    #timein = data_layers[i].in_time
        #    #timeout = data_layers[i].cur_time
        #    delay= data_layers[i].in_time-data_layers[i-1].cur_time
        #    #bedelay= data_layers[i].cur_time 
        #    print(
        #        "node1:{} node2:{} delay:{}us bw:{} Mbps droppkt:{} \n".format(data_layers[i-1].swid, data_layers[i].swid, delay, utilization, droppkt))


# 发送数据包的函数
def send_probe_pkt(hop_cnt, swid):
    probe_pkt = Ether(dst='ff:ff:ff:ff:ff:ff', src=get_if_hwaddr('h170-eth0')) / \
                Probe(hop_cnt=hop_cnt, data_cnt=0)
    for s in swid:
        probe_pkt /= ProbeFwd(swid=s)

    sendp(probe_pkt, iface='h170-eth0')

def start_sniff_thread():
    iface = 'h170-eth0'
    print("sniffing on {}".format(iface))
    sniff(iface=iface, prn=lambda x: receive_probe_pkt(x))

def main():
    #启动一个线程来进行数据包接收
    sniff_thread = threading.Thread(target=start_sniff_thread)
    sniff_thread.start()

    while True:
        try:
            # 发送第一个路径的数据包
            send_probe_pkt(8, [176, 186, 188, 178, 184, 182, 176, 170])
            time.sleep(1)

            """# 发送第二个路径的数据包
            send_probe_pkt(6, [1, 2, 5, 3, 1, 0])
            time.sleep(1)"""

            """# 发送第三个路径的数据包
            send_probe_pkt(6, [3, 4, 4, 1, 4, 1, 1, 0])
            time.sleep(1)"""

        except KeyboardInterrupt:
            sys.exit()

if __name__ == '__main__':
    main()

