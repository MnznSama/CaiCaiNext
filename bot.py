# -*- coding: utf-8 -*-
import configparser
import os
import websocket
import threading
import json

from utils import log

logger = log.get_logger()
config = configparser.ConfigParser()
config.read('.\data\config.ini',encoding='utf-8')
startmsg = config['DEFAULT']['startmsg']
upgroup = config['DEFAULT']['upgroup']
wsUrl = "ws://"+config['WS']['url']+":"+config['WS']['port']+"/"
ws = None

def on_open(ws):
    payload = {
        "action": "send_group_msg",
        "params": {
            "group_id": upgroup,
            "message": f"{startmsg}\n"
        },
        "echo": "StartMessage"
    }
    ws.send(json.dumps(payload))
    print("Send Start Message:", payload)

def on_message(ws, message):
    logger.debug(f"Message:{message}")

def on_error(ws, error):
    logger.warning(f"Error:{error}")
def on_close(ws):
    logger.info("Connection Closed")
def run_websocket():
    ws = websocket.WebSocketApp(wsUrl,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever()
def send_pri_message(ws, qq, message):
    payload = {
        "action": "send_private_msg",
        "params": {
            "user_id": qq,
            "message": message
        },
        "echo": "SendMessage-Private-To-{}".format(qq)
    }
    ws.send(json.dumps(message))

def send_pub_message(ws, message):
    ws.send(json.dumps(message))
run_websocket()