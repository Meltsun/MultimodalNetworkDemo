import logging
from datetime import datetime
import os
from pathlib import Path
import toml

__all__=['logger','config']

root = Path(__file__).parent
CONFIG_PATH = root/"config.toml"
LOG_FILE_PATH = root/"logs"/datetime.now().strftime("%Y%m%d_%H-%M-%S.log")

config = toml.load(CONFIG_PATH)
LOG_FILE_PATH.parent.mkdir(exist_ok=True)

logger=logging.getLogger('schedule')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE_PATH,encoding='utf8',mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s > %(message)s',
        datefmt= '%Y-%m-%d %H:%M:%S'
    )
)
logger.addHandler(file_handler)
logger.addHandler(console_handler)