from typing import Generator, Optional
from enum import Enum
from sqlmodel import Field, SQLModel, create_engine,Session
from datetime import datetime

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

class NodeType(Enum):
    HOST = "host"
    SWITCH = "switch"

#终端和交换机
class Node(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    type: NodeType 
    ip:Optional[str] = Field(default=None,description="主机的ip地址, 由'.'分割的四个数，类似'1.1.1.1';交换机的此字段为空")
    console_ip:str = Field(description="ssh(192.168.199.xxx)")

#终端和交换机
class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    node_id_1:int
    interface_id_1:int=Field(description="两个id按照字典序排序")
    node_id_2:int
    interface_id_2:int=Field(description="两个id按照字典序排序")
    delay:Optional[int]=Field(default=None)
    rate:Optional[int]=Field(default=None)
    lost:Optional[float]=Field(default=None)

#网卡
class Interface(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name:str
    node_id:int
    bmv2_port:Optional[int] = Field(default=-1,description="交换机网卡对应的bmv2 port;主机网卡置为-1")

#测试任务；暂未确定，需要进一步讨论；
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    src_host_id:int
    src_port:int
    dst_host_id:int
    dst_port:int
    enable:bool

class TaskResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id:int
    time:datetime
    delay:Optional[int] = Field(default=None,description="时延")
    rate:Optional[int] = Field(default=None,description="速率")
    loss:Optional[float] = Field(default=None,description="丢包率")
    disorder:Optional[float] = Field(default=None,description="乱序率")

def _create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session,None,None]:
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    _create_db_and_tables()