#!/usr/bin/env python3

import sys
import time
from probe_hdrs import *

# 发送数据包的函数
def send_probe_pkt(hop_cnt, swid):
    probe_pkt = Ether(dst='ff:ff:ff:ff:ff:ff', src=get_if_hwaddr('eth1')) / \
                Probe(hop_cnt=hop_cnt, data_cnt=0)
    for s in swid:
        probe_pkt /= ProbeFwd(swid=s)

    sendp(probe_pkt, iface='eth1')

def main():

    while True:
        try:
            # 发送第一个路径的数据包
            send_probe_pkt(3, [184, 188, 168])
            time.sleep(1)

            # 发送第二个路径的数据包
            send_probe_pkt(3, [184, 186, 166])
            time.sleep(1)

            # 发送第三个路径的数据包
            send_probe_pkt(3, [184, 182, 162])
            time.sleep(1)

            # 发送第四个路径的数据包
            send_probe_pkt(3, [184, 178, 174])
            time.sleep(1)                    

        except KeyboardInterrupt:
            print("Interrupted by user, stopping...")
            sniff_thread.join()
            sys.exit("Exiting gracefully")            

if __name__ == '__main__':
    main()

