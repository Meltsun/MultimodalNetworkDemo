# 多模态项目演示系统

## 开发规范
### 项目目录

为了方便管理，多模态项目使用到的所有文件、代码、文档等，任何需要部署在实体机中的，都应该放在该实体机的一个目录下统一管理。

此目录规定为所有服务器中 sinet 用户根目录下的的 `multimodal` 文件夹。如果此目录不存在就自己新建（使用sinet用户执行 `mkdir ~/multimodal` ）

## 模块说明
### 多路径调度 by WXY
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