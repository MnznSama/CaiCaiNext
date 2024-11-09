import glob
import json
import os
import importlib
import sys

from utils import log
from utils.events import GroupMessage, PrivateMessage


class PluginInfo:
    def __init__(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                # 如果值是字典，递归调用 PluginInfo 类（处理嵌套字典）
                if isinstance(value, dict):
                    value = PluginInfo(value)
                setattr(self, key, value)
        else:
            raise ValueError("Input data must be a dictionary")

    def __repr__(self):
        return f"PluginInfo({self.__dict__})"


def main(message):
    logger = log.get_logger()
    # 加载插件列表
    plugin_files = glob.glob(os.path.join(".\\plugins", '*.py'))
    # 创建 EventGroupMessage 实例
    if message.get("message_type") == "group":
        try:
            message_event = GroupMessage(message)
            logger.info(
                f"GroupMessage|{message_event.group_id}->[{message_event.sender.role}]{message_event.sender.nickname}({message_event.sender.user_id}):{message_event.raw_message}(message_id:{message_event.message_id})"
            )
            for file in plugin_files:
                # 使用 importlib 执行插件
                try:
                    plugin = importlib.import_module("plugins." + os.path.splitext(os.path.basename(file))[0])
                    logger.debug(plugin.info)
                    info = PluginInfo(plugin.info)
                    result = plugin.group_message(json.dumps(message))
                    del sys.modules["plugins." + os.path.splitext(os.path.basename(file))[0]]
                    if result == 1:
                        logger.info(f"Plugin \'{info.name}\' Intercepted Message.")
                        break
                except Exception as e:
                    logger.error(f"Error In Plugin:{e}")
        except Exception as e:
            logger.error(f"Error In Group: {e}")



    elif message.get("message_type") == "private":
        try:
            message_event = PrivateMessage(message)
            logger.info(
                f"PrivateMessage|{message_event.sender.nickname}({message_event.sender.user_id}):{message_event.raw_message}(message_id:{message_event.message_id})"
            )
            for file in plugin_files:
                # 使用 importlib 执行插件
                try:
                    plugin = importlib.import_module("plugins." + os.path.splitext(os.path.basename(file))[0])
                    logger.debug(plugin.info)
                    info = PluginInfo(plugin.info)
                    result = plugin.private_message(json.dumps(message))
                    del sys.modules["plugins." + os.path.splitext(os.path.basename(file))[0]]
                    if result == 1:
                        logger.info(f"Plugin \'{info.name}\' Intercepted Message.")
                        break
                except Exception as e:
                    logger.error(f"Error In Plugin:{e}")

        except Exception as e:
            logger.error(f"Error In Private: {e}")
