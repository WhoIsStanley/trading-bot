import discord
from discord.ext import commands, tasks
from datetime import datetime
import yfinance as yf
import asyncio
from alert_update import alerts, save_alerts, load_alerts

class AlertTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_alerts.start()

    def cog_unload(self):
        self.check_alerts.cancel()

    @tasks.loop(seconds=10)
    async def check_alerts(self):
        now = datetime.now()

        for channel_id, alert_list in list(alerts.items()):
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                continue

            for alert in alert_list[:]:
                try:
                    ticker = alert["ticker"]
                    operator = alert["operator"]
                    value = alert["value"]
                    end_date = alert["end_date"]
                    user_id = alert["user_id"]

                    # Expired
                    if end_date and now > datetime.strptime(end_date, "%Y-%m-%d"):
                        await channel.send(f"Alert expired for <@{user_id}> ({ticker})")
                        alert_list.remove(alert)
                        save_alerts(alerts)
                        continue

                    # Fetch latest price
                    data = yf.download(ticker, period="1d", interval="1m")
                    if data.empty:
                        continue

                    last_price = float(data["Close"].iloc[-1])

                    if (
                        (operator == ">" and last_price > value) or
                        (operator == "<" and last_price < value) or
                        (operator == ">=" and last_price >= value) or
                        (operator == "<=" and last_price <= value) or
                        (operator == "==" and last_price == value)
                    ):
                        try:
                            info = yf.Ticker(ticker).info
                            company_name = info.get("longName", ticker)
                        except Exception:
                            company_name = ticker

                        await channel.send(
                            f"<@{user_id}> Alert! **{company_name} ({ticker})** "
                            f"is {last_price:.2f} ({operator} {value})"
                        )

                        alert_list.remove(alert)
                        save_alerts(alerts)

                except Exception as e:
                    print(f"Error in check_alerts for {alert}: {e}")
                    continue

            await asyncio.sleep(1) 

async def setup(bot):
    await bot.add_cog(AlertTask(bot))
