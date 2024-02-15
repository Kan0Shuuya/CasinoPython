from loguru import logger
logger.info("Starting...")

import time
import configparser
import web_server_test as web_server

if __name__ == '__main__':
    startTime = time.localtime(time.time())
    strStartTime = f"{startTime.tm_year}_{startTime.tm_mon}_{startTime.tm_mday}_{startTime.tm_hour}-{startTime.tm_min}-{startTime.tm_sec}"

    logger.add(f"logs/logging_{strStartTime}.log", level="INFO", format="{time} {level} {message}")

    config = configparser.ConfigParser()
    config.read("server.ini")
    SERVER_PORT = int(config['SOCKETConfig']['Port'])
    
    web_server.start_server(SERVER_PORT)


