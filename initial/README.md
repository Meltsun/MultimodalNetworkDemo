## 说明

#### 文件说明

本文件夹为初始化系统网卡命名（XXX-ports.sh）、同步系统时间（allcloclmake.sh、allptpclocled.sh、distribute_ssh_keys.sh（主控机器：185））、运行bmv2（s-XXX-bmv2.sh）、下发流表（s-XXX-table.sh）功能说明

1、在初始化系统网卡命名之前，要检查6台交换机、8台终端网线物理连接，系统统一选用左侧四个端口和右侧第一个端口进行物理连接，对应网卡命名的bmv2-port1到bmv2-port5。在每个机器中运行XXX-ports.sh文件，进行网卡命名刷新。

2、6台交换机、8台终端编写时间同步shell文件，进行ptp时间同步。
distribute_ssh_keys.sh文件用于分发公钥，保证每个机器都可以无密互操作；
allcloclmake.sh用于配置各主机和交换机的系统时钟同步；
allptpclocled.sh文件用于关闭PTP协议的时钟同步。
统一将185机器作为主控机器，运行文件。

3、6台交换机编写bmv2运行shell文件，开启bmv2。
./s-XXX-bmv2.sh

4、6台交换机编写流表下发shell文件，下发流表。
./s-XXX-table.sh

### 以上文件均可能需要确保脚本执行权限：chmod +x XXX.sh