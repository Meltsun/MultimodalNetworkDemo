#!/bin/bash

# 定义需要操作的网络接口
interfaces=("bmv2-port1" "bmv2-port2" "bmv2-port3" "bmv2-port4" "bmv2-port5" "bmv2-port6" "bmv2-port7" "bmv2-port8" "network")

# 查询每个网络接口
for iface in "${interfaces[@]}"; do
    # 检查接口是否存在
    if ip link show $iface &> /dev/null; then
        # 获取该接口上的链路本地地址
        addresses=$(ip -6 addr show dev $iface scope link | grep -oP 'fe80::[^\s/]+')
        
        # 遍历每个链路本地地址并删除
        for addr in $addresses; do
            echo "Deleting $addr on interface $iface"
            sudo ip -6 addr del $addr/64 dev $iface
        done
    else
        echo "Interface $iface does not exist ipv6 address."
    fi
done
