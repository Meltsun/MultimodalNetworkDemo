from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `ipv4_table` MODIFY COLUMN `mask_id` VARCHAR(32) NOT NULL  COMMENT '子网掩码';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `ipv4_table` MODIFY COLUMN `mask_id` INT NOT NULL  COMMENT '子网掩码';"""
