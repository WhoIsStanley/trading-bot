import yfinance as yf
import mplfinance as mpf
import pandas as pd

info = yf.Ticker("VOO").info
logo_url = info.get("logo_url")

if not logo_url and "website" in info:
    domain = info["website"].split("/")[2]  # extract domain
    logo_url = f"https://logo.clearbit.com/{domain}"

print(logo_url)
print(info)

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