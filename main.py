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
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    while data["status"] == "RUNNING":
        try:
            for message_index in range(num_messages):
                if data["status"] != "RUNNING": break
                
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()

                # Original URL Logic with t_ prefix
                url = "https://graph.facebook.com/v15.0/{}/".format('t_' + convo_id.replace('t_', ''))
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                
                response = requests.post(url, json=parameters, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                if response.ok:
                    data["total_sent"] += 1
                    data["logs"].insert(0, f"[+] Sent: {message_index + 1} | Time: {current_time}")
                else:
                    data["logs"].insert(0, f"[x] Failed: {message_index + 1} | Error: {response.text}")
                
                time.sleep(int(speed))
            data["logs"].insert(0, "[!] All messages sent. Restarting...")
        except Exception as e:
            data["logs"].insert(0, f"[!] Error: {str(e)}")
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
        textarea, input { width: 90%; background: #111; color: #0f0; border: 1px solid #0f0; margin: 5px; padding: 10px; border-radius: 5px; }
        button { width: 95%; padding: 15px; background: #0f0; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 10px; }
        #logs { height: 200px; overflow-y: auto; background: #050505; text-align: left; padding: 10px; margin-top: 15px; font-size: 11px; border: 1px solid #333; }
    </style>
</head>
<body>
    <div class="box">
        <h1>MR GURU WEB APP</h1>
        <div id="stat">SENT: 0</div>
        <form method="POST" action="/start">
            <textarea name="tks" placeholder="Tokens (One per line)" rows="3" required></textarea>
            <input name="id" placeholder="Convo ID" required>
            <input name="hater" placeholder="Hater Name">
            <textarea name="msgs" placeholder="Messages (One per line)" rows="5" required></textarea>
            <input name="spd" type="number" placeholder="Speed (Seconds)" value="30">
            <button type="submit">ACTIVATE ENGINE</button>
        </form>
        <div id="logs">>> System Ready...</div>
    </div>
    <script>
        setInterval(() => {
            fetch('/status').then(r => r.json()).then(d => {
                document.getElementById('stat').innerText = "SENT: " + d.total_sent;
                document.getElementById('logs').innerHTML = d.logs.join("<br>");
            });
        }, 2000);
    </script>
</body>
</html>
'''

@app.route('/')
def home(): return render_template_string(HTML_UI)

@app.route('/status')
def status(): return jsonify(data)

@app.route('/start', methods=['POST'])
def start():
    tks = request.form['tks'].split('\n')
    msgs = request.form['msgs'].split('\n')
    threading.Thread(target=send_messages_logic, args=(
        tks, request.form['id'], msgs, request.form['hater'], request.form['spd']
    ), daemon=True).start()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
