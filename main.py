# -*- coding: utf-8 -*-
import os

from utils import log

file_data = {
    "data\config.ini": '[DEFAULT]\n'
                       'author=\n'
                       'upgroup=\n'
                       'debug=False\n'
                       'startmsg=Start\n\n'
                       '[WS]\n'
                       'url=127.0.0.1\nport=1145',
}
dirs = ("data\groups",
        "data\plugins",
        "logs",
        "plugins")


def main():
    initialize()
    import bot
    bot.run_websocket()

def initialize():
    print("Initializing...")
    # 遍历目录列表
    for dir_name in dirs:
        # 检查目录是否存在
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
            print(f"Dir {dir_name} Created.")
    # 遍历文件列表
    for file_name, content in file_data.items():
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                file.write(content)
            print(f"File {file_name} Created.")
    logger = log.get_logger()
    logger.info("Log System Initialized.")
    logger.debug("Debug Mode Enabled.")
    return 0


if __name__=="__main__":
    main()
