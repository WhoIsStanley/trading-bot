import yfinance as yf
import mplfinance as mpf
import pandas as pd
import json, os

class StockChart:
    def __init__(self, ticker, period="6mo", interval="1d", volume=True, rsi=False, macd=False, sma_periods=None, style_file="dark_style.json"):
        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.Volume = volume
        self.RSI = rsi
        self.MACD = macd
        self.SMA_periods = sma_periods if sma_periods else []
        # Style
        self.DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self.filepath = os.path.join(self.DATA_DIR, style_file)
        with open(self.filepath, "r") as f:
            self.style = json.load(f)
        self.colors_map = ["red", "blue", "magenta"]
        # Data
        self.save_file=f"data/{self.ticker}_chart.png"
        self.df = None
        
    
    def download_data(self):
        self.df = yf.download(self.ticker, period=self.period, interval=self.interval)
        if isinstance(self.df.columns, pd.MultiIndex):
            self.df.columns = [col[0] for col in self.df.columns]
        
    
    def plot(self, figsize=(12,9)):
        self.download_data()
        panel_ratios = [3] + [1.2]*1
        fig, axes = mpf.plot(
            self.df,
            type="candle",
            style=self.style,
            volume=self.Volume,
            figsize=figsize,
            panel_ratios=panel_ratios,
            returnfig=True
        )

        fig.savefig(self.save_file, bbox_inches="tight", pad_inches=0.2)
        
        return self.save_file