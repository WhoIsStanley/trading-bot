import json, os
import requests

def yahoo_search(query, count=5):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "quotesCount": count, "newsCount": 0}
    headers = {"User-Agent": "Mozilla/5.0"}  
    
    resp = requests.get(url, params=params, headers=headers)
    
    try:
        data = resp.json()
    except Exception:
        print("Response not JSON:", resp.text[:200])
        raise
    
    results = []
    for item in data.get("quotes", []):
        results.append({
            "symbol": item.get("symbol"),
            "shortname": item.get("shortname"),
            "exchange": item.get("exchDisp"), 
            "type": item.get("typeDisp") 
        })
    return results

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