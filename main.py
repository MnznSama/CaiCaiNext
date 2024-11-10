# -*- coding: utf-8 -*-
import argparse
import configparser

author = ''                             #机器人主人QQ
upGroup = ''                            #机器人上报群号
debug = False                           #是否开启调试模式
startMsg = 'Bot Start'                  #机器人启动时发送的消息
url = '127.0.0.1'                       #NapCat设置的正向WebSocket地址
port = 1145                             #NapCat设置的WebSocket端口,+1为应开放的HTTP端口
token = ''                              #NapCat设置的AccessToken

#配置文件
DATA = {
    "config.ini": {
        'NapDog': {
            'author': author,
            'upgroup': upGroup,
            'debug': debug,
            'startmsg': startMsg
        },
        'WS': {
            'url': url,
            'port': port,
            'token': token
        },
        'PLUGIN': {
        }

    }
}

DATA_DIR = (
        "data\groups",
        "data\plugins",
        "logs",
        "plugins"
)


def main():
    from bot import run_websocket
    run_websocket()                         #运行机器人


if __name__=="__main__":
    from utils import initialize
    initialize.init(DATA, DATA_DIR)    #初始化

    config = configparser.ConfigParser()
    config.read('.\data\config.ini',encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", type=bool, default=False)
    args = parser.parse_args()
    debug = args.debug
    # print(debug)
    if args.debug:
       config.set('NapDog', 'debug', 'True')
    else:
        config.set('NapDog', 'debug', 'False')
    with open('.\data\config.ini', 'w', encoding='utf-8') as f:
        config.write(f)

    main()
