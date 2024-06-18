## 拥塞模块运行流程

在运行拥塞模块前需要完成以下流程：
```python
完成相应终端主机的内核编译
完成系统启动初始化模块:具体详情请查看介绍
在打开6台交换机的bmv2，同时完成流表下发文件后，即可在服务器开启后端代码。
"6台交换机编写bmv2运行shell文件，开启bmv2"(s-XXX-bmv2.sh,和s-XXX-table.sh和multimodel.p4、s176-commands.txt)
请放在同一文件夹下）bmv2打开需要一段时间，请不要立即运行./s-XXX-table.sh文件
./s-XXX-bmv2.sh
./s-XXX-table.sh
服务器开启后端代码：
python main.py

在tcp层进行拥塞算法切换需要提前进行拥塞算法的下载编译，例如bbr
sudo modprobe -a tcp_bbr（即可完成下载编译，如要比较其他算法，请自行下载编译）

在前端点击相应按钮后，后端服务器即进行拥塞算法切换。
```

## 拥塞模块原理
我们的拥塞控制算法名为encc,在本项目中，我们在6台交换机中开启bmv2运行我们的multimodel.p4代码，同时我们在相应的主机进行了内核编译。
```python
"内核编译请参考"：https://github.com/lkseagle/end-host-and-network-cooperation
在该网站上，我们已经完成了ubuntu的内核编译，其中内核版本为linux-5.4.224，因为我们的代码是基于 Reno 原始代码修改。如果要运行我们的算法，需要将拥塞算法切换为reno。
如果相应编译其他的内核版本，请自行编译。
我们主要更改了tcp_cong.c文件中的tcp_reno_cong_avoid函数和tcp_input.c文件中的tcp_parse_options函数，以及tcp.h文件中的tcp_options_received（我们新增了一个可选项my_wnd）
如果想在我们的代码基础上修改，请参考这3个文件。
路径：/usr/src/linu-x.x.x/include/linux/tcp.h
    /usr/src/ linu-x.x.x/ net/ipv4/tcp_input.c
    /usr/src/linu-x.x.x/net/ipv4/tcp_cong.c
```

## P4代码encc算法简要介绍：
我们的encc算法实在reno上更改的，因此要运行我们的算法，需要将拥塞算法切换为reno。
在交换机运行的p4代码，我们的的encc算法逻辑如下：
```text
在p4代码中我们定义了一个寄存器register< bit<32> >(8) transmition_model;
其中transmition_model[0]=1，则使用ECCN，=0则不用，对于该寄存器可在流表下发阶段进行写入。
register_write transmition_model 0 1（具体文件可参考`./switch/initial`中的文本文件）
```
```text
如果transmition_model[0]=1且发送的包为tcp包，即可使用我们的encc算法。在该算法中，我们仅对拥塞控制时间以内、超出数据包传输时间的ACK包进行处理，且不处理入网第一跳的ACK包。
在我们的算法中，我们根据当前时间与上次拥塞时间的时间差通过不同的逻辑来进行窗口中的更新，同时为tcp包增添一个头部（my_wnd），这与编译内核中的处理逻辑匹配，从而在终端窗口就可以通过我们的encc算法进行窗口值更新。
```
