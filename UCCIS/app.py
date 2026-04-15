from flask import Flask, render_template, jsonify, request
import json, random
from datetime import datetime

app = Flask(__name__)

mode = "synthetic"
alerts = []

def load_data():
    with open("data.json") as f:
        return json.load(f)

# 🔥 AI Risk Prediction (simple logic)
def predict_risk(status):
    if status == "Red":
        return random.randint(80, 100)
    elif status == "Yellow":
        return random.randint(50, 79)
    else:
        return random.randint(10, 49)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/zones")
def zones():
    data = load_data()

    for z in data["zones"]:
        if mode == "synthetic":
            z["status"] = random.choice(["Green", "Yellow", "Red"])

        z["risk"] = predict_risk(z["status"])

    return jsonify(data)

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    
    if data is None:
        return jsonify({"error": "Invalid request"}), 400

    alert = {
        "zone": data["zone"],
        "action": data["action"],
        "severity": "High" if data["action"] == "Emergency" else "Medium",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    alerts.append(alert)

    return jsonify(alert)

@app.route("/alerts")
def get_alerts():
    return jsonify(alerts)

@app.route("/mode", methods=["POST"])
def mode_switch():
    global mode
    if request.json is None:
        return jsonify({"error": "Invalid request"}), 400
    mode = request.json["mode"]
    return jsonify({"mode": mode})

if __name__ == "__main__":
    app.run(debug=True)