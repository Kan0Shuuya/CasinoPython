import configparser
import time
from loguru import logger
from api import main
if __name__ == '__main__':
    logger.add(f"logs/logging_{str(time.time())}.log", level="INFO", format="{time} {level} {message}")
    logger.info("Starting...")
    config = configparser.ConfigParser()
    config.read("server.ini")
    main.run(config["API"]["IP"], int(config["API"]["Port"]))