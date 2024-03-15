from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `ipv4_table` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `switch_id` INT NOT NULL UNIQUE COMMENT '交换机id',
    `destination_address` VARCHAR(32) NOT NULL UNIQUE COMMENT '目的地址',
    `mask_id` INT NOT NULL  COMMENT '子网掩码',
    `port` INT NOT NULL UNIQUE COMMENT '端口地址',
    `next_hop_mac` VARCHAR(32) NOT NULL UNIQUE COMMENT '物理地址'
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `ipv4_table`;"""
