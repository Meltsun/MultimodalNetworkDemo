import logging
from datetime import datetime
import os
from pathlib import Path
import toml
from pydantic import BaseModel,Field
from ipaddress import IPv4Address
import typing_extensions as typing

os.environ['PYTHONIOENCODING'] = 'utf-8'

__all__=['logger','switch_config']

root = Path(__file__).parent.parent

class SSHConfig(BaseModel):
    ip:IPv4Address
    port:int
    user:str
    password:str
class Bmv2Config(BaseModel):
    port:int
    register_indexes:typing.Tuple[int,int,int]=Field(description="路径123分别对应寄存器的哪些索引")
class SwitchConfig(BaseModel):
    ssh:SSHConfig
    bmv2:Bmv2Config
    name:str
class IperfConfig(BaseModel):
    interval:int
    port:int
class DDQNConfig(BaseModel):
    interval:float

CONFIG_PATH = root/"config.toml"
with CONFIG_PATH.open(encoding="utf8") as file:
    all_multipath_config = toml.load(file)['multipath']
    switch_config = [SwitchConfig(**i) for i in all_multipath_config['switch']]
    iperf_config = IperfConfig(**all_multipath_config['iperf'])
    ddqn_config = DDQNConfig(**all_multipath_config['ddqn'])

LOG_FILE_PATH = root/"logs"/datetime.now().strftime("%Y%m%d_%H-%M-%S.log")
LOG_FILE_PATH.parent.mkdir(exist_ok=True)

logger=logging.getLogger('schedule')
logger.setLevel(logging.DEBUG)

formatter=logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s > %(message)s',
    datefmt= '%Y-%m-%d %H:%M:%S'
)
        
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(LOG_FILE_PATH,encoding='utf8',mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
    
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')
