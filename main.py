import requests
import threading
import time
import os
from flask import Flask, render_template_string, request, redirect, jsonify

app = Flask(__name__)
data = {"status": "OFFLINE", "logs": [], "total_sent": 0}

def guru_engine_fixed(tokens, convo_id, messages, hater, speed):
    global data
    data["status"] = "RUNNING"
    data["total_sent"] = 0
    num_tokens = len(tokens)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    while data["status"] == "RUNNING":
        for i, msg in enumerate(messages):
            if data["status"] != "RUNNING": break
            token = tokens[i % num_tokens].strip()
            clean_id = convo_id.replace('t_t_', '').replace('t_', '').strip()
            final_msg = f"{hater} {msg.strip()}"
            url = f"https://graph.facebook.com/v19.0/t_{clean_id}/messages"
            try:
                response = requests.post(url, data={'message': final_msg, 'access_token': token}, headers=headers)
                res = response.json()
                if "id" in res:
                    data["total_sent"] += 1
                    data["logs"].insert(0, f"<span style='color: #0f0;'>[✓] {time.strftime('%H:%M:%S')} - Sent: {data['total_sent']}</span>")
                else:
                    url_alt = f"https://graph.facebook.com/v19.0/{clean_id}/messages"
                    response_alt = requests.post(url_alt, data={'message': final_msg, 'access_token': token}, headers=headers)
                    res_alt = response_alt.json()
                    if "id" in res_alt:
                        data["total_sent"] += 1
                        data["logs"].insert(0, f"<span style='color: #0f0;'>[✓] {time.strftime('%H:%M:%S')} - Sent (Alt): {data['total_sent']}</span>")
                    else:
                        err = res_alt.get("error", {}).get("message", "Unknown Error")
                        data["logs"].insert(0, f"<span style='color: #f00;'>[X] ERROR: {err}</span>")
            except:
                data["logs"].insert(0, "<span style='color: #ff0;'>[!] Connection Lag...</span>")
            time.sleep(int(speed))

HTML_UI = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR GURU V43 FIXED</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; }
        .main-box { border: 2px solid #0f0; border-radius: 15px; padding: 20px; max-width: 450px; margin: 20px auto; box-shadow: 0 0 15px #0f0; }
        textarea, input { width: 90%; background: #111; color: #0f0; border: 1px solid #0f0; margin: 5px; padding: 10px; border-radius: 5px; }
        button { width: 95%; padding: 15px; background: #0f0; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 10px; }
        #log-box { height: 180px; overflow-y: auto; background: #050505; text-align: left; padding: 10px; margin-top: 15px; font-size: 11px; border: 1px solid #333; }
    </style>
</head>
<body>
    <div class="main-box">
        <h2 style="text-shadow: 0 0 10px #0f0;">⚡ MR GURU REPAIR V43 ⚡</h2>
        <div id="status">SENT: 0</div>
        <form method="POST" action="/start">
            <textarea name="tks" placeholder="Tokens (One per line)" rows="3" required></textarea>
            <input name="id" placeholder="Convo ID (Numeric Only)" required>
            <input name="hater" placeholder="Hater Name">
            <textarea name="msgs" placeholder="Messages (One per line)" rows="5" required></textarea>
            <input name="spd" type="number" value="30">
            <button type="submit">FIX & START SENDING</button>
        </form>
        <div id="log-box">>> Ready for repair deployment...</div>
    </div>
    <script>
        setInterval(() => {
            fetch('/status').then(r => r.json()).then(d => {
                document.getElementById('status').innerText = "SENT: " + d.total_sent;
                document.getElementById('log-box').innerHTML = d.logs.join("<br>");
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
    tks = request.form['tks'].split('\\n')
    msgs = request.form['msgs'].split('\\n')
    threading.Thread(target=guru_engine_fixed, args=(tks, request.form['id'], msgs, request.form['hater'], request.form['spd']), daemon=True).start()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
