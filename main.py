import time
import configparser
from loguru import logger

if __name__ == '__main__':
    startTime = time.localtime(time.time())
    strStartTime = f"{startTime.tm_year}_{startTime.tm_mon}_{startTime.tm_mday}_{startTime.tm_hour}-{startTime.tm_min}-{startTime.tm_sec}"

    logger.info(f"Initialization date: {strStartTime}")
    logger.add(f"logs/logging_{strStartTime}.log", level="INFO", format="{time} {level} {message}")

    config = configparser.ConfigParser()
    config.read("server.ini")

    logger.info(f"Start SOCKET")
    logger.info(f"Port:{config['SOCKETConfig']['Port']}")


