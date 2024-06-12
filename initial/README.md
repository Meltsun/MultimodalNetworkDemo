## 说明

#### 文件说明

本文件夹为初始化系统网卡命名（XXX-ports.sh）、同步系统时间（allcloclmake.sh、allptpclocled.sh、distribute_ssh_keys.sh（主控机器：185））、运行bmv2（s-XXX-bmv2.sh）、下发流表（s-XXX-table.sh）功能说明

1、在初始化系统网卡命名之前，要检查6台交换机、8台终端网线物理连接，系统统一选用左侧四个端口和右侧第一个端口进行物理连接，对应网卡命名的bmv2-port1到bmv2-port5。在每个机器中运行XXX-ports.sh文件，进行网卡命名刷新。并运行ipv6_delete.sh，去除每个网口自配ipv6地址。

2、交换机时间同步操作：
（1）查看时钟频率（客户端和服务端都看，把客户端tick调成与服务端一致）
sudo apt-get install adjtimex
sudo adjtimex --print 

（2）重新时间同步一遍
服务端：
service ntp restart
客户端：
sudo systemctl stop ntp
sudo ntpdate 192.168.199.186
sudo systemctl start ntp

（3）查看客户端与服务端两时间偏移量（多次），
sudo ntpdate -q 192.168.199.186 或 ntpq -p

（4）过程3一直增长，值调小，过程3一直减小，值调大。重复3到4，使过程3的结果上下浮动为止
sudo adjtimex --tick  XX 

（5）2到4重新手动时间，同步再来一遍

3、6台交换机编写bmv2运行shell文件，开启bmv2。
./s-XXX-bmv2.sh

4、6台交换机编写流表下发shell文件，下发流表。
./s-XXX-table.sh

### 以上文件均可能需要确保脚本执行权限：chmod +x XXX.sh