#!/bin/bash

# 定义要修改的 MAC 地址和对应的新名称的映射关系
declare -A MAC_NAME_MAPPING=(
  ["a0:36:9f:d5:24:90"]="bmv2-port1"
  ["a0:36:9f:d5:24:91"]="bmv2-port2"
  ["a0:36:9f:d5:24:92"]="bmv2-port3"
  ["a0:36:9f:d5:24:93"]="bmv2-port4"
  ["a0:36:9f:d9:3b:80"]="bmv2-port5"
  ["a0:36:9f:d9:3b:81"]="bmv2-port6"
  ["a0:36:9f:d9:3b:82"]="bmv2-port7"
  ["a0:36:9f:d9:3b:83"]="bmv2-port8"
  ["20:88:10:c2:2e:00"]="network"
  ["20:88:10:c2:2e:01"]="unused"   
  # 可以继续添加其他 MAC 地址和名称的映射
)

# 遍历映射关系，针对每个 MAC 地址执行修改操作
for mac in "${!MAC_NAME_MAPPING[@]}"; do
  new_name="${MAC_NAME_MAPPING[$mac]}"
  echo "修改 MAC 地址 $mac 对应的网卡名称为 $new_name"
  
  # 使用 ip 命令修改网卡名称
  sudo ifconfig "$(ip addr show | grep -B 1 "$mac" | head -n 1| awk '{print substr($2, 0, length($2)-1)}')" down
  sudo ip link set dev "$(ip addr show | grep -B 1 "$mac" | head -n 1| awk '{print substr($2, 0, length($2)-1)}')" name "$new_name"
  sudo ifconfig "$(ip addr show | grep -B 1 "$mac" | head -n 1| awk '{print substr($2, 0, length($2)-1)}')" up

  # 检查执行结果
  if [ $? -eq 0 ]; then
    echo "修改成功"
  else
    echo "修改失败"
  fi
done
