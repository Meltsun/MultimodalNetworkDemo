## 说明

#### 文件说明

本文件夹为mininet仿真程序，同时实现多路径调度和INT

包括：

    网络拓扑构建文件 network.py
    交换机逻辑文件 intmultipath.p4
    交换机流表 s176/178/182/184/186/188-commands.txt
    寄存器配置文件 initial_schedule_RR.py
    指令运行文件 run.sh
    垃圾清理文件 clean.sh

#### 指令说明

1、将所有文件复制到虚拟机种

2、增加 run.sh 权限

    sudo chmod +x ./run.sh

3、运行 run.sh

    ./run.sh

4、初始化寄存器

    python3 initial.py

5、开始通信

可选择

    initial.py 中 multipath 置 0
        icmp 单路径传输
        tcp 单路径传输
        udp 单路径传输
    initial.py 中 multipath 置 1
        icmp 多路径传输
        tcp 多路径传输
        udp 单路径传输
