from fabric import Connection
from invoke import Responder
from packet_handle import *
from threading import Thread
import time
import requests

# 客户端服务器

client_host = '192.168.199.170'
username = 'sinet'
password = 'bjtungirc'

server_host = '192.168.199.180'

interface = 'eno1'  # 指定要监听的网络接口
duration = 8  # 指定网卡监听时间，一般比视频时长稍大一些
yes = 'yes'

# pcap 文件路径
server_path = "/home/sinet/project_measure/server.pcap"
client_path = "/home/sinet/project_measure/client.pcap"
# 视频路径
video_path = "/home/sinet/project_measure/webrtc/480p.mp4"


def start_server_tcpdump(server_host, username, password, interface):
    sudo_pass = Responder(
        pattern=f'\[sudo\] password for {username}:',
        response=password + '\n'
    )
    
    with Connection(host=server_host, user=username, connect_kwargs={"password": password}) as conn:
        conn.run(f"sudo timeout {duration} tcpdump -i {interface} src {server_host} and dst {client_host} -w {server_path}", pty=True, watchers=[sudo_pass], warn=True)


def start_client_tcpdump(host, username, password, interface):
    # 配置sudo命令需要的密码
    sudo_pass = Responder(
        pattern=f'\[sudo\] password for {username}:',
        response=password + '\n'
    )
    connect_pass = Responder(
        pattern='Are you sure you want to continue connecting',
        response=yes + '\n'
    )
    scp_pass = Responder(
        pattern=f'sinet\@{server_host}',
        response=password + '\n'
    )

    with Connection(host=client_host, user=username, connect_kwargs={"password": password}) as conn:
        conn.run(f"sudo timeout {duration} tcpdump -i {interface} src {server_host} and dst {client_host} -w client.pcap", pty=True, watchers=[sudo_pass], warn=True)

        # 将抓到的包通过scp发送给180服务器
        conn.run(f"scp /home/sinet/client.pcap {username}@{server_host}:{client_path}", pty=True, watchers=[connect_pass, scp_pass], warn=True)


start_time = time.time()

t1 = Thread(target=start_client_tcpdump, args=(client_host, username, password, interface))
t2 = Thread(target=start_server_tcpdump, args=(server_host, username, password, interface))
threads = [t1, t2]


for t in threads:
    t.start()

for t in threads:
    t.join()


# 对数据包进行处理
# 服务端
packets1 = extract_id_timestamp(server_path)
# 客户端
packets2 = extract_id_timestamp(client_path)

tail_delay, congestion_rate = calculate_tail_delay_and_congestion_rate(packets1, packets2)
resolution = extract_resolution(video_path)

end_time = time.time()

print(end_time - start_time)

print("尾时延(s)：", tail_delay)
print("卡顿率(%)：", congestion_rate)
print("清晰度：", resolution)


information = {"tail_delay":tail_delay, "congestion_rate":congestion_rate, "resolution_height":resolution[0], "resolution_width":resolution[1]}

print(information)

# 将指标传输至数据库（目前数据库没有部署在服务器上）
url = 'http://192.168.199.110:8000/Videosituation/add'

# 要发送的数据
data = information

# 发送 POST 请求
#response = requests.post(url, json=data)

# 检查响应
#if response.status_code == 200:
    #print("数据成功发送到数据库接口！")
#else:
#    print("数据发送失败。)
