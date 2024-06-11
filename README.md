# 多模态项目演示系统

## 开发规范
### 项目目录

为了方便管理，多模态项目使用到的所有文件、代码、文档等，任何需要部署在实体机中的，都应该放在该实体机的一个目录下统一管理。

此目录规定为所有服务器中 sinet 用户根目录下的的 `multimodal` 文件夹。如果此目录不存在就自己新建（使用sinet用户执行 `mkdir ~/multimodal` ）

## 模块说明
### 多路径调度
#### 配置
1. 按照example编写config.toml，配置账号密码等
3. 安装pytorch
4. 安卓iperf
2. `pip install toml fabric typing_extensions pydantic_extra_types netaddr numpy`
#### 启动
```bash
cd ./controller/schedule
#启动虚拟环境
python main.py
```
