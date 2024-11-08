import json
import sys

from utils.operate import send_group_message, send_private_message

class EventGroupMessage:
    def __init__(self, message):  # 直接接收 message 字典
        # 从字典中提取值并进行类型转换
        self.time = str(message.get("time", ""))
        self.self_id = str(message.get("self_id", ""))
        self.post_type = str(message.get("post_type", ""))
        self.message_type = str(message.get("message_type", ""))
        self.sub_type = str(message.get("sub_type", ""))
        self.message_id = str(message.get("message_id", ""))
        self.group_id = str(message.get("group_id", ""))
        self.user_id = str(message.get("user_id", ""))
        self.anonymous = str(message.get("anonymous", "")) or None  # 处理 None 值
        self.message = str(message.get("message", ""))
        self.raw_message = str(message.get("raw_message", ""))
        self.font = str(message.get("font", ""))
        self.sender = EventGroupSender(**{k: str(v) for k, v in message.get("sender", {}).items()}) if message.get("sender") else None
        self.message_seq = str(message.get("message_seq", "")) or None  # 处理 message_seq

    def __repr__(self):
        return (f"<GroupMessageEvent(time={self.time}, user_id={self.user_id}, "
                f"group_id={self.group_id}, message={self.message}, sender={self.sender})>")
class EventGroupSender:
    def __init__(self, user_id, nickname, card, role):
        self.user_id = str(user_id)
        self.nickname = str(nickname)
        self.card = str(card)
        self.role = str(role)

    def __repr__(self):
        return f"<Sender(user_id={self.user_id}, nickname={self.nickname}, card={self.card}, role={self.role})>"


info = {
    "name": "Example",
    "description": "A Example Plugin",
    "author": "Mnzn",
    "version": "0.0.1"
    }

def main(message):
    message_event = EventGroupMessage(json.loads(message))
    if message_event.raw_message == "test":
        send_group_message(message_event.group_id, "Module:Test-Success")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    message = sys.argv[1]
    main(message)


