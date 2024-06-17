
1、添加wireshark解析数据包权限(xxx为用户名)

    sudo groupadd wireshark
    sudo chgrp wireshark /usr/bin/dumpcap
    sudo chmod 4755 /usr/bin/dumpcap
    sudo gpasswd -a xxx wireshark

2、将文件dissector_INT.lua复制进入home/xxx文件夹

3、添加wireshark插件(xxx为用户名)

    进入 /usr/share/wireshark/init.lua
    文件前几行，确定enable_lua为true
    在最后一行添加
    dofile("/home/xxx/dissector_INT.lua")

4、命令行输入wireshark或直接打开软件，即可解析数据包
