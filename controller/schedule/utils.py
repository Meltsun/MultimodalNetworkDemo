import logging
from datetime import datetime
from pathlib import Path

__all__=['logger']

root = Path(__file__).parent
LOG_PATH = root/"log"/datetime.now().strftime("%Y%m%d_%H-%M-%S.log")

logger=logging.getLogger('schedule')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_PATH,encoding='utf8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s > %(message)s',
        datefmt= '%Y-%m-%d %H:%M:%S'
    )
)
logger.addHandler(file_handler)
logger.addHandler(console_handler)