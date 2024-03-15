from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `alltask` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `client_host_id` INT NOT NULL UNIQUE COMMENT '客户端id',
    `client_port` VARCHAR(32) NOT NULL UNIQUE COMMENT '端口',
    `server_host_id` INT NOT NULL UNIQUE COMMENT '服务端id',
    `server_port` VARCHAR(32) NOT NULL UNIQUE COMMENT '服务端端口',
    `enable` BOOL NOT NULL  COMMENT '是否启用了任务，0表示未启用，1表示启用'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `topology_edges` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `edges` JSON NOT NULL  COMMENT '从某个节点到某个节点'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `topology_link` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `delay` INT NOT NULL  COMMENT '延迟',
    `bandwidth` INT NOT NULL  COMMENT '带宽',
    `lost` INT NOT NULL  COMMENT '丢包数',
    `node1` VARCHAR(32) NOT NULL  COMMENT '链路节点1',
    `node2` VARCHAR(32) NOT NULL  COMMENT '链路节点2'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `topology_nodes` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `label` VARCHAR(32) NOT NULL UNIQUE COMMENT '拓扑节点名称',
    `type` VARCHAR(32) NOT NULL  COMMENT '拓扑类型',
    `ip` VARCHAR(32) NOT NULL  COMMENT 'ip地址',
    `package_count` INT NOT NULL  COMMENT '处理包的数量',
    `interface` JSON NOT NULL  COMMENT '接口连接'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `task_information` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `task_id` INT NOT NULL UNIQUE COMMENT '任务id',
    `time` INT NOT NULL  COMMENT '处理时间',
    `delay` INT NOT NULL  COMMENT '任务延迟'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
