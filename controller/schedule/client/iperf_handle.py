import subprocess
from io import BufferedReader
import os
from typing_extensions import List,cast,TypeAlias,Optional,Never,TypeVar,Literal
from dataclasses import dataclass,field
import re
import datetime
import time
import sys
import logging
from pathlib import Path
import traceback

Mbps:TypeAlias = float
NumOfPackets:TypeAlias = int


@dataclass
class NetworkState:
    bandwidth: Optional[Mbps]= field(default=None)
    lost: Optional[NumOfPackets]= field(default=None)
    total: Optional[NumOfPackets]= field(default=None)
    out_of_order: Optional[NumOfPackets]= field(default=None)
    time:datetime.datetime=field(default_factory=datetime.datetime.now)

class IperfHandle:
    """
    在本地开启一个iperf客户端，接收运行时输出，并进行格式化。\n
    需要python>=3.12才能在windows上运行，否则只能运行在linux上。\n
    初始化时请传入参数列表，类似['iperf','-s','-i','1','-p','5000','-u','-e']\n
    请使用close关闭cli和ssh连接或者直接作为上下文使用。
    """
    stdout:BufferedReader
    logger:logging.Logger
    iperf_logger:logging.Logger
    def __init__(self,cmd:List,logger:logging.Logger,iperf_logger:logging.Logger) -> None:
        cmd = [str(i) for i in cmd]
        self.logger.debug("发送命令"+' '.join(cmd))
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert isinstance(self.process.stdout,BufferedReader)
        self.stdout = self.process.stdout
        for _ in range(5):
            self.stdout.readline()
        if sys.version_info >= (3, 12) or sys.platform.startswith('linux'):
            os.set_blocking(self.stdout.fileno(),False) # type: ignore
        else:
            raise Exception("需要运行在python>3.12或linux平台上")
    
    def close(self) -> None:
        self.process.terminate()
        self.process.wait()
        self.logger.warn("iperf handle已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def phase_line(self,line:str) -> Optional[NetworkState]:
        splited = re.split(r'[/\s]+',line)[:-1]
        self.iperf_logger.info(line)
        state = NetworkState()
        def unknown_unit(name:str,unit:str)->Never:
            raise Exception(f"{name} 的未知单位：{unit}")
        try:
            if len(splited)==8 and splited[7]=="out-of-order": #乱序行
                state.out_of_order = NumOfPackets(splited[4])
            elif len(splited)==22 or len(splited)==21 and splited[20]=='pps':      #常规行
                if splited[7] == "Mbits" and splited[8]=="sec":
                    state.bandwidth = Mbps(splited[6])
                elif splited[7] == "Kbits" and splited[8]=="sec":
                    state.bandwidth = Mbps(float(splited[6])/1000)
                elif splited[7] == "bits" and splited[8]=="sec":
                    state.bandwidth = Mbps(float(splited[6])/1000000)
                else:
                    unknown_unit("bandwith",splited[7])
                #lost
                state.lost=NumOfPackets(splited[11])
                #total
                state.total=NumOfPackets(splited[12])
            else :
                self.logger.info(f"未知输出，未进行解析：{line}")
                return None
            return state
        except Exception as e:
            self.logger.error(f"iperf解析错误: {line}\n错误详情:{e}\n{traceback.format_exc()}")
    
    def get_network_states_block(self) -> List[NetworkState]:
        states=self.get_network_states()
        while len(states)==0:
            time.sleep(0.1)
            states=self.get_network_states()
        return states

    def get_network_states(self,*,phase:bool=True) -> List[NetworkState]:
        """
        获取实例化或上次调用此方法后的所有输出，并解析为NetworkState。
        如果把phase置为False，则不会尝试进行解析，输出空列表；可以用于清空现有输出并节省性能
        """
        states:List[NetworkState] = []
        while True:
            #如果缓冲区可读，会一直读到/n；如果不可读，会返回None。如果iperf输出了一些东西但没输出回车，可能会引起阻塞。应该没事。
            line=self.stdout.readline()
            if not line:
                break
            if phase:
                line = line.decode()
                state=self.phase_line(line)
                if state:
                    states.append(state)
                else:
                    pass
        return states

    def monitor_for_seconds(self,duration:int) -> List[NetworkState]:
        """
        获取这段时间的网络状态
        """
        self.get_network_states(phase=False)
        time.sleep(duration)
        return self.get_network_states()