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
### 1. 交换机模块 by HXT、CCJ、WJF、XZH
待补充。说明p4程序的功能，启动和配置流程。
所有不在两端而是在中间交换机结点上运行的东西都放在这里，包括INT等。

### 2. 前端展示模块 by LJW
LJW补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 3. 后端数据库模块 by CCJ
CCJ补充，说明运行代码位置、功能、环境配置和运行流程，以及相关说明文档位置

### 4. 百万级链接模块 by WJF
WJF补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 5. 拥塞控制模块 by ZX、CCJ
ZX、CCJ补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 6. 指标测量模块 by GZC
GZC补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 7. 流表下发模块 by WXY
`./controller/p4_command_controller`
利用fabric，通过ssh向bmv2发送命令，实现流表和寄存器下发。相比p4runtime效率更低，但更灵活易懂，且不会独占交换机。
#### 使用方法
本身直接运行没有任何效果，请导入后实现相应的业务逻辑。
接口请查看`controller/p4_command_controller/p4_switch.py`里abc的docstring。
#### 注意事项
1. 建立ssh连接耗时较长，对于每一台交换机，请不要重复创建实例，而是只在程序启动时创建一个实例，之后一直用这一个。
2. 程序结束时记得调用close关闭。
3. 程序目前需要持续和bmv2的cli连接，而一个bmv2同一时间只能打开一个cli。**正在优化**
### 8. 多路径调度模块 by WXY
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
