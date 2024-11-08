import os
import websocket
import threading
import json

wsUrl = ""

def on_open(ws):
    payload = {
        "action": "send_private_msg",
        "params": {
            "user_id": author,
            "message": "Service Launched"
        },
        "echo": "ServiceLaunched"
    }
    send_message(ws, payload)
    print("Send Start Message:", payload)

def on_message(ws, message):

def on_error(ws, error):

def on_close(ws):

def run_websocket():
    ws = websocket.WebSocketApp(wsUrl,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
