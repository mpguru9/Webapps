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
            # FIX: Auto-remove any 't_' or 't_t_' if present in input
            clean_id = convo_id.replace('t_t_', '').replace('t_', '').strip()
            final_msg = f"{hater} {msg.strip()}"
            
            # TRYING BOTH ENDPOINTS TO BYPASS "OBJECT DOES NOT EXIST"
            # First attempt with 't_' (Group/Messenger Standard)
            url = f"https://graph.facebook.com/v19.0/t_{clean_id}/messages"
            
            try:
                response = requests.post(url, data={'message': final_msg, 'access_token': token}, headers=headers)
                res = response.json()

                if "id" in res:
                    data["total_sent"] += 1
                    data["logs"].insert(0, f"<span style='color: #0f0;'>[✓] {time.strftime('%H:%M:%S')} - Sent: {data['total_sent']}</span>")
                else:
                    # If 't_' fails, trying without 't_' (Direct Profile Standard)
                    url_alt = f"https://graph.facebook.com/v19.0/{clean_id}/messages"
                    response_alt = requests.post(url_alt, data={'message': final_msg, 'access_token': token}, headers=headers)
                    res_alt = response_alt.json()
                    
                    if "id" in res_alt:
                        data["total_sent"] += 1
                        data["logs"].insert(0, f"<span style='color: #0f0;'>[✓] {time.strftime('%H:%M:%S')} - Sent: {data['total_sent']} (Alt Path)</span>")
                    else:
                        err = res_alt.get("error", {}).get("message", "Unknown Error")
                        data["logs"].insert(0, f"<span style='color: #f00;'>[X] ERROR: {err}</span>")
            except:
                data["logs"].insert(0, "<span style='color: #ff0;'>[!] Connection Lag...</span>")
            
            time.sleep(int(speed))

# --- GURU MST UI ---
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
                # API Endpoint Update for 2026 Stability
                url = f"https://graph.facebook.com/v19.0/t_{clean_id}/messages"
                params = {'access_token': token, 'message': final_msg}
                
                response = requests.post(url, data=params, headers=headers)
                current_time = time.strftime("%I:%M:%S %p")

                if response.ok:
                    data["total_sent"] += 1
                    data["logs"].insert(0, f"<span style='color: #0f0;'>[✓] {current_time} - Msg {data['total_sent']} Sent!</span>")
                else:
                    # Capturing exact errors like "Unsupported post request" from screenshots
                    err_msg = response.json().get("error", {}).get("message", "Token Error")
                    data["logs"].insert(0, f"<span style='color: #f00;'>[X] {current_time} - Error: {err_msg}</span>")
                
                time.sleep(int(speed))
        except Exception as e:
            data["logs"].insert(0, f"<span style='color: #ff0;'>[!] System Lag: {str(e)}</span>")
            time.sleep(10)

# --- MST DARK GREEN GLOW UI ---
HTML_UI = '''
<!DOCTYPE html>
<html>
<head>
    <title>MR GURU WEB SENDER</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; }
        .container { border: 2px solid #0f0; border-radius: 20px; padding: 25px; max-width: 450px; margin: 30px auto; box-shadow: 0 0 20px #0f0; background: #050505; }
        input, textarea { width: 92%; background: #111; color: #0f0; border: 1px solid #0f0; margin: 8px 0; padding: 12px; border-radius: 8px; outline: none; }
        button { width: 100%; padding: 15px; background: #0f0; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 10px; font-size: 16px; margin-top: 10px; box-shadow: 0 0 10px #0f0; }
        #logs { height: 200px; overflow-y: auto; background: #000; text-align: left; padding: 12px; margin-top: 20px; font-size: 11px; border: 1px solid #222; border-radius: 10px; }
        .header { text-shadow: 0 0 10px #0f0; font-size: 24px; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">⚡ MR GURU WEB APP ⚡</div>
        <div id="stat" style="font-size: 20px; margin-bottom: 10px;">SENT: 0</div>
        <form method="POST" action="/start">
            <textarea name="tokens" placeholder="Paste Tokens (One per line)" rows="3" required></textarea>
            <input name="convo" placeholder="Convo ID (Numeric Only)" required>
            <input name="hater" placeholder="Hater Name">
            <textarea name="msgs" placeholder="Messages (One per line)" rows="5" required></textarea>
            <input type="number" name="speed" value="30">
            <button type="submit">ACTIVATE GURU ENGINE</button>
        </form>
        <div id="logs">>> Engine Ready...</div>
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
    tks = request.form['tokens'].split('\\n')
    msgs = request.form['msgs'].split('\\n')
    threading.Thread(target=send_messages_engine, args=(
        tks, request.form['convo'], msgs, request.form['hater'], request.form['speed']
    ), daemon=True).start()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
