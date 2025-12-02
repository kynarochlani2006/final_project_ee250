from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Store last 200 data points
data_buffer = []

@app.route("/")
def home():
    return render_template("dashboard.html")

# Node 1 sends data here
@app.route("/ingest", methods=["POST"])
def ingest():
    global data_buffer
    try:
        obj = request.get_json()
        obj["received_at"] = time.time()
        data_buffer.append(obj)

        # keep buffer small
        if len(data_buffer) > 200:
            data_buffer = data_buffer[-200:]

        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# Dashboard fetches data here
@app.route("/data")
def get_data():
    return jsonify(data_buffer[-100:])  # last 100 points

# Flask entrypoint for Gunicorn (Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
