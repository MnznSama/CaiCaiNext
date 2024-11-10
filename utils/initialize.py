import configparser
import glob
import importlib
import os
import sys

from importlib_resources import files

from utils import log

def init(DATA: dict, DATA_DIRS: tuple):
    print("Initializing...")
    # 遍历目录列表
    for dir_name in DATA_DIRS:
        # 检查目录是否存在
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
            print(f"Dir {dir_name} Created.")
    # 遍历文件列表
    file_path = os.path.join("data", "config.ini")
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    # 遍历 DATA 中的每个 section 和 key
    for files in DATA:
        for section in DATA[files]:
            # 如果节不存在，添加该节
            if section not in config.sections():
                config.add_section(section)
            # 遍历每个 key 和 value
            for key, value in DATA[files][section].items():
                # 如果 key 不存在，写入对应的值
                if key not in config[section]:
                    config.set(section, key, str(value))
                # 将更新后的配置写回文件
    with open(file_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

    logger = log.get_logger('Init')
    logger.info("Initializing...")
    logger.info("Log System Initialized.")
    logger.debug("Debug Mode Enabled.")
    # 加载插件列表
    plugin_files = glob.glob(os.path.join(".\\plugins", '*.py'))
    # 初始化插件
    for file in plugin_files:
        file = os.path.splitext(os.path.basename(file))[0]
        try:
            plugin = importlib.import_module("plugins." + file)
            info = plugin.info
            if not os.path.isdir(os.path.join("data", "plugins", info['name'])):
                os.makedirs(os.path.join("data", "plugins", info['name']))
            config = configparser.ConfigParser()
            config.read('.\data\config.ini', encoding='utf-8')
            if config['PLUGIN'].getboolean(info['name']) != True:
                config['PLUGIN'][info['name']] = 'False'
                with open(file_path, 'w', encoding='utf-8') as configfile:
                    config.write(configfile)
                logger.info(f"Plugin \'{info['name']}\' Is Disabled.")
            else :
                result = plugin.init()
                if result == 1:
                    logger.info(f"Plugin \'{info['name']}\' Initialized.")
                else:
                    logger.warning(f"There Are Something Wrong In Plugin \'{info['name']}\'.")
            del sys.modules["plugins." + file]
        except Exception as e:
            logger.error(f"Error In Plugin File \'{file}\' Init : {e}")
    return 0