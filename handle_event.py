import json
from utils import log
from events import message, meta, notice, request

def main(data):
    logger = log.get_logger()
    data = json.loads(data)
    if data.get("post_type") == "message":
        message.main(data)
    elif data.get("post_type") == "notice":
        notice.main(data)
    elif data.get("post_type") == "request":
        request.main(data)
    elif data.get("post_type") == "meta_event":
        meta.main(data)
    elif data.get("echo"):
        echo = data.get("echo")
        logger.info("Get-Echo|" + echo)