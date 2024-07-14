#/bin/bash

flag=$1
terminal=(162 164 166 168 172 174) # 
# 把 server 和 client 传给所有终端
# Text file busy 传文件报这个错时说明对端server正在被使用，不能被覆盖，所以必须把远端server client 程序关了才能传文件
if [ "$flag" -eq 2 ]; then
    for n in "${terminal[@]}"
    do
        sshpass -p "bjtungirc" scp -o StrictHostKeyChecking=no example/server/server sinet@192.168.199.$n:/home/sinet/multimodal/millionTcp/server/
        sshpass -p "bjtungirc" scp -o StrictHostKeyChecking=no example/client/client sinet@192.168.199.$n:/home/sinet/multimodal/millionTcp/client/
        echo "$n OK"
    done
# 把 开docker容器的脚本 传给所有终端
elif [ "$flag" -eq 3 ]; then
    for n in "${terminal[@]}"
    do
        sshpass -p "bjtungirc" scp -o StrictHostKeyChecking=no startServer.sh sinet@192.168.199.$n:/home/sinet/multimodal/millionTcp/startServer.sh
        sshpass -p "bjtungirc" scp -o StrictHostKeyChecking=no startClients.sh sinet@192.168.199.$n:/home/sinet/multimodal/millionTcp/startClients.sh
        sshpass -p "bjtungirc" scp -o StrictHostKeyChecking=no stopAllContainers.sh sinet@192.168.199.$n:/home/sinet/multimodal/millionTcp/stopAllContainers.sh
        echo "$n OK"
    done
else
    echo "请输出参数 2 或 3"
    exit 1
fi
