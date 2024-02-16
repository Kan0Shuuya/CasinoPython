import configparser
import time

from loguru import logger

from api import mainserver

logger.info("Starting...")

if __name__ == '__main__':
    startTime = time.localtime(time.time())
    strStartTime = f"{startTime.tm_year}_{startTime.tm_mon}_{startTime.tm_mday}_{startTime.tm_hour}-{startTime.tm_min}-{startTime.tm_sec}"

    logger.add(f"logs/logging_{strStartTime}.log", level="INFO", format="{time} {level} {message}")

    config = configparser.ConfigParser()
    config.read("server.ini")
    SERVER_PORT = int(config['SOCKETConfig']['Port'])

    logger.debug(f"startTime: {startTime}")
    logger.debug(f"strStartTime: {strStartTime}")
    logger.debug(f"SERVER_PORT: {SERVER_PORT}")
    mainserver.run(port=SERVER_PORT)

    logger.debug(f"Start DB...")
