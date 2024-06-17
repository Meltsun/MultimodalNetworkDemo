import time
from typing import Optional
from enum import Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel, create_engine, Session
from datetime import datetime

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


class UserBased(SQLModel):
    username: str = Field(index=True, unique=True)
    password: str = Field(default=None, max_length=255)


class User(UserBased, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserLogin(UserBased):
    pass


class NodeType(Enum):
    HOST = "host"
    SWITCH = "switch"


class NoneBased(SQLModel):
    name: str
    type: NodeType


class Node(NoneBased, table=True):
    """
    结点信息。包括终端和交换机。
    此表是手动根据网络配置填写的。
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: Optional[str] = Field(default=None,
                              description="主机的ip地址, 由'.'分割的四个数，类似'1.1.1.1';交换机的此字段为空")
    console_ip: str = Field(description="用于管理的内网ip地址和端口，例如192.168.199.3:22")


class NodeRead(NoneBased):
    id: int
    ip: Optional[str] = Field(default=None,
                              description="主机的ip地址, 由'.'分割的四个数，类似'1.1.1.1';交换机的此字段为空")


class NodeUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[NodeType] = None
    ip: Optional[str] = None
    console_ip: str = None


class NodeCreate(NoneBased):
    ip: Optional[str] = Field(default=None,
                              description="主机的ip地址, 由'.'分割的四个数，类似'1.1.1.1';交换机的此字段为空")
    console_ip: str = Field(description="用于管理的内网ip地址和端口，例如192.168.199.3:22")


class LinkBased(SQLModel):
    node_id_1: int
    interface_id_1: int
    node_id_2: int
    interface_id_2: int


class Link(LinkBased, table=True):
    """
    此表是手动根据配置的网络填写的。
    连接有方向（因为int）。两个结点之间需要添加来回两个连接。
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class LinkIntCreate(SQLModel):
    node_id_1: int
    node_id_2: int


class LinkCreate(LinkBased):
    pass


class LinkStateBased(SQLModel):
    create_time: datetime
    delay: Optional[int] = Field(default=None)
    rate: Optional[float] = Field(default=None)
    lost: Optional[float] = Field(default=None)


class LinkState(LinkStateBased, table=True):
    """
    由int程序写入的测试信息
    schedule程序读取
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    link_id: int
    node_id_1: Optional[int] = Field(default=None)
    node_id_2: Optional[int] = Field(default=None)


class LinkStateCreat(LinkStateBased):
    node_id_1: Optional[int] = Field(default=None)
    node_id_2: Optional[int] = Field(default=None)


# 网卡
class Interface(SQLModel, table=True):
    """
    网卡信息，也包括网卡对应的bmv2端口号。
    此表是手动根据网络配置填写的。
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    node_id: int
    bmv2_port: Optional[int] = Field(default=-1, description="交换机网卡对应的bmv2 port;主机网卡置为-1或None")


class Task(SQLModel, table=True):
    """
    测试任务
    此表暂未确定，需要进一步讨论；
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    src_host_id: int
    src_port: int
    dst_host_id: int
    dst_port: int
    enable: bool
    message: str


class TaskResult(SQLModel, table=True):
    """
    测试任务的结果
    此表暂未确定，需要进一步讨论；
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int
    create_time: datetime
    delay: Optional[int] = Field(default=None, description="时延")
    rate: Optional[int] = Field(default=None, description="速率")
    loss: Optional[float] = Field(default=None, description="丢包率")
    disorder: Optional[float] = Field(default=None, description="乱序率")


class NetworkPerformanceBased(SQLModel):
    protocol: str = Field(default="http", description="协议")
    congestion_rate: Optional[float] = Field(default=None, description="卡顿率")
    tail_delay: Optional[float] = Field(default=None, description="时延")
    resolution_height: Optional[int] = Field(default=None, description="清晰度长")
    resolution_width: Optional[int] = Field(default=None, description="清晰度宽")
    state: str = Field(default="场景一", description="状态表示")
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间")


class NetworkPerformance(NetworkPerformanceBased, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class NetworkPerformanceCreate(SQLModel):
    protocol: str = Field(default="http", description="协议")
    congestion_rate: Optional[float] = Field(default=None, description="卡顿率")
    tail_delay: Optional[float] = Field(default=None, description="时延")
    resolution_height: Optional[int] = Field(default=None, description="清晰度长")
    resolution_width: Optional[int] = Field(default=None, description="清晰度宽")


def _create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def create_linkstate():
    linkstate = LinkState(link_id=5, create_time=datetime.now(), delay=1, rate=1, loss=100)
    with Session(engine) as session:
        session.add(linkstate)
        session.commit()


if __name__ == "__main__":
    # create_linkstate()
    _create_db_and_tables()
