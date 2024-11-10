import base64
import json
import os

import requests

from utils.operate import send_group_message, send_private_message, delete_message
from utils.events import GroupMessage, PrivateMessage
from utils import log
from typing import Dict, Any

class Usage:
    def __init__(self, prompt_tokens: int, prompt_unit_price: str, prompt_price: str,
                 completion_tokens: int, completion_unit_price: str, completion_price: str,
                 total_tokens: int, total_price: str, currency: str, latency: float):
        self.prompt_tokens = prompt_tokens
        self.prompt_unit_price = prompt_unit_price
        self.prompt_price = prompt_price
        self.completion_tokens = completion_tokens
        self.completion_unit_price = completion_unit_price
        self.completion_price = completion_price
        self.total_tokens = total_tokens
        self.total_price = total_price
        self.currency = currency
        self.latency = latency

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Usage':
        return cls(**{k: data.get(k, v) for k, v in {
            'prompt_tokens': 0,
            'prompt_unit_price': '',
            'prompt_price': '',
            'completion_tokens': 0,
            'completion_unit_price': '',
            'completion_price': '',
            'total_tokens': 0,
            'total_price': '',
            'currency': '',
            'latency': 0.0
        }.items()})
class RetrieverResource:
    def __init__(self, position: int, dataset_id: str, dataset_name: str,
                 document_id: str, document_name: str, segment_id: str,
                 score: float, content: str):
        self.position = position
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.document_id = document_id
        self.document_name = document_name
        self.segment_id = segment_id
        self.score = score
        self.content = content

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'RetrieverResource':
        return cls(**{k: data.get(k, v) for k, v in {
            'position': 0,
            'dataset_id': '',
            'dataset_name': '',
            'document_id': '',
            'document_name': '',
            'segment_id': '',
            'score': 0.0,
            'content': ''
        }.items()})
class ChatCompletionResponse:
    def __init__(self, event: str, message_id: str, conversation_id: str,
                 mode: str, answer: str, metadata: Dict[str, Any], created_at: int):
        self.event = event
        self.message_id = message_id
        self.conversation_id = conversation_id
        self.mode = mode
        self.answer = answer
        self.metadata = metadata

        # 解析 metadata
        self.usage = Usage.from_json(metadata.get('usage', {}))
        self.retriever_resources = [RetrieverResource.from_json(res) for res in metadata.get('retriever_resources', [])]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'ChatCompletionResponse':
        return cls(**{k: data.get(k, v) for k, v in {
            'event': '',
            'message_id': '',
            'conversation_id': '',
            'mode': '',
            'answer': '',
            'metadata': {},
            'created_at': 0
        }.items()})

info = {
    "name": "ChatBot",
    "description": "A Plugin For Chat With AI",
    "author": "Mnzn",
    "version": "0.0.1"
    }

logger = log.get_logger()
api_key = os.environ.get('dify_key')
model = "Qwen-Plus"

def group_message(message):
    message_event = GroupMessage(json.loads(message))
    if message_event.raw_message.startswith("菜菜"):
        logger.debug(f"AIChat:{message_event.raw_message}")
        to_delete_id = send_group_message(message_event.group_id, f"[CQ:reply,id={message_event.message_id}]菜菜看到啦！加速理解中！\n*PS:模型在墙的另一面，稍安勿躁 > , <")
        ai(message_event.raw_message, message_event.group_id, message_event.sender.user_id, message_event.sender.nickname, message_event.message_id, to_delete_id)
        return 1
    else:
        return 0

def private_message(message):
    message_event = PrivateMessage(json.loads(message))
    logger.debug(message_event)
    return 1

def ai(raw_message, group_id, user_id, name, message_id, to_delete_id):
    url = 'https://api.dify.ai/v1/chat-messages'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "inputs": {
            "userName": f"{name}",
            "userId": f"{user_id}"
        },
        "query": raw_message,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": user_id
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    result = ChatCompletionResponse.from_json(response.json())
    token = result.usage.total_tokens
    price = result.usage.total_price
    logger.debug(f"AI RESPONSE | {result.answer} | conversation_id: {result.conversation_id} | message_id: {result.message_id} | tokens: {token} | price: {price}")
    if (json_answer := json.loads(result.answer)).get('mode') == 'chat':
        text = base64.b64decode(json_answer.get('text')).decode('utf-8')
        if 'f47ac10b' in text:
            text = "[Filtered]"
        text = f"[CQ:reply,id={message_id}]{text}\n*对话模型:{model}\n*对话消耗: {token} tokens"
        send_group_message(group_id, text)
        delete_message(to_delete_id)
        return 1