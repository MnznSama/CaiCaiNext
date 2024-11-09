import json
from utils.operate import send_group_message, send_private_message
from utils.events import GroupMessage, PrivateMessage
from utils import log



info = {
    "name": "Example",
    "description": "A Example Plugin",
    "author": "Mnzn",
    "version": "0.0.1"
    }

logger = log.get_logger()

def group_message(message):
    message_event = GroupMessage(json.loads(message))
    if message_event.raw_message == "test":
        logger.debug("Module:Test-Success")
        print(1)
        send_group_message(message_event.group_id, "Module:Test-Success")
        return 1
    else:
        return 0

def private_message(message):
    message_event = PrivateMessage(json.loads(message))
    logger.debug(message_event)
    return 1