## 一、说明

该拓扑为minient最终拓扑，完全模拟实际网络节点信息，网口名称、IP、MAC、端口号均相同，便于各编程人员进行仿真测试。

## 二、相关依赖

该network.py文件需要特殊的python模块p4-utils，该模块安装教程如下

1、下载该模块

    git clone https://github.com/nsg-ethz/p4-utils

2、 安装该模块

    cd p4-utils
    sudo ./install.sh

3、登录https://nsg-ethz.github.io/p4-utils/usage.html学习p4-utils模块相关函数