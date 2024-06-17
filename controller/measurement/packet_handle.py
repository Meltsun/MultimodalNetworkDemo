import dpkt
import cv2


# 两个数据，时间戳，包id
def extract_id_timestamp(file_path, protocols):
    packets = {}
    with open(file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if protocols == 22 or protocols == 23:
                    # 处理udp包
                    if isinstance(ip.data, dpkt.udp.UDP):
                        packets[ip.id] = timestamp
                elif protocols == 24:
                    # 处理TCP包
                    if isinstance(ip.data, dpkt.tcp.TCP):
                        packets[ip.id] = timestamp
                else:
                    print("端口号开启有问题")
    return packets


# 测试尾时延(此处定义为最大时延)
def calculate_tail_delay_and_congestion_rate(packets1, packets2):
    # 尾时延
    tail_delay = 0
    delay = []
    for packet1_id in packets1:
        if packet1_id in packets2:
            arrival_time1 = packets1[packet1_id]
            arrival_time2 = packets2[packet1_id]
            delay.append(abs(arrival_time2 - arrival_time1))
            # tail_delay = max(tail_delay, abs(arrival_time2 - arrival_time1))
    delay.sort()
    
    # 计算最大1%的时延平均值
    tail_percentage = 0.01
    tail_count = max(1, int(len(delay) * tail_percentage))
    tail_delays = delay[-tail_count:]
    tail_delay = sum(tail_delays) / len(tail_delays)
    
    if delay:
        average_value = sum(delay) / len(delay)

    values_greater_than_average = []
    for num in delay:
        if num > average_value * 1.2:
            values_greater_than_average.append(num)
    
    
    return round(tail_delay, 4), round(len(values_greater_than_average) / len(delay) * 100 if delay else 0, 3)

    
# 测试卡顿率（这里新定义卡顿率，就是求出每一个包的到达时间，一旦后一个包的到达时间超过前一个包的两倍，则计入卡顿数据包）
def calculate_congestion_rate():
    pass


# 测试分辨率
def extract_resolution(video_path):
    video = cv2.VideoCapture(video_path)
    # 获取视频的分辨率大小
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #print("视频分辨率：", size)
    video.release()
    return size

