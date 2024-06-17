#!/bin/bash

# ********* 执行该脚本格式 ************
# bash startServer.sh [host_id] 

# 声明关联数组 把所有的IP放在map里。
declare -A datanet_server_ip_map
declare -A ctrlnet_server_ip_map
declare -A datanet_server_mac_map

# 定义控制网 ip 地址
ctrlnet_server_ip_map["162"]="192.168.199.200"
ctrlnet_server_ip_map["164"]="192.168.199.205"
ctrlnet_server_ip_map["166"]="192.168.199.210"
ctrlnet_server_ip_map["168"]="192.168.199.215"
ctrlnet_server_ip_map["172"]="192.168.199.220"
ctrlnet_server_ip_map["174"]="192.168.199.223"
# 定义数据网 ip 地址
datanet_server_ip_map["162"]="10.162.162.200"
datanet_server_ip_map["164"]="10.164.164.200"
datanet_server_ip_map["166"]="10.166.166.200"
datanet_server_ip_map["168"]="10.168.168.200"
datanet_server_ip_map["172"]="10.172.172.200"
datanet_server_ip_map["174"]="10.174.174.200"
# 定义数据网 mac 地址
datanet_server_mac_map["162"]="08:00:01:62:02:00"
datanet_server_mac_map["164"]="08:00:01:64:02:00"
datanet_server_mac_map["166"]="08:00:01:66:02:00"
datanet_server_mac_map["168"]="08:00:01:68:02:00"
datanet_server_mac_map["172"]="08:00:01:72:02:00"
datanet_server_mac_map["174"]="08:00:01:74:02:00"

# 先删除之前的 server 容器
bash ./stopAllContainers.sh s

# 需要传入的变量：该机器的ID（164，166等） 
host_id=$1
if [ -z "$host_id" ] || ! [[ $host_id =~ ^(162|164|166|168|172|174)$ ]]; then
    echo "ERR : host_id(本机编号) 参数无效，必须在 (162, 164, 166, 168, 172, 174) 之间。格式：bash startServer.sh [host_id] "
    exit 1
fi

# 开启一个docker容器，在其中启动 server 程序
ctrlnet_server_ip=${ctrlnet_server_ip_map["$1"]}
datanet_server_ip=${datanet_server_ip_map["$1"]}
datanet_server_mac=${datanet_server_mac_map["$1"]}
container_name=h${1}s1
echo "==> 该 server 所在docker容器名为 $container_name：控制网 IP：${ctrlnet_server_ip}，数据网 IP：${datanet_server_ip}，数据网 MAC：${datanet_server_mac}"

# 开启 server 容器，默认连接到数据网
docker run -d -v /home/sinet/multimodal/millionTcp/server:/server \
            --privileged --name=$container_name --network=dataNet \
            --ip=$datanet_server_ip --mac-address=$datanet_server_mac multimodal_ubt
# 连接到控制网
docker network connect --ip=$ctrlnet_server_ip ctrlNet $container_name
# 添加路由信息
docker exec $container_name route add -net 10.0.0.0 netmask 255.0.0.0 gw 10.$host_id.$host_id.1
# 执行程序，使用 sh -c 可以传入多个命令；nohup 【CMD】 > /dev/null 2>&1 & 将命令的所有输出都丢弃且不占用本终端
docker exec $container_name sh -c "cd /server/; nohup ./server -sdip=${datanet_server_ip} -scip=${ctrlnet_server_ip} -sname=${container_name} > /dev/null 2>&1 &"

echo "server 容器开启完毕 "
