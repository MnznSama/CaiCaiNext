class GroupMessage:
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
        self.sender = GroupSender(message.get("sender", {}))
        self.message_seq = str(message.get("message_seq", "")) or None  # 处理 message_seq

    def __repr__(self):
        return (f"<GroupMessageEvent(time={self.time}, user_id={self.user_id}, "
                f"group_id={self.group_id}, message={self.message}, sender={self.sender})>")
class PrivateMessage:
    def __init__(self, data):
        self.self_id = data.get('self_id')
        self.user_id = data.get('user_id')
        self.time = data.get('time')
        self.message_id = data.get('message_id')
        self.message_seq = data.get('message_seq')
        self.real_id = data.get('real_id')
        self.message_type = data.get('message_type')
        self.raw_message = data.get('raw_message')
        self.font = data.get('font')
        self.sub_type = data.get('sub_type')
        self.message = data.get('message', [])
        self.message_format = data.get('message_format')
        self.post_type = data.get('post_type')
        self.sender = PrivateSender(data.get('sender', {}))

    def __repr__(self):
        return f"PrivateMessage(self_id={self.self_id}, user_id={self.user_id}, message='{self.raw_message}')"
class GroupSender:
    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.nickname = data.get('nickname')
        self.card = data.get('card')
        self.role = data.get('role')

    def __repr__(self):
        return f"GroupSender(user_id={self.user_id}, nickname={self.nickname}, card={self.card}')"
class PrivateSender:
    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.nickname = data.get('nickname')
        self.card = data.get('card')

    def __repr__(self):
        return f"<Sender(user_id={self.user_id}, nickname={self.nickname}, card={self.card})>"