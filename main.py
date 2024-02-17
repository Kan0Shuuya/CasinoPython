import configparser
import time
from loguru import logger
from api import mainserver
logger.add(f"logs/logging_{str(time.time())}.log", level="INFO", format="{time} {level} {message}")
if __name__ == '__main__':
    logger.info("Starting...")
    config = configparser.ConfigParser()
    config.read("server.ini")
    mainserver.run(config["API"]["IP"], int(config["API"]["Port"]))