## 使用说明

测试代码放在180服务器上

packet_capture.py为抓取客户端和服务器网卡数据包程序，需修改内部参数duration来指定网卡监听时间。

packet_handle.py为处理数据包程序。

直接在/home/sinet/下运行`./start.sh`即可启动程序。

测试指标说明：
尾时延：计算出所有视频流数据包的传输时延，并按时延大小从小到大排序，取最后1%的数据包时延，求出这1%数据包时延
的平均值作为尾时延。
卡顿率（目前无法按普通定义计算出，这里是自定义的卡顿率）：时延大于平均时延1.2倍（这个1.2是凑的）数据包比例。
分辨率：调用Python的opencv库解析源视频获得。

尾时延和卡顿率对应packet_handle.py中的calculate_tail_delay_and_congestion_rate函数
分辨率对应packet_handle.py中的extract_resolution函数


开启webrtc服务器脚本：在180服务器上，直接在/home/sinet/下运行`./start_webrtc.sh`即可开启webrtc服务器。
