import logging
from pathlib import Path
from datetime import datetime

root = Path(__file__).parent.parent
LOG_FILE_PATH = root/"logs"
LOG_FILE_PATH.mkdir(exist_ok=True)

iperf_logger=logging.getLogger('iperf')
iperf_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE_PATH/'iperf.log',encoding='utf8',mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s > %(message)s',
        datefmt= '%Y-%m-%d %H:%M:%S'
    )
)
iperf_logger.addHandler(file_handler)

# -----------------------------------------------------
client_logger=logging.getLogger('schedule_client')
client_logger.setLevel(logging.DEBUG)

formatter=logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s > %(message)s',
    datefmt= '%Y-%m-%d %H:%M:%S'
)
        
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(LOG_FILE_PATH/datetime.now().strftime("%Y%m%d_%H-%M-%S_client.log"),encoding='utf8',mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
    
client_logger.addHandler(file_handler)
client_logger.addHandler(console_handler)