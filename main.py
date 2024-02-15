import logging
import time
import configparser

if __name__ == '__main__':
    startTime = time.localtime(time.time())
    strStartTime = f"{startTime.tm_year}_{startTime.tm_mon}_{startTime.tm_mday}_{startTime.tm_hour}-{startTime.tm_min}-{startTime.tm_sec}"
    logging.basicConfig(level=logging.INFO, filename=f"logs/logging_{strStartTime}.log", filemode="w")
    config = configparser.ConfigParser()
    logging.info(f"Initialization date: {strStartTime}")
    logging.info(f"Start SOCKET")
    config.read("server.ini")
    logging.info(f"Port:{config['SOCKETConfig']['Port']}")



