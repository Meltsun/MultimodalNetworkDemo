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
代码文件均在switch文件夹中的initial文件夹

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
INT相关文件均在switch文件中的INT文件夹中；
六个终端（除去170和180）均进行收发包的操作：
   收包：`sudo python3 int_receive_new.py`   （new文件是带有数据库操作的，如果不想上传数据仅做测试可以运行`int_receive.py`文件；另外注意，164机器的网口和其他几个终端不同，有自己对应的收包文件，文件夹里有对应名字的文件）
   发包：`sudo python3 int_send_XXX.py`       (XXX为对应机器编号）

### 4. 后端数据库模块 by CCJ
CCJ补充，说明运行代码位置、功能、环境配置和运行流程，以及相关说明文档位置

### 5. 百万级链接模块 by WJF
WJF补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 6. 拥塞控制模块 by ZX、CCJ
ZX、CCJ补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 7. 指标测量模块 by GZC
GZC补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 8. 流表下发模块 by WXY
`./controller/p4_command_controller`
利用fabric，通过ssh向bmv2发送命令，实现流表和寄存器下发。相比p4runtime效率更低，但更灵活易懂，且不会独占交换机。
#### 使用方法
本身直接运行没有任何效果，请导入后实现相应的业务逻辑。
接口请查看`controller/p4_command_controller/p4_switch.py`里abc的docstring。
#### 注意事项
1. 建立ssh连接耗时较长，对于每一台交换机，请不要重复创建实例，而是只在程序启动时创建一个实例，之后一直用这一个。
2. 程序结束时记得调用close关闭。
3. 程序目前需要持续和bmv2的cli连接，而一个bmv2同一时间只能打开一个cli。**正在优化**
### 9. 多路径调度模块 by WXY
`./controller/schedule`
使用iperf测试速率和乱序率，使用dqn计算选路策略，使用流表下发模块修改寄存器值来应用策略。
#### 配置
1. 按照example编写config.toml，配置账号密码等(这些东西可不兴往github上放啊)
2. 确认已经安装iperf
3. 安装cuda、pytorch
2. 安装其他python依赖项：fabric typing_extensions pydantic_extra_types netaddr numpy
#### 启动
先启动客户端,再启动服务器
##### 客户端
启动retry_iperf.sh。此脚本会不断的尝试启动iperf客户端。
```bash
bash ./controller/schedule/retry_iperf.sh <server_ip> <port>
```
##### 服务器
直接运行模块时，运行一次调度任务，计算指定轮次后结束。
```bash
cd ./controller
python -m schedule
```
运行整个系统时，请`from schedule import MultiPathTask`。具体请查看docstring。
一个MultiPathTask实例包含一个P4Switch实例，所以同样不适合重复创建。
