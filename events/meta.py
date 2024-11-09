from utils import log

def main(message):
    logger = log.get_logger()
    if message.get("meta_event_type") == "heartbeat":
        logger.debug("Get-HeartBeat-" + str(message.get("status").get("online")) + "-" + str(
            message.get("status").get("good")) + "-" + str(message.get("time")))
    if message.get("meta_event_type") == "lifecycle":
        logger.debug("LifeCycle-" + message.get("sub_type") + "-" + str(message.get("self_id")))