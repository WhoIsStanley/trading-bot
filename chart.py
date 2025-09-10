import yfinance as yf
import mplfinance as mpf
import pandas as pd
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
ticker="388"
info = yf.Ticker(ticker).info
company_name = info.get("longName", ticker.upper())
print(f"{info} and {company_name}")
print(yahoo_search("VOOO"))


"""
binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},  
        "edge": {"up": "#3dc985", "down": "#ef4f60"},  
        "wick": {"up": "#3dc985", "down": "#ef4f60"},  
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},  
        "vcedge": {"up": "green", "down": "red"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}

ticker = "AAPL"
data = yf.download(ticker, period="3mo", interval="1d")

# If multi-index columns exist, flatten them
if isinstance(data.columns, pd.MultiIndex):
    data.columns = [col[0] for col in data.columns]

# Now mplfinance can plot
mpf.plot(
    data,
    type="candle",
    style=binance_dark,
    volume=True,
    title=f"{ticker} - Daily Candlestick",
    ylabel="Price ($)",
    ylabel_lower="Volume",
    savefig=f"{ticker}_chart.png"
)
"""