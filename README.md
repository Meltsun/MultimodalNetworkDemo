# 多模态项目演示系统

## 开发规范
### 项目目录

为了方便管理，多模态项目使用到的所有文件、代码、文档等均存放到此仓库，每个文件夹应包含相应`README.md`文件说明各个文件的内容，如果是代码文件，应说明代码属于哪个模块、作用是什么。

#### ./controller文件夹说明
包括前端界面代码、后端界面代码、多路径控制层面代码。

#### ./docs文件夹说明
存放网络拓扑、系统运行流程等非代码性质的文档。各个模块的说明性、介绍性、解释性文档，应该放在此处，如：百万级链接的建立原理、指标测试的原理、ENCC拥塞控制的原理、INT测试原理、多路径方法调整原理等。

#### ./switch文件夹说明
存放交换机层面的代码，包括P4、各交换机初始化代码、int代码等。

## 系统运行流程
在所有服务器中git获取本仓库代码到 sinet 用户根目录下的的 `multimodal` 文件夹。如果此目录不存在就自己新建（使用sinet用户执行 `mkdir ~/multimodal` ）

系统包括系统初始化模块、前端展示模块、后端数据库模块、INT探测模块、百万级链接模块、多路径调度模块，具体运行流程如下。
### 1. 系统启动初始化模块 by HXT、CCJ、WJF
代码文件均在switch文件夹中的 initial 文件夹 `./switch/initial`

#### (1)在初始化系统网卡命名之前，要检查6台交换机、8台终端网线物理连接，系统统一选用左侧四个端口和右侧第一个端口进行物理连接，对应网卡命名的 bmv2-port1 到 bmv2-port5。
在每个机器中运行`./XXX-ports.sh`文件，进行网卡命名刷新。并运行`./ipv6_delete.sh`，去除每个网口自配ipv6地址。

#### (2)交换机时间同步操作：
①. 查看时钟频率（客户端和服务端都看，把客户端tick调成与服务端一致）
`sudo apt-get install adjtimex`
`sudo adjtimex --print `

②. 重新时间同步一遍
服务端：
`service ntp restart`
客户端：
`sudo systemctl stop ntp`
`sudo ntpdate 192.168.199.186`
`sudo systemctl start ntp`

③. 查看客户端与服务端两时间偏移量（多次），
`sudo ntpdate -q 192.168.199.186 或 ntpq -p`

④. 过程3一直增长，值调小，过程3一直减小，值调大。重复3到4，使过程3的结果上下浮动为止
`sudo adjtimex --tick  XX `

⑤. 2 到 4 重新手动时间，同步再来一遍

#### (3)6台交换机编写bmv2运行shell文件，开启bmv2。
`./s-XXX-bmv2.sh`

#### (4)6台交换机编写流表下发shell文件，下发流表。
`./s-XXX-table.sh`

### 2. 前端展示模块 by LJW
LJW补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 3. INT探测模块 by HXT
INT相关文件均在switch文件中的INT文件夹中  `./switch/INT`
#### 使用方法
六个终端（除去170和180）均进行收发包的操作：
收包：
   `sudo python3 int_receive_new.py`   
发包：
   `sudo python3 int_send_XXX.py`   (XXX为对应机器编号）
#### 注意事项
收包：new文件是带有数据库操作的，如果不想上传数据仅做测试可以运行 `int_receive.py` 文件；
另外注意，164机器的网口和其他几个终端不同，有自己对应的收包文件，文件夹里有对应名字的文件。

### 4. 后端数据库模块 by CCJ
后端代码文件放在controller模块下的backed文件夹下`./controller/backend`，运行详情请查看readme文件，后端代码的功能主要为存储其他模块发送的数据，并为前端提供数据。

### 5. 百万级链接模块 by WJF
文件在六个终端162、164、166、168、172、174的/mutilmodel/milliontcp文件夹下

流程：

1、首先在六个终端bash stopAllContainers.sh文件

2、在六个终端上运行startserver.sh

3、在六个终端上运行startclient.sh

各文件说明：

example：客户端（主体代码）和服务端的实现层

utils：工具或全局文件（连接数和客户端与服务端端口等全局变量）

ziface：接口

znet：服务器功能的具体实现

	- connection：单个连接的具体实现
 
	- connmanager：连接管理器
 
	- datapack：msg->byte数组，byte数组->msg
 
	- heartbeat：心跳包
 
	- message：应用层的所有数据格式
 
	- msgHandler：收到消息对应的id号，进行相应的route处理
 
	- request：消息和连接绑定
 
	- router：描述相应的信息处理规则
 
	- server：server程序的实现
 
dockerfile：构建需要的镜像

fileFrans：把需要用到的shell文件传递给所有交换机

发文件流程：sever发，client收；sever收到client的文件请求消息后将消息中的文件名读取出来，将相应文件发送给对应的client

### 6. 拥塞控制模块 by ZX、CCJ
说明文件目录在`./controller/congestion_control`,其功能主要为拥塞算法切换

### 7. 指标测量模块 by GZC
说明文件在`./controller/measurement/README.md`下，有启动脚本以及相关说明。

### 8. 流表下发模块 by WXY
`./controller/p4_command_controller`
利用fabric，通过ssh向bmv2发送命令，实现流表和寄存器下发。相比p4runtime效率更低，但更灵活易懂，且不会独占交换机。
#### 使用方法
本身直接运行没有任何效果，请导入后实现相应的业务逻辑。
接口请查看`controller/p4_command_controller/p4_switch.py`里abc的docstring。
#### 注意事项
1. 建立ssh连接耗时较长，对于每一台交换机，请不要重复创建实例，而是只在程序启动时创建一个实例，之后一直用这一个。
2. 程序结束时记得调用close关闭ssh连接。

### 9. 多路径调度模块 by WXY
`./controller/schedule`
使用iperf测试速率和乱序率，使用ddqn计算选路策略，使用流表下发模块修改寄存器值来应用策略
目前修改188和182的寄存器

#### 配置
1. 按照example编写config.toml，配置账号密码等(这些东西可不兴往github上放啊)
2. 确认已经安装iperf
3. 安装cuda、pytorch
2. 安装其他python依赖项：fabric typing_extensions pydantic_extra_types netaddr numpy toml
#### 启动，直接运行模块时
直接运行模块时，运行一次调度任务，计算指定轮次后结束。
```bash
#服务端服务器（179）
cd ./controller
python -m schedule
```
等待初始化完成后会有提示，要求启动或重启客户端.
**重复测试时，每次服务端重启后，必须重启客户端，否则iperf无法连接**

```bash
#客户端服务器（169）
bash ./client/retry_iperf.sh <server_ip> <port>
```
#### 作为模块导入
`from schedule import MultiPathTask`
具体请查看docstring和__main__
一个MultiPathTask实例包含2个P4Switch实例，所以同样不适合重复创建

### 10. 网络连接配置 by WJF
##### 终端：
文件在六个终端162、164、166、168、172、174的/mutilmodel/milliontcp文件夹下
运行sudo ./write.sh文件进行以下操作：

1、设置静态 IP 地址和 DNS

2、禁用 IPv6

3、绑定 MAC 地址

4、配置路由
##### 交换机：
文件在6个交换机176、178、182、184、186、188的/ECCN文件下
运行sudo ./writeswitch.sh文件进行以下操作：

1、禁用IPv4和IPv6

2、绑定MAC地址
