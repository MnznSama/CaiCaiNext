import glob
import importlib
import json
import os
import sys

from utils import log
from utils.operate import get_plugin_status


def main(message):
    logger = log.get_logger("Request")
    request_type = message.get("request_type")
    if request_type == "friend":
        logger.info(f"新的好友请求 | {message.get('user_id')} 验证消息: {message.get('comment')} - {message.get('flag')}")
        task = 1
    elif request_type == "group":
        logger.info(f"新的群聊{message.get('sub_type')}请求 | {message.get('user_id')} 群号: {message.get('group_id')} : {message.get('comment')} - {message.get('flag')}")
        task = 2

        # 加载插件列表
    plugin_files = glob.glob(os.path.join("plugins", '*.py'))
    plugins = {}
    i = 0
    for file in plugin_files:
        _file = os.path.splitext(os.path.basename(file))[0]
        plugin_module = importlib.import_module("plugins." + _file)
        info = plugin_module.info
        plugins[i] = info
        plugins[i]['file'] = _file
        plugins[i]['status'] = get_plugin_status(plugins[i]['name'])
        i += 1
    for file in plugin_files:
        # 使用 importlib 执行插件
        try:
            for index in plugins:
                plugin_module = importlib.import_module("plugins." + plugins[index]['file'])
                if plugins[index]['status'] == 'True':
                    result = 0
                    if task == 1:
                        result = plugin_module.group_message(json.dumps(message))
                    elif task == 2:
                        result = plugin_module.private_message(json.dumps(message))
                    if result == 1:
                        logger.info(f"Plugin \'{plugins[index]['info']['name']}\' Intercepted Message.")
                        break
            del sys.modules["plugins." + os.path.splitext(os.path.basename(file))[0]]
        except Exception as e:
            logger.error(f"Error In Plugin:{e}")
