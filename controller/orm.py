from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime
from pathlib import Path

sqlite_file_name = Path(__file__).parent/"database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

class NodeType(Enum):
    HOST = "host"
    SWITCH = "switch"

class Node(SQLModel, table=True):
    """
    结点信息。包括终端和交换机。
    此表是手动根据网络配置填写的。
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    type: NodeType 
    ip:Optional[str] = Field(default=None,description="主机的ip地址, 由'.'分割的四个数，类似'1.1.1.1';交换机的此字段为空")
    console_ip:str = Field(description="用于管理的内网ip地址和端口，例如192.168.199.3:22")

class Link(SQLModel, table=True):
    """
    此表是手动根据配置的网络填写的。
    连接有方向（因为int）。两个结点之间需要添加来回两个连接。
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    node_id_1:int
    interface_id_1:int
    node_id_2:int
    interface_id_2:int

class LinkState(SQLModel, table=True):
    """
    由int程序写入的测试信息
    schedule程序读取
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    link_id:int
    create_time:datetime
    delay:Optional[int]=Field(default=None)
    rate:Optional[int]=Field(default=None)
    lost:Optional[float]=Field(default=None)

#网卡
class Interface(SQLModel, table=True):
    """
    网卡信息，也包括网卡对应的bmv2端口号。
    此表是手动根据网络配置填写的。
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name:str
    node_id:int
    bmv2_port:Optional[int] = Field(default=-1,description="交换机网卡对应的bmv2 port;主机网卡置为-1或None")

class Task(SQLModel, table=True):
    """
    测试任务
    此表暂未确定，需要进一步讨论；
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    src_host_id:int
    src_port:int
    dst_host_id:int
    dst_port:int
    enable:bool
    message:str

class TaskResult(SQLModel, table=True):
    """
    测试任务的结果
    此表暂未确定，需要进一步讨论；
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id:int
    create_time:datetime
    delay:Optional[int] = Field(default=None,description="时延")
    rate:Optional[int] = Field(default=None,description="速率")
    loss:Optional[float] = Field(default=None,description="丢包率")
    disorder:Optional[float] = Field(default=None,description="乱序率")

def _create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    _create_db_and_tables()