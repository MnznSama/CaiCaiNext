import configparser
import json
import os.path
from xmlrpc.client import boolean

from utils.operate import send_group_message, send_private_message, delete_message
from utils.events import GroupMessage, PrivateMessage
from utils import log


#存放插件的基础信息
info = {
    "name": "Uplog",                  #插件名称
    "description": "A Example Plugin",  #插件描述
    "author": "Mnzn",                   #插件作者
    "version": "0.0.1"                  #插件版本
    }

DATA_DIR = os.path.join(
        os.getcwd(),
        "data",
        "plugins",
        info["name"]
)
config = configparser.ConfigParser()
config.read(os.path.join('data','config.ini'),encoding='utf-8')
upgroup = config['NapDog']['upgroup']

#注册日志
logger = log.get_logger(f"Plugin \'{info['name']}\'")

# 插件设计规范:
# 插件数据目录为./data/plugins/插件名称，所有的文件均应存储于该目录下
# 插件入口文件为./plugins/插件名称.py
# 插件入口文件必须包含info变量、init函数
# 所有的代码均应清晰明了，不进行混淆操作，禁止出现恶意代码

# ---------------------------------函数说明---------------------------------
# get_login_info()                                   获取登录信息
# send_group_message(群号, 消息内容)                  发送群消息-返回消息ID
# send_private_message(QQ号, 消息内容)                发送私聊消息-返回消息ID
# delete_message(消息ID)                              撤回消息
# add_group(群号)                                     加入群聊
# set_group_leave(群号)                               退出群聊
# add_friend(QQ号)                                    添加好友
# delete_friend(QQ号)                                 删除好友
# set_group_ban(群号, QQ号, 时间)                      禁言某人
# unmute_one(群号, QQ号)                              解除某人禁言
# set_group_whole_ban(群号, 是否禁言)                  全员禁言/解除全员禁言
# set_group_kick(群号, QQ号)                          群组踢人
# set_group_card(群号, QQ号, 群名片)                   设置群名片（群备注）
# set_group_kick(群号, QQ号)                          群踢人
# set_friend_add_request(flag, approve, remark)      处理好友请求
# set_group_add_request(flag, approve, reason)       处理加群请求/邀请
# get_friend_list()                                  获取好友列表
# get_group_info(群号)                                获取群信息
# get_group_list()                                   获取群列表
# get_group_member_list(群号)                         获取群成员列表
# get_group_member_info(群号, QQ号)                    获取群成员信息
#-------------------------------------------------------------------------

# -----------------------事件说明-----------------------
# 消息事件
# - group_message                         收到群消息
# - private_message                       收到私聊消息

# 通知事件
# - group_ban                             群禁言
# - group_recall                          群消息撤回
# - group_upload                          群文件上传
# - group_decrease                        群成员减少
# - group_increase                        群成员增加
# - group_admin                           群管理员变动
# - group_tick                            群成员戳一戳
# - friend_add                            好友添加

# 请求事件
# - friend_request                        好友请求
# - group_request                         群请求/邀请
#-----------------------------------------------------
#类说明-

# 以上所有规范均遵循OneBot11标准
# https://283375.github.io/onebot_v11_vitepress/event/message.html

#消息事件-接收到群消息
def group_message(message):
    if not on:
        return 0
    message_event = GroupMessage(json.loads(message))
    if message_event.group_id == upgroup:
        if message_event.raw_message.upper() == "TEST":
            logger.info("Module:Test-Success")
            send_group_message(message_event.group_id, "Module:Test-Success")
            return 1
        elif message_event.raw_message.upper() == "GETLOG":
            logger.info("Module:GetLog-Success")
            send_group_message(message_event.group_id, f"[CQ:reply,id={message_event.message_id}]{log.get_log()}",0)
            return 1
        else:
            return 0
    else:
        return 0

#消息事件-接收到私聊消息
def private_message(message):
    if not on:
        return 0
    return 0

#通知事件-群禁言
def group_ban(message):
    if not on:
        return 0
    return 0

#通知事件-群消息撤回
def group_recall(message):
    if not on:
        return 0
    return 0

#通知事件-群文件上传
def group_upload(message):
    if not on:
        return 0
    return 0

#通知事件-群成员减少
def group_decrease(message):
    if not on:
        return 0
    return 0

#通知事件-群成员增加
def group_increase(message):
    if not on:
        return 0
    return 0

#通知事件-群管理员变动
def group_admin(message):
    if not on:
        return 0
    return 0

#通知事件-群成员戳一戳
def group_tick(message):
    if not on:
        return 0
    return 0

#通知事件-好友添加
def friend_add(message):
    if not on:
        return 0
    return 0

#请求事件-好友请求
def friend_request(message):
    if not on:
        return 0
    return 0

#请求事件-群请求/邀请
def group_request(message):
    if not on:
        return 0
    return 0

def on():
    status = config['PLUGIN'][f'{info["name"]}']
    return bool(status)

#插件初始化
def init():
    return 1