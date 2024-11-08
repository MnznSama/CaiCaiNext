import configparser
import requests
from utils import log

logger = log.get_logger()
config = configparser.ConfigParser()
config.read('.\data\config.ini',encoding='utf-8')
url = "http://"+config['WS']['url']+":"+str(int(config['WS']['port'])+1)+"/"
token = config['WS']['token']
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
}

def send_private_message(qq, message):
    payload = {
            "user_id": qq,
            "message": message
        }
    response = requests.post(url+"send_private_msg", headers=headers, json=payload)

def send_group_message(group,message):
    payload = {
            "group_id": group,
            "message": message,
            "echo": "SendMessage-Group-To-{}".format(group)
        }
    response = requests.post(url + "send_group_msg", headers=headers, json=payload)
    logger.info(f"Send Group Message To {group} : {message}")
    #print(response.text)