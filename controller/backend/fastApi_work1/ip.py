from typing import List

server_ips = [
    "192.168.199.200",
    "192.168.199.205",
    "192.168.199.210", "192.168.199.215",
    "192.168.199.220", "192.168.199.223"
]
# 服务ip
client_ips = [
    "192.168.199.201", "192.168.199.202",
    "192.168.199.203", "192.168.199.204",
    "192.168.199.206", "192.168.199.207", "192.168.199.208", "192.168.199.209",
    "192.168.199.211", "192.168.199.212", "192.168.199.213", "192.168.199.214",
    "192.168.199.216", "192.168.199.217", "192.168.199.218", "192.168.199.219",
    "192.168.199.221", "192.168.199.222", "192.168.199.224", "192.168.199.225"
]

servers = [
    {'hostname': '219.242.112.215', 'port': 6166, 'username': 'sinet', 'password': 'bjtungirc',
     'command': 'echo hello > a.txt'},
    {'hostname': '219.242.112.215', 'port': 6168, 'username': 'sinet', 'password': 'bjtungirc',
     'command': 'echo hello > a.txt'}
    # {'hostname': '219.242.112.215', 'port': 6172, 'username': 'sinet', 'password': 'bjtungirc',
    #  'command': '/path/to/172.sh'},
    # {'hostname': '219.242.112.215', 'port': 6164, 'username': 'sinet', 'password': 'bjtungirc',
    #  'command': '/path/to/172.sh'},
    # {'hostname': '219.242.112.215', 'port': 6174, 'username': 'sinet', 'password': 'bjtungirc',
    #  'command': '/path/to/172.sh'}
]
PROTOCOL_SINGLE = {
    "24": "encc",
    "22": "quic",
    "23": "webrtc",
    # 其他映射...
}

PROTOCOL_MULTIPATH = {
    "22": "quic",
    "23": "webrtc",
    "24": "ennc"
}

data_dict_fake = {
    "10.162.162.100": {
        "hostTerminal": "162",
        "amountOfConns": 0,
        "amountOfFileReqConns": 0
    },
    "10.164.164.100": {
        "hostTerminal": "164",
        "amountOfConns": 0,
        "amountOfFileReqConns": 0
    },
    "10.166.166.100": {
        "hostTerminal": "166",
        "amountOfConns": 0,
        "amountOfFileReqConns": 0
    },
    "10.168.168.100": {
        "hostTerminal": "168",
        "amountOfConns": 0,
        "amountOfFileReqConns": 0
    },
    "10.172.172.100": {
        "hostTerminal": "172",
        "amountOfConns": 0,
        "amountOfFileReqConns": 0
    }
}


def process_data_history(data) -> List[dict]:
    processed_data = []
    for item in data:
        formatted_time = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        processed_item = {
            "protocol": item.protocol,
            "resolution_width": item.resolution_width,
            "resolution_height": item.resolution_height,
            "tail_delay": item.tail_delay,
            "congestion_rate": item.congestion_rate,
            "state": item.state,
            "create_time": formatted_time
        }
        processed_data.append(processed_item)
    return processed_data


