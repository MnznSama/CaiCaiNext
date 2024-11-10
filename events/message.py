import configparser
import glob
import json
import os
import importlib
import sys

from utils import log
from utils.events import GroupMessage, PrivateMessage
from utils.operate import get_plugin_status, send_group_message, is_plugin_exist

file_path = os.path.join("data", "config.ini")
config = configparser.ConfigParser()
config.read(file_path, encoding='utf-8')

def main(message):
    logger = log.get_logger("Message")

    task = 0
    if message.get("message_type") == "group":
        message_event = GroupMessage(message)
        logger.info(
            f"收到群消息 | {message_event.group_id}->[{message_event.sender.role}]{message_event.sender.nickname}({message_event.sender.user_id}):{message_event.raw_message}(message_id:{message_event.message_id})"
        )
        task = 1
    elif message.get("message_type") == "private":
        message_event = PrivateMessage(message)
        logger.info(
            f"收到私聊消息 | {message_event.sender.nickname}({message_event.sender.user_id}):{message_event.raw_message}(message_id:{message_event.message_id})"
        )
        task = 2

    # 加载插件列表
    plugin_files = glob.glob(os.path.join("plugins", '*.py'))
    plugins = {}
    i = 0
    for file in plugin_files:
        _file = os.path.splitext(os.path.basename(file))[0]
        plugin_module = importlib.import_module("plugins." + _file)
        info =  plugin_module.info
        plugins[i] = info
        plugins[i]['file'] = _file
        plugins[i]['status'] = get_plugin_status(plugins[i]['name'])
        i += 1

    if message_event.sender.user_id == int(config['NapDog']['author']):

        if message_event.raw_message.startswith(".ls"):
            text = ""
            for index in plugins:
                logger.debug(plugins[index])
                text += f"插件名称:{plugins[index]['name']},插件状态:{plugins[index]['status']},描述:{plugins[index]['description']}\n"
            send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]{text}")

        if message_event.raw_message.startswith(".status"):
            text = message_event.raw_message.split(" ")
            if len(text) == 1:
                send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]请输入插件名")
            elif len(text) == 2:
                _plugin = text[1]
                if is_plugin_exist(_plugin):
                    send_group_message(message_event.group_id,
                                       f"[CQ:reply,id={message_event.message_id}]{_plugin}状态为{config['PLUGIN'][_plugin]}")
                else:
                    send_group_message(message_event.group_id, f"[CQ:reply,id={message_event.message_id}]插件不存在")
            else:
                send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]参数错误")

        if message_event.raw_message.startswith(".on"):
            text = message_event.raw_message.split(" ")
            if len(text) == 1:
                send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]请输入插件名")
            elif len(text) == 2:
                _plugin = text[1]
                if is_plugin_exist(_plugin):
                    config['PLUGIN'][_plugin] = 'True'
                    with open(file_path, 'w', encoding='utf-8') as configfile:
                        config.write(configfile)
                    send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]插件{_plugin}已启用")
                else:
                    send_group_message(message_event.group_id, f"[CQ:reply,id={message_event.message_id}]插件不存在")
            else:
                send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]参数错误")

        if message_event.raw_message.startswith(".off"):
            text = message_event.raw_message.split(" ")
            if len(text) == 1:
                send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]请输入插件名")
            elif len(text) == 2:
                _plugin = text[1]
                if is_plugin_exist(_plugin):
                    config['PLUGIN'][_plugin] = 'False'
                    with open(file_path, 'w', encoding='utf-8') as configfile:
                        config.write(configfile)
                    send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]插件{_plugin}已禁用")
                else:
                    send_group_message(message_event.group_id, f"[CQ:reply,id={message_event.message_id}]插件不存在")
            else:
                send_group_message(message_event.group_id,f"[CQ:reply,id={message_event.message_id}]参数错误")



        # 使用 importlib 执行插件
        for index in plugins:
            plugin_module = importlib.import_module("plugins." + plugins[index]['file'])
            try:
                if plugins[index]['status'] == 'True':
                    result = 0
                    if task == 1:
                        result = plugin_module.group_message(json.dumps(message))
                    elif task == 2:
                        result = plugin_module.private_message(json.dumps(message))
                    if result == 1:
                        logger.info(f"Plugin \'{plugins[index]['info']['name']}\' Intercepted Message.")
                        break

                del sys.modules["plugins." + plugins[index]['file']]
            except Exception as e:
                logger.error(f"Error In Plugin:{e}")





