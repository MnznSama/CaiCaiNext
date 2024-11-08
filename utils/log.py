# log.py
import configparser
import os
import logging
import colorlog
from datetime import datetime

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


def get_logger():
    # 创建或获取 logger
    logger = logging.getLogger('CaiCai')

    # 如果 logger 已经有处理器（handlers），则不重复配置
    if not logger.handlers:
        # 设置日志级别
        config = configparser.ConfigParser()
        config.read('.\data\config.ini',encoding='utf-8')
        debug = config['DEFAULT']['debug']
        if debug == 'True':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        # 日志文件创建
        currentTime = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
        filename = f'.\logs\\{currentTime}.log'
        if not os.path.exists(filename):
            os.close(os.open(filename, os.O_CREAT))

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s]%(filename)s->[%(levelname)s] %(message)s',
            datefmt='%y-%m-%d %H:%M:%S',
            log_colors=log_colors_config
        )
        console_handler.setFormatter(console_formatter)

        # 文件处理器
        file_handler = logging.FileHandler(filename=filename, mode='a', encoding='utf8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # 添加处理器到 logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
