# -*- coding: utf-8 -*-
import websocket
import configparser
import threading
from utils.operate import send_group_message
from utils import log

def on_open(ws):
    send_group_message(upgroup, startmsg)
    send_group_message(upgroup, log.get_log(),0)
    logger.info('Bot Started')
def on_message(ws, message):
    import handle_event
    logger.debug(f"Message:{message}")
    threading.Thread(target=handle_event.main, args=(message,)).start()
def on_error(ws, error):
    logger.warning(f"Error:{error}")
def on_close(ws):
    logger.info("Connection Closed")
def run_websocket():
    ws.run_forever()



logger = log.get_logger()
config = configparser.ConfigParser()
config.read('.\data\config.ini',encoding='utf-8')
startmsg = config['NapDog']['startmsg']
upgroup = config['NapDog']['upgroup']
token = config['WS']['token']
wsUrl = "ws://"+config['WS']['url']+":"+config['WS']['port']+"/event"
ws = websocket.WebSocketApp(wsUrl,
                            header={"Authorization": "Bearer "+token},
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error)

if __name__ == '__main__':
    run_websocket()
