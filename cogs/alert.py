import discord
from discord import app_commands
from discord.ext import commands
import yfinance as yf
from datetime import datetime
from alert_update import alerts, save_alerts

class AlertCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command
    @app_commands.command(name="alert", description="Set a stock alert")
    async def set_alert(self, interaction: discord.Interaction, ticker: str, operator: str, value: float, end_date: str = None):
        end_dt = None
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                await interaction.response.send_message("Invalid date format. Use YYYY-MM-DD.")
                return

        try:
            info = yf.Ticker(ticker).info
            company_name = info.get("longName", ticker.upper())
        except Exception:
            company_name = ticker.upper()

        alert_data = {
            "ticker": ticker.upper(),
            "operator": operator,
            "value": float(value),
            "end_date": end_dt.strftime("%Y-%m-%d") if end_dt else None,
            "channel": interaction.channel_id,
            "user_id": interaction.user.id
        }

        alerts.setdefault(str(interaction.channel_id), []).append(alert_data)
        save_alerts()

        await interaction.response.send_message(
            f"Alert set for <@{interaction.user.id}>: **{company_name} ({ticker.upper()})** {operator} {value} until {end_date or 'no limit'}"
        )

    @commands.command(name="alert")
    async def set_alert(self, ctx, ticker: str, operator: str, value: float, end_date: str = None):
        end_dt = None
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                await ctx.send("Invalid date format. Use YYYY-MM-DD.")
                return
        
        # Try to fetch company name
        try:
            info = yf.Ticker(ticker).info
            company_name = info.get("longName", ticker.upper())
        except Exception:
            company_name = ticker.upper()

        alert_data = {
            "ticker": ticker.upper(),
            "operator": operator,
            "value": float(value),
            "end_date": end_dt.strftime("%Y-%m-%d") if end_dt else None,
            "channel": ctx.channel.id,
            "user_id": ctx.author.id
        }

        alerts.setdefault(str(ctx.channel.id), []).append(alert_data)
        save_alerts()

        await ctx.send(
            f"Alert set for <@{ctx.author.id}>: **{company_name} ({ticker.upper()})** {operator} {value} until {end_date or 'no limit'}"
        )
    

async def setup(bot):
    await bot.add_cog(AlertCog(bot))
