#!/bin/bash

# ********* 执行该脚本格式 ************
# bash startClient.sh [host_id] [CONNECTIONS]

# 声明关联数组 把所有的IP放在map里。
declare -A datanet_client_ip_map
declare -A ctrlnet_client_ip_map
declare -A datanet_client_mac_map

# 定义控制网 ip 地址
h162_ctrlnet_client_ips=("192.168.199.201" "192.168.199.202" "192.168.199.203" "192.168.199.204")
ctrlnet_client_ip_map["162"]="h162_ctrlnet_client_ips[@]"
h164_ctrlnet_client_ips=("192.168.199.206" "192.168.199.207" "192.168.199.208" "192.168.199.209")
ctrlnet_client_ip_map["164"]="h164_ctrlnet_client_ips[@]"
h166_ctrlnet_client_ips=("192.168.199.211" "192.168.199.212" "192.168.199.213" "192.168.199.214")
ctrlnet_client_ip_map["166"]="h166_ctrlnet_client_ips[@]"
h168_ctrlnet_client_ips=("192.168.199.216" "192.168.199.217" "192.168.199.218" "192.168.199.219")
ctrlnet_client_ip_map["168"]="h168_ctrlnet_client_ips[@]"
h172_ctrlnet_client_ips=("192.168.199.221" "192.168.199.222")
ctrlnet_client_ip_map["172"]="h172_ctrlnet_client_ips[@]"
h174_ctrlnet_client_ips=("192.168.199.224" "192.168.199.225")
ctrlnet_client_ip_map["174"]="h174_ctrlnet_client_ips[@]"
# 定义数据网 ip 地址
h162_datanet_client_ips=("10.162.162.201" "10.162.162.202" "10.162.162.203" "10.162.162.204")
datanet_client_ip_map["162"]="h162_datanet_client_ips[@]"
h164_datanet_client_ips=("10.164.164.201" "10.164.164.202" "10.164.164.203" "10.164.164.204")
datanet_client_ip_map["164"]="h164_datanet_client_ips[@]"
h166_datanet_client_ips=("10.166.166.201" "10.166.166.202" "10.166.166.203" "10.166.166.204")
datanet_client_ip_map["166"]="h166_datanet_client_ips[@]"
h168_datanet_client_ips=("10.168.168.201" "10.168.168.202" "10.168.168.203" "10.168.168.204")
datanet_client_ip_map["168"]="h168_datanet_client_ips[@]"
h172_datanet_client_ips=("10.172.172.201" "10.172.172.202")
datanet_client_ip_map["172"]="h172_datanet_client_ips[@]"
h174_datanet_client_ips=("10.174.174.201" "10.174.174.202")
datanet_client_ip_map["174"]="h174_datanet_client_ips[@]"
# 定义数据网 mac 地址
h162_datanet_client_macs=("08:00:01:62:02:01" "08:00:01:62:02:02" "08:00:01:62:02:03" "08:00:01:62:02:04")
datanet_client_mac_map["162"]="h162_datanet_client_macs[@]"
h164_datanet_client_macs=("08:00:01:64:02:01" "08:00:01:64:02:02" "08:00:01:64:02:03" "08:00:01:64:02:04")
datanet_client_mac_map["164"]="h164_datanet_client_macs[@]"
h166_datanet_client_macs=("08:00:01:66:02:01" "08:00:01:66:02:02" "08:00:01:66:02:03" "08:00:01:66:02:04")
datanet_client_mac_map["166"]="h166_datanet_client_macs[@]"
h168_datanet_client_macs=("08:00:01:68:02:01" "08:00:01:68:02:02" "08:00:01:68:02:03" "08:00:01:68:02:04")
datanet_client_mac_map["168"]="h168_datanet_client_macs[@]"
h172_datanet_client_macs=("08:00:01:72:02:01" "08:00:01:72:02:02")
datanet_client_mac_map["172"]="h172_datanet_client_macs[@]"
h174_datanet_client_macs=("08:00:01:74:02:01" "08:00:01:74:02:02")
datanet_client_mac_map["174"]="h174_datanet_client_macs[@]"

# 先删除之前的client 容器
bash ./stopAllContainers.sh c

# 需要传入的变量，该机器的ID（164，166等）。每个机器的连接数量
host_id=$1
if [ -z "$host_id" ] || ! [[ $host_id =~ ^(162|164|166|168|172|174)$ ]]; then
    echo "ERR : host_id(本机编号) 参数无效，必须在 (162, 164, 166, 168, 172, 174) 之间。\n格式：bash startClient.sh [host_id] [CONNECTIONS]"
    exit 1
fi
CONNECTIONS=$2  # 一般传50000
if [ -z "$CONNECTIONS" ] || [ "$CONNECTIONS" -gt 50000 ]; then
    echo "ERR : 连接数未传入或超过50000，程序退出。"
    exit 1
fi

# 开启多个docker容器，在其中启动 client 程序
datanet_client_ips=(${!datanet_client_ip_map[$1]})
ctrlnet_client_ips=(${!ctrlnet_client_ip_map[$1]})
datanet_client_macs=(${!datanet_client_mac_map[$1]})
for (( i=0; i<${#datanet_client_ips[@]}; i++ )) # 使用下标来遍历数组
do
    container_name=h${1}c$((i+1))
    echo "==> $((i+1))： 该 client 所在docker容器名为 $container_name：控制网 ip: ${ctrlnet_client_ips[$i]}，数据网 ip: ${datanet_client_ips[$i]}，数据网 mac: ${datanet_client_macs[$i]}"
    # 开启 client 容器，默认连接到数据网
    docker run -d -v /home/sinet/multimodal/millionTcp/client:/client \
            --privileged --name=$container_name --network=dataNet \
            --ip=${datanet_client_ips[$i]} --mac-address=${datanet_client_macs[$i]} multimodal_ubt
    # 连接到控制网
    docker network connect --ip=${ctrlnet_client_ips[$i]} ctrlNet $container_name
    # 添加路由信息
    docker exec $container_name route add -net 10.0.0.0 netmask 255.0.0.0 gw 10.$host_id.$host_id.1
    # 执行程序，使用 sh -c 可以传入多个命令；nohup 【CMD】 > /dev/null 2>&1 & 将命令的所有输出都丢弃且不占用本终端
    docker exec $container_name sh -c "cd /client/; nohup ./client -cdip=${datanet_client_ips[$i]} -ccip=${ctrlnet_client_ips[$i]} -cname=${container_name} -host=${host_id} -conn=${CONNECTIONS} > /dev/null 2>&1 &" 
    # docker exec $container_name sh -c "cd /client/; ./client -cdip=${datanet_client_ips[$i]} -ccip=${ctrlnet_client_ips[$i]} -cname=${container_name} -host=${host_id} -conn=${CONNECTIONS}"
    # exit 1 # 先开一个测试
done
echo "client 容器开启完毕 "
