import json, os

ALERTS_FILE = "alerts.json"
alerts = {}

def load_alerts():
    global alerts
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            alerts = json.load(f)
    else:
        alerts = {}

def save_alerts(data=None):
    global alerts
    if data is not None:
        alerts = data
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4, default=str)