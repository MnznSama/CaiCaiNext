import configparser
import io
import os
import logging
import colorlog
from datetime import datetime
import sys

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

log_output = io.StringIO()


def get_logger(name=None):
    # 创建或获取 logger
    if not name:
        name = 'NapDog'
    logger = logging.getLogger(name)

    # 如果 logger 已经有处理器（handlers），则不重复配置
    if not logger.handlers:
        # 设置日志级别
        config = configparser.ConfigParser()
        config_path = os.path.join(os.getcwd(), 'data', 'config.ini')
        config.read(config_path, encoding='utf-8')
        debug = config['NapDog']['debug']
        if debug == 'True':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        # 日志文件创建
        currentTime = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        filename = os.path.join(log_dir, f'{currentTime}.log')
        if not os.path.exists(filename):
            os.close(os.open(filename, os.O_CREAT))

        # 控制台处理器，带颜色
        console_handler = logging.StreamHandler(sys.stdout)  # 输出到控制台
        console_formatter = colorlog.ColoredFormatter(
            fmt=f'%(log_color)s[%(asctime)s] [{name}] %(filename)s [%(levelname)s] %(message)s',
            datefmt='%y-%m-%d %H:%M:%S',
            log_colors=log_colors_config
        )
        console_handler.setFormatter(console_formatter)

        # 文件处理器，不带颜色
        file_handler = logging.FileHandler(filename=filename, mode='a', encoding='utf8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            fmt=f'[%(asctime)s.%(msecs)03d] [{name}] %(filename)s %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # StringIO 处理器，不带颜色
        memory_handler = logging.StreamHandler(log_output)
        memory_handler.setLevel(logging.INFO)
        memory_format = logging.Formatter(
            fmt=f'[%(asctime)s] [{name}] [%(levelname)s] %(message)s',
            datefmt='%y-%m-%d %H:%M:%S'
        )
        memory_handler.setFormatter(memory_format)  # 使用没有颜色的 formatter

        # 添加处理器到 logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(memory_handler)

    return logger
def get_log():
    return log_output.getvalue()



