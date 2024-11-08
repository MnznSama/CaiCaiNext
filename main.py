# -*- coding: utf-8 -*-
import bot
from utils import log

def main():
    logger.info("Log System Initialization")
    bot.run_websocket()

if __name__=="__main__":
    logger = log.get_logger()
    main()
