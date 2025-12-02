import socket
import threading
import json
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# store data for dashboard
data_buffer = []

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/data")
def get_data():
    return jsonify(data_buffer[-100:])  # last 100 points

def tcp_server():
    HOST = "0.0.0.0"
    PORT = 5001

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("TCP server listening...")

    while True:
        client, addr = server.accept()
        print("Client connected:", addr)
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(conn):
    global data_buffer
    with conn:
        while True:
            line = conn.recv(1024)
            if not line:
                break
            try:
                obj = json.loads(line.decode().strip())
                data_buffer.append(obj)
            except:
                pass

if __name__ == "__main__":
    threading.Thread(target=tcp_server).start()
    app.run(host="0.0.0.0", port=5000)
