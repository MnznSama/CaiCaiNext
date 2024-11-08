import ast
import glob
import json
import os
import subprocess
import sys
import importlib
from utils import log

class EventGroupMessage:
    def __init__(self, message):  # 直接接收 message 字典
        # 从字典中提取值并进行类型转换
        self.time = str(message.get("time", ""))
        self.self_id = str(message.get("self_id", ""))
        self.post_type = str(message.get("post_type", ""))
        self.message_type = str(message.get("message_type", ""))
        self.sub_type = str(message.get("sub_type", ""))
        self.message_id = str(message.get("message_id", ""))
        self.group_id = str(message.get("group_id", ""))
        self.user_id = str(message.get("user_id", ""))
        self.anonymous = str(message.get("anonymous", "")) or None  # 处理 None 值
        self.message = str(message.get("message", ""))
        self.raw_message = str(message.get("raw_message", ""))
        self.font = str(message.get("font", ""))
        self.sender = EventGroupSender(**{k: str(v) for k, v in message.get("sender", {}).items()}) if message.get("sender") else None
        self.message_seq = str(message.get("message_seq", "")) or None  # 处理 message_seq

    def __repr__(self):
        return (f"<GroupMessageEvent(time={self.time}, user_id={self.user_id}, "
                f"group_id={self.group_id}, message={self.message}, sender={self.sender})>")
class EventGroupSender:
    def __init__(self, user_id, nickname, card, role):
        self.user_id = str(user_id)
        self.nickname = str(nickname)
        self.card = str(card)
        self.role = str(role)

    def __repr__(self):
        return f"<Sender(user_id={self.user_id}, nickname={self.nickname}, card={self.card}, role={self.role})>"
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
    a = importlib.import_module("bot")
    upgroup = a.upgroup
    del sys.modules['bot']
    # 创建 EventGroupMessage 实例
    if message.get("message_type") == "group":
        try:
            message_event = EventGroupMessage(message)
            logger.info(
                f"GroupMessage|{message_event.group_id}->[{message_event.sender.role}]{message_event.sender.nickname}({message_event.sender.user_id}):{message_event.raw_message}"
            )
            args = [json.dumps(message)]
            plugin_files = glob.glob(os.path.join(".\\plugins", '*.py'))
            for file in plugin_files:
                # 使用 importlib 执行插件
                plugin = importlib.import_module("plugins."+os.path.splitext(os.path.basename(file))[0])
                print(plugin.info)
                info = PluginInfo(plugin.info)

                result = subprocess.run(['python', file] + args, capture_output=True, text=True)
                logger.debug(f"插件 {info.name} 输出: {result.stdout}")
                # 如果返回值为 1，跳出循环
                if result.returncode == 1:
                    logger.info(f'插件 {info.name} 对消息进行拦截')
                    logger.info(f"插件 {info.name} 输出: {result.stdout}")
                    break
                if result.stderr == " ":
                    logger.error(f"插件{info.name}抛出错误: {result.stderr}")
                    break

        except Exception as e:
            logger.error(f"Error In Group: {e}")
    elif message.get("message_type") == "private":
        try:
            message_event = EventGroupMessage(message)
            logger.info(
                f"GroupMessage|{message_event.sender.nickname}({message_event.sender.user_id})From({message_event.group_id}):{message_event.raw_message}"
            )
        except Exception as e:
            logger.error(f"Error In Private: {e}")
