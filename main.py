import time
from loguru import logger
from api import main
if __name__ == '__main__':
    logger.add(f"logs/logging_{str(time.time())}.log", level="INFO", format="{time} {level} {message}")
    logger.info("Starting...")
    main.run("0.0.0.0", 7275)