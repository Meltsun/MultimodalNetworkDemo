import dpkt
import cv2


# 两个数据，时间戳，包id
def extract_id_timestamp(file_path):
    packets = {}
    with open(file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, dpkt.udp.UDP):
                    packets[ip.id] = timestamp
    return packets


# 测试尾时延和卡顿率
def calculate_tail_delay_and_congestion_rate(packets1, packets2):
    # 尾时延
    tail_delay = 0
    delay = []
    for packet1_id in packets1:
        if packet1_id in packets2:
            arrival_time1 = packets1[packet1_id]
            arrival_time2 = packets2[packet1_id]
            delay.append(abs(arrival_time2 - arrival_time1))
            tail_delay = max(tail_delay, abs(arrival_time2 - arrival_time1))
    if delay:
        average_value = sum(delay) / len(delay)
        #print(delay)

    # 求卡顿率（自定义）
    values_greater_than_average = []
    for num in delay:
        if num > average_value * 1:
            values_greater_than_average.append(num)
    return round(tail_delay, 4), round(len(values_greater_than_average) / len(delay) * 100 if delay else 0, 3)


# 测试分辨率
def extract_resolution(video_path):
    video = cv2.VideoCapture(video_path)
    # 获取视频的分辨率大小
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #print("视频分辨率：", size)
    video.release()
    return size

