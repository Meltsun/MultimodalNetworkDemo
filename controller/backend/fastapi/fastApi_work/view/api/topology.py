from fastapi import APIRouter
from database.models import Topology_nodes, Topology_link, Topology_edges, Alltask, ipv4_table
from pydantic import BaseModel, validator
from typing import Dict,List,Any

api_topology = APIRouter()



@api_topology.get("/")
async def getAlltopology()-> Dict[str, Any]:# 
    topology = await Topology_nodes.all()
    edges = await Topology_edges.all()
    return {
        "topology": topology,
        "edges": edges
    }


@api_topology.post("/node")
async def getnode(id: int) -> List[Topology_nodes]:
    node = await Topology_nodes.filter(id=id)
    return node


class nodeIn(BaseModel):
    id: int
    label: str
    type: str
    ip: str
    package_count: int
    interface: Dict[str, int]

    # @validator("interface")
    # def validate_type(cls, value):
    #     assert value.isalpha(), "无效的字符串，格式应类似为10.10.1.2"
    #     return value


@api_topology.post("/add/node")
async def addnode(node: nodeIn) -> Topology_nodes:
    node_db = await Topology_nodes.create(id=node.id, label=node.label, type=node.type, ip=node.ip,
                                        package_count=node.package_count,
                                        interface=node.interface)
    print(node_db)
    # 插入到数据库中
    return node_db


@api_topology.get("/task")
async def getalltasks() -> List[Alltask]:
    tasks = await  Alltask.all()
    return tasks


# @api_topology.post("/link")
# async def getlink(node1: int, node2: int):
#     link = await Topology_link.filter(node1=node1, node2=node2).values("id", "delay", "bandwidth", "lost")
#     print(link)
#     return link


@api_topology.post("/table")
async def send_ipv4_table(switch_id: int, dst: str, mask: str, port: int, next_hop_mac: str):
    return {
        "目前返回失败"
    }
