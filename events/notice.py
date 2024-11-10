import glob
import importlib
import json
import os
import sys

from utils import log
from utils.operate import get_message, get_plugin_status


#https://283375.github.io/onebot_v11_vitepress/event/notice.html

def main(message):
    logger = log.get_logger("Notice")
    notice_type = message.get("notice_type")
    task = 0
    if notice_type == "group_ban":
        logger.info(f"群禁言 | {message.get('group_id')} | {message.get('operator_id')} 禁言了 {message.get('user_id')} : {message.get('duration')}s")
        task = 1
    elif notice_type == "group_recall":
        msg = get_message(message.get("message_id"))
        logger.info(f"群消息撤回 | {message.get('group_id')} | {message.get('user_id')} 撤回了 {msg.get('sender')['user_id']} : {msg.get('raw_message')}")
        task = 2
    elif notice_type == "friend_recall":
        msg = get_message(message.get("message_id"))
        logger.info(
            f"好友消息撤回 | {message.get('user_id')} 撤回了内容 {msg.get('raw_message')}")
        task = 3
    elif notice_type == "group_decrease":
        logger.info(f"群人数减少 | {message.get('group_id')} | {message.get('operator_id')} ->{message.get('sub_type')} - {message.get('user_id')}")
        task = 4
    elif notice_type == "group_increase":
        logger.info(f"群人数增加 | {message.get('group_id')} | {message.get('operator_id')} ->{message.get('sub_type')} - {message.get('user_id')}")
        task = 5
    elif notice_type == "group_admin":
        logger.info(f"群管理员变动 | {message.get('group_id')} | {message.get('user_id')} : {message.get('sub_type')}")
        task = 6
    elif notice_type == "notify":
        logger.info(f"戳一戳 | {message.get('group_id')} | {message.get('user_id')} 戳了戳 {message.get('target_id')}")
        task = 7
    elif notice_type == "friend_add":
        logger.info(f"新好友 | {message.get('user_id')}")
        task = 8

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
    # 使用 importlib 执行插件
    for index in plugins:
        plugin_module = importlib.import_module("plugins." + plugins[index]['file'])
        try:
            if plugins[index]['status'] == 'True':
                result = 0
                if task == 1:
                    result = plugin_module.group_ban(json.dumps(message))
                elif task == 2:
                    result = plugin_module.group_recall(json.dumps(message))
                elif task == 3:
                    result = plugin_module.friend_recall(json.dumps(message))
                elif task == 4:
                    result = plugin_module.group_decrease(json.dumps(message))
                elif task == 5:
                    result = plugin_module.group_increase(json.dumps(message))
                elif task == 6:
                    result = plugin_module.group_admin(json.dumps(message))
                elif task == 7:
                    result = plugin_module.group_tick(json.dumps(message))
                elif task == 8:
                    result = plugin_module.friend_add(json.dumps(message))
            del sys.modules["plugins." + plugins[index]['file']]
        except Exception as e:
            logger.error(f"Error In Plugin:{e}")
