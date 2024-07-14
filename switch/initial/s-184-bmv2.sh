#!/bin/bash

# 执行第一条命令
sudo p4c --arch v1model --target bmv2 multimodel.p4
# 定义日志文件
LOGFILE="logfile184.log"

# 清空日志文件
> $LOGFILE
# 执行第二条命令
sudo /home/sinet/P4/behavioral-model/targets/simple_switch/simple_switch --log-console --thrift-port 9091 -i 1@bmv2-port1 -i 2@bmv2-port2 -i 3@bmv2-port3 -i 4@bmv2-port4 -i 5@bmv2-port5 multimodel.json &>> $LOGFILE
