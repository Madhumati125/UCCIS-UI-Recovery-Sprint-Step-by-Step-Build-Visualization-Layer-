from flask import Flask, jsonify, request, render_template
import random
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- DATA ----------------
mode = "synthetic"

zones_data = [
    {"name": "Mumbai", "status": "Green", "risk": 0},
    {"name": "Thane", "status": "Yellow", "risk": 0},
    {"name": "Navi Mumbai", "status": "Red", "risk": 0}
]

alerts = []

# ---------------- AI RISK ----------------
def predict_risk(status):
    if status == "Red":
        return random.randint(80, 100)
    elif status == "Yellow":
        return random.randint(50, 79)
    return random.randint(10, 49)

# ---------------- ROUTES ----------------

# ✅ FIX: Homepage route added
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/zones")
def zones():
    for z in zones_data:
        if mode == "synthetic":
            z["status"] = random.choice(["Green", "Yellow", "Red"])
        z["risk"] = predict_risk(z["status"])
    return jsonify({"zones": zones_data})

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid request"}), 400
    zone_name = data.get("zone")
    action_type = data.get("action")

    for z in zones_data:
        if z["name"] == zone_name:
            z["status"] = "Green"  # ✅ state change

    alert = {
        "zone": zone_name,
        "action": action_type,
        "severity": "High" if action_type == "Emergency" else "Medium",
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
    if request.json:
        mode = request.json.get("mode", "synthetic")
    return jsonify({"mode": mode})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)