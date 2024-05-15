#!/bin/bash
# 连接到192.168.199.176，端口22，关闭PTP4L进程并删除日志文件
ssh -p 22 sinet@192.168.199.176 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
# 进入/home/sinet71/lk目录，执行关闭PTP4L进程的脚本，将输出重定向到pctp4lclosed.txt文件
ssh -p 22 sinet@192.168.199.176 "cd /home/sinet; nohup sudo rm makeclock* "
# 删除以makeclock开头的所有文件

echo "176 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.182 "cd /home/sinet; nohup sudo rm makeclock*"

echo "182 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.184 "cd /home/sinet; nohup sudo rm makeclock*"

echo "184 : all clock are closed!"
echo "----------------------------------------------"
ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.186 "cd /home/sinet; nohup sudo rm makeclock*"

echo "186 : all clock are closed!"
echo "----------------------------------------------"
ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.188 "cd /home/sinet; nohup sudo rm makeclock*"


echo "188 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.178 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.178 "cd /home/sinet; nohup sudo rm makeclock*"

echo "178 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.166 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.166 "cd /home/sinet; nohup sudo rm makeclock*"

echo "166 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.170 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.170 "cd /home/sinet; nohup sudo rm makeclock*"

echo "170 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.172 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.172 "cd /home/sinet; nohup sudo rm makeclock*"

echo "172 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.162 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.162 "cd /home/sinet; nohup sudo rm makeclock*"

echo "162 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.164 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.164 "cd /home/sinet; nohup sudo rm makeclock*"

echo "164 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.174 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.174 "cd /home/sinet; nohup sudo rm makeclock*"

echo "174 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.180 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.180 "cd /home/sinet; nohup sudo rm makeclock*"

echo "180 : all clock are closed!"
echo "----------------------------------------------"

ssh -p 22 sinet@192.168.199.168 "cd /home/sinet; nohup sudo ./shut_ptp4l.sh > pctp4lclosed.txt 2>&1"
ssh -p 22 sinet@192.168.199.168 "cd /home/sinet; nohup sudo rm makeclock*"

echo "168 : all clock are closed!"
echo "----------------------------------------------"


