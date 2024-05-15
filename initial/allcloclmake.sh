#!/bin/bash
# 连接到192.168.199.176，端口22，关闭PTP4L进程并设置时钟同步
ssh -p 22 sinet@192.168.199.176 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
# 进入/home/sinet目录，执行关闭PTP4L进程的脚本，将输出重定向到pctp4lclosed.txt文件

ssh -p 22 sinet@192.168.199.176 "cd /home/sinet; sudo ifconfig bmv2-port3 up; nohup sudo ptp4l -i bmv2-port3 -m -H > makeclock3.txt 2>&1 &"
# 配置bmv2-port3网卡，并激活
# 启动PTP4L以bmv2-port3网卡为接口，以守护进程形式运行并将输出重定向到makeclock2.txt文件
ssh -p 22 sinet@192.168.199.176 "cd /home/sinet; sudo ifconfig bmv2-port2 up; nohup sudo ptp4l -i bmv2-port2 -s -m -H > makeclock2.txt 2>&1 &"
# 配置bmv2-port2网卡，并激活
# 启动PTP4L以bmv2-port2网卡为接口，以守护进程形式运行并将输出重定向到makeclock3.txt文件
ssh -p 22 sinet@192.168.199.176 "cd /home/sinet; sudo ifconfig bmv2-port1 up; nohup sudo ptp4l -i bmv2-port1 -s -m -H > makeclock1.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.176 "cd /home/sinet; sudo ifconfig bmv2-port4 up; nohup sudo ptp4l -i bmv2-port4 -s -m -H > makeclock4.txt 2>&1 &"
echo "176 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; sudo ifconfig bmv2-port1 up; nohup sudo ptp4l -i bmv2-port1 -s -m -H > makeclock1.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; sudo ifconfig bmv2-port2 up; nohup sudo ptp4l -i bmv2-port2 -s -m -H > makeclock2.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; sudo ifconfig bmv2-port3 up; nohup sudo ptp4l -i bmv2-port3 -s -m -H > makeclock3.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; sudo ifconfig bmv2-port4 up; nohup sudo ptp4l -i bmv2-port4 -s -m -H > makeclock4.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; sudo ifconfig bmv2-port5 up; nohup sudo ptp4l -i bmv2-port5 -s -m -H > makeclock5.txt 2>&1 &"
echo "186 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; sudo ifconfig bmv2-port1 up; nohup sudo ptp4l -i bmv2-port1 -s -m -H > makeclock1.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; sudo ifconfig bmv2-port2 up; nohup sudo ptp4l -i bmv2-port2 -s -m -H > makeclock2.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; sudo ifconfig bmv2-port3 up; nohup sudo ptp4l -i bmv2-port3 -s -m -H > makeclock3.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; sudo ifconfig bmv2-port4 up; nohup sudo ptp4l -i bmv2-port4 -m -H > makeclock4.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; sudo ifconfig bmv2-port5 up; nohup sudo ptp4l -i bmv2-port5 -m -H > makeclock5.txt 2>&1 &"
echo "182 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; sudo ifconfig bmv2-port1 up; nohup sudo ptp4l -i bmv2-port1 -s -m -H > makeclock1.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; sudo ifconfig bmv2-port2 up; nohup sudo ptp4l -i bmv2-port2 -s -m -H > makeclock2.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; sudo ifconfig bmv2-port3 up; nohup sudo ptp4l -i bmv2-port3 -s -m -H > makeclock3.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; sudo ifconfig bmv2-port4 up; nohup sudo ptp4l -i bmv2-port4 -m -H > makeclock4.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; sudo ifconfig bmv2-port5 up; nohup sudo ptp4l -i bmv2-port5 -m -H > makeclock5.txt 2>&1 &"
echo "184 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.178 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.178 "cd /home/sinet; sudo ifconfig bmv2-port1 up; nohup sudo ptp4l -i bmv2-port1 -s -m -H > makeclock1.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.178 "cd /home/sinet; sudo ifconfig bmv2-port3 up; nohup sudo ptp4l -i bmv2-port3 -s -m -H > makeclock3.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.178 "cd /home/sinet; sudo ifconfig bmv2-port2 up; nohup sudo ptp4l -i bmv2-port2 -m -H > makeclock2.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.178 "cd /home/sinet; sudo ifconfig bmv2-port4 up; nohup sudo ptp4l -i bmv2-port4 -s -m -H > makeclock4.txt 2>&1 &"
echo "178 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; sudo ifconfig bmv2-port1 up; nohup sudo ptp4l -i bmv2-port1 -s -m -H > makeclock1.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; sudo ifconfig bmv2-port2 up; nohup sudo ptp4l -i bmv2-port2 -m -H > makeclock2.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; sudo ifconfig bmv2-port3 up; nohup sudo ptp4l -i bmv2-port3 -m -H > makeclock3.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; sudo ifconfig bmv2-port4 up; nohup sudo ptp4l -i bmv2-port4 -m -H > makeclock4.txt 2>&1 &"
ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; sudo ifconfig bmv2-port5 up; nohup sudo ptp4l -i bmv2-port5 -m -H > makeclock5.txt 2>&1 &"
echo "188 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.166 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.166 "cd /home/sinet; sudo ifconfig eno2 up; nohup sudo ptp4l -i eno2 -m -H > makeclock1.txt 2>&1 &"
echo "166 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.170 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.170 "cd /home/sinet; sudo ifconfig eno2 up; nohup sudo ptp4l -i eno2 -m -H > makeclock1.txt 2>&1 &"
echo "170 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.172 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.172 "cd /home/sinet; sudo ifconfig eno2 up; nohup sudo ptp4l -i eno2 -m -H > makeclock1.txt 2>&1 &"
echo "172 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.162 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.162 "cd /home/sinet; sudo ifconfig eno2 up; nohup sudo ptp4l -i eno2 -m -H > makeclock1.txt 2>&1 &"
echo "162 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.164 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.164 "cd /home/sinet; sudo ifconfig eth1 up; nohup sudo ptp4l -i eth1 -m -H > makeclock1.txt 2>&1 &"
echo "164 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.174 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.174 "cd /home/sinet; sudo ifconfig eno2 up; nohup sudo ptp4l -i eno2 -m -H > makeclock1.txt 2>&1 &"
echo "174 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.180 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.180 "cd /home/sinet; sudo ifconfig eno2 up; nohup sudo ptp4l -i eno2 -m -H > makeclock1.txt 2>&1 &"
echo "180 : all clock are maked!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.168 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.168 "cd /home/sinet; sudo ifconfig eno2 up; nohup sudo ptp4l -i eno2 -m -H > makeclock1.txt 2>&1 &"
echo "168 : all clock are maked!"
echo "----------------------------------------------"



