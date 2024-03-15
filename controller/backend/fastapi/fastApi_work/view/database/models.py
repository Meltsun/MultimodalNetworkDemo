from tortoise.fields import BooleanField
from tortoise.models import Model
from tortoise import fields


class Topology_nodes(Model):
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=32, unique=True, description="拓扑节点名称")
    type = fields.CharField(max_length=32, description="拓扑类型")
    ip = fields.CharField(max_length=32, description="ip地址")
    package_count = fields.IntField(max_length=32, description="处理包的数量")
    interface = fields.JSONField(description="接口连接")


class Topology_edges(Model):
    id = fields.IntField(pk=True)
    edges = fields.JSONField(description="从某个节点到某个节点")


class Topology_link(Model):
    id = fields.IntField(pk=True)
    delay = fields.IntField(description="延迟")
    bandwidth = fields.IntField(description="带宽")
    lost = fields.IntField(description="丢包数")
    node1 = fields.CharField(description="链路节点1", max_length=32)
    node2 = fields.CharField(description="链路节点2", max_length=32)


class Alltask(Model):
    id = fields.IntField(pk=True)
    client_host_id = fields.IntField(unique=True, description="客户端id")
    client_port = fields.CharField(max_length=32, unique=True, description="端口")
    server_host_id = fields.IntField(unique=True, description="服务端id")
    server_port = fields.CharField(max_length=32, unique=True, description="服务端端口")
    enable = fields.BooleanField(description="是否启用了任务，0表示未启用，1表示启用")


class task_information(Model):
    id = fields.IntField(pk=True)
    task_id = fields.IntField(unique=True, description="任务id")
    time = fields.IntField(description="处理时间")
    delay = fields.IntField(description="任务延迟")


class ipv4_table(Model):
    id = fields.IntField(pk=True)
    switch_id = fields.IntField(unique=True, description="交换机id")
    destination_address = fields.CharField(max_length=32, description="目的地址", unique=True)
    mask_id = fields.CharField(max_length=32, description="子网掩码")
    port = fields.IntField(unique=True, description="端口地址")
    next_hop_mac = fields.CharField(unique=True, description="物理地址", max_length=32)


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)
