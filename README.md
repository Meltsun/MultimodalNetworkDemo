# 多模态项目演示系统

## 开发规范
### 项目目录

为了方便管理，多模态项目使用到的所有文件、代码、文档等，每个文件夹应包含相应`README.md`文件说明各个文件的内容，如果是代码文件，应说明代码属于哪个模块、作用是什么。

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
HXT、CCJ、WJF补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 2. 后端数据库模块 by CCJ
CCJ补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 3. INT探测模块 by HXT
HXT补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 4. 百万级链接模块 by WJF
WJF补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 5. 前端展示模块 by LJW
LJW补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 6. 拥塞控制模块 by ZX、CCJ
ZX、CCJ补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

### 7. 多路径调度模块 by WXY
WXY补充，说明运行代码位置、流程、运行所需环境，以及相关说明文档位置

#### 配置
1. 按照example编写config.toml，配置账号密码等
4. 安装iperf
2. 安装python依赖项：fabric typing_extensions pydantic_extra_types netaddr numpy
3. 单独安装pytorch

#### 启动
客户段启动retry_iperf.sh，不断的尝试启动iperf客户端
```bash
bash ./controller/schedule/retry_iperf.sh <server_ip> <port>
```

测试时直接运行模块，运行一次调度任务
```bash
cd ./controller
#(启动虚拟环境)
python -m schedule
```

运行整个系统时，请`from schedule import MultiPathTask`，请在系统启动时创建一个实例，按需启动。
具体请查看docstring

### 交换机配置下发 by WXY
此模块提供了python接口，用于向bmv2下发流表或修改寄存器。具体请查看p4_switch.py中abc的docstring。
