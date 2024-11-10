import configparser
import glob
import importlib
import os.path

import requests
from utils import log

logger = log.get_logger()
config = configparser.ConfigParser()
config.read(os.path.join("data", "config.ini"),encoding='utf-8')
url = "http://"+config['WS']['url']+":"+str(int(config['WS']['port'])+1)+"/"
token = config['WS']['token']
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
}

def get_message(message_id):
    payload = {
            "message_id": message_id
        }
    response = requests.get(url + "get_msg", headers=headers, params=payload)
    response_json = response.json()
    logger.debug(response.text)
    if response_json['status'] == 'ok':
        logger.info(f"Get Message {message_id} Success.")
    elif response_json['status'] == 'error':
        logger.error(f"Get Message {message_id} Failed.")
    return response_json['data']
def get_login_info():
    response = requests.get(url + "get_login_info", headers=headers)
    response_json = response.json()
    logger.debug(response.text)
    if response_json['status'] == 'ok':
        logger.info(f"Get Login Info Success.")
    elif response_json['status'] == 'error':
        logger.error(f"Get Login Info Failed.")
    return response_json['data']
def send_private_message(qq, message):
    payload = {
            "user_id": qq,
            "message": message
        }
    response = requests.post(url+"send_private_msg", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Send Private Message To {qq}:{message}(message_id:{response_json['data']['message_id']})")
    elif response_json['status'] == 'error':
        logger.error(f"Send Private Message To {qq} Failed:{message}({response.text})")
    return response_json['data']['message_id']
def send_group_message(group,message,visible=1):
    payload = {
            "group_id": group,
            "message": message,
            "echo": "SendMessage-Group-To-{}".format(group)
        }
    response = requests.post(url + "send_group_msg", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if visible == 0:
        return response_json['data']['message_id']
    if  response_json['status'] == 'ok':
        logger.info(f"Send Group Message To {group}:{message}(message_id:{response_json['data']['message_id']})")
    elif response_json['status'] == 'error':
        logger.error(f"Send Group Message To {group} Failed:{message}({response.text})")
    return response_json['data']['message_id']
def delete_message(message_id):
    payload = {
            "message_id": message_id,
            "echo": "DeleteMessage-{}".format(message_id)
        }
    response = requests.post(url + "delete_msg", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Delete Message {message_id} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Delete Message {message_id} Failed.")
    return response_json['data']['message_id']
def add_group(group):
    payload = {
            "group_id": group,
            "echo": "AddGroup-{}".format(group)
        }
    response = requests.post(url + "add_group", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Add Group {group} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Add Group {group} Failed.")
    return response_json['data']['message_id']
def set_group_leave(group):
    payload = {
            "group_id": group,
            "echo": "SetGroupLeave-{}".format(group)
        }
    response = requests.post(url + "set_group_leave", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Set Group Leave {group} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Set Group Leave {group} Failed.")
    return response_json['data']['message_id']
def add_friend(qq):
    payload = {
            "user_id": qq,
            "echo": "AddFriend-{}".format(qq)
        }
    response = requests.post(url + "add_friend", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Add Friend {qq} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Add Friend {qq} Failed.")
    return response_json['data']['message_id']
def delete_friend(qq):
    payload = {
            "user_id": qq,
            "echo": "DeleteFriend-{}".format(qq)
        }
    response = requests.post(url + "delete_friend", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Delete Friend {qq} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Delete Friend {qq} Failed.")
    return response_json['data']['message_id']
def set_group_ban(group,qq,time):
    payload = {
            "group_id": group,
            "user_id": qq,
            "duration": time,
            "echo": "SetGroupBan-{}-{}-{}".format(group,qq,time)
        }
    response = requests.post(url + "set_group_ban", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Set Group Ban {qq} In {group} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Set Group Ban {qq} In {group} Failed.")
    return response_json['data']['message_id']
def unmute_one(group,qq):
    payload = {
            "group_id": group,
            "user_id": qq,
            "duration": 0,
            "echo": "UnmuteOne-{}-{}".format(group,qq)
        }
    response = requests.post(url + "set_group_ban", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Unmute {qq} In {group} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Unmute {qq} In {group} Failed.")
    return response_json['data']['message_id']
def set_group_whole_ban(group,ban):
    payload = {
            "group_id": group,
            "enable": ban,
            "echo": "SetGroupWholeBan-{}-{}".format(group,ban)
        }
    response = requests.post(url + "set_group_whole_ban", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Set Group Whole Ban {group} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Set Group Whole Ban {group} Failed.")
    return response_json['data']['message_id']
def set_group_kick(group,qq):
    payload = {
            "group_id": group,
            "user_id": qq,
            "reject_add_request": False,
            "echo": "SetGroupKick-{}-{}".format(group,qq)
        }
    response = requests.post(url + "set_group_kick", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Set Group Kick {qq} In {group} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Set Group Kick {qq} In {group} Failed.")
    return response_json['data']['message_id']
def set_group_card(group,qq,card):
    payload = {
            "group_id": group,
            "user_id": qq,
            "card": card,
            "echo": "SetGroupCard-{}-{}-{}".format(group,qq,card)
        }
    response = requests.post(url + "set_group_card", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Set Group Card {qq} In {group} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Set Group Card {qq} In {group} Failed.")
    return response_json['data']['message_id']
def set_friend_add_request(flag,approve,remark):
    payload = {
            "flag": flag,
            "approve": approve,
            "remark": remark,
            "echo": "SetFriendAddRequest-{}-{}-{}".format(flag,approve,remark)
        }
    response = requests.post(url + "set_friend_add_request", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Set Friend Add Request {flag} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Set Friend Add Request {flag} Failed.")
    return response_json['data']['message_id']
def set_group_add_request(flag,approve,reason):
    payload = {
            "flag": flag,
            "approve": approve,
            "reason": reason,
            "echo": "SetGroupAddRequest-{}-{}-{}".format(flag,approve,reason)
        }
    response = requests.post(url + "set_group_add_request", headers=headers, json=payload)
    response_json = response.json()
    logger.debug(response.text)
    if  response_json['status'] == 'ok':
        logger.info(f"Set Group Add Request {flag} Success.")
    elif response_json['status'] == 'error':
        logger.warning(f"Set Group Add Request {flag} Failed.")
    return response_json['data']['message_id']
def get_friend_list():
    response = requests.get(url + "get_friend_list", headers=headers)
    response_json = response.json()
    logger.debug(response.text)
    if response_json['status'] == 'ok':
        logger.info(f"Get Friend List Success.")
    elif response_json['status'] == 'error':
        logger.error(f"Get Friend List Failed.")
    return response_json['data']
def get_group_info(group):
    payload = {
            "group_id": group
        }
    response = requests.get(url + "get_group_info", headers=headers, params=payload)
    response_json = response.json()
    logger.debug(response.text)
    if response_json['status'] == 'ok':
        logger.info(f"Get Group Info {group} Success.")
    elif response_json['status'] == 'error':
        logger.error(f"Get Group Info {group} Failed.")
    return response_json['data']
def get_group_list():
    response = requests.get(url + "get_group_list", headers=headers)
    response_json = response.json()
    logger.debug(response.text)
    if response_json['status'] == 'ok':
        logger.info(f"Get Group List Success.")
    elif response_json['status'] == 'error':
        logger.error(f"Get Group List Failed.")
    return response_json['data']
def get_group_member_list(group):
    payload = {
            "group_id": group
        }
    response = requests.get(url + "get_group_member_list", headers=headers, params=payload)
    response_json = response.json()
    logger.debug(response.text)
    if response_json['status'] == 'ok':
        logger.info(f"Get Group Member List {group} Success.")
    elif response_json['status'] == 'error':
        logger.error(f"Get Group Member List {group} Failed.")
    return response_json['data']
def get_group_member_info(group,qq):
    payload = {
            "group_id": group,
            "user_id": qq
        }
    response = requests.get(url + "get_group_member_info", headers=headers, params=payload)
    response_json = response.json()
    logger.debug(response.text)
    if response_json['status'] == 'ok':
        logger.info(f"Get Group Member Info {qq} In {group} Success.")
    elif response_json['status'] == 'error':
        logger.error(f"Get Group Member Info {qq} In {group} Failed.")
    return response_json['data']

def get_plugin_status(pluginname):
    config.read(os.path.join("data", "config.ini"), encoding='utf-8')
    on = config['PLUGIN'][pluginname]
    return on

def is_plugin_exist(pluginname):
    plugin_files = glob.glob(os.path.join("plugins", '*.py'))
    plugins = {}
    exist = False
    for file in plugin_files:
        _file = os.path.splitext(os.path.basename(file))[0]
        plugin_module = importlib.import_module("plugins." + _file)
        info =  plugin_module.info
        if str(info['name']).upper() == pluginname.upper():
            exist = True
            break
    return exist