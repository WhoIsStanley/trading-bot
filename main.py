import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands, tasks
import yfinance as yf
from datetime import datetime
import json, os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

ALERTS_FILE = "alerts.json"

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_alerts(data):
    with open(ALERTS_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

alerts = load_alerts()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    synced = await tree.sync(guild=discord.Object(id=os.getenv("GULID_ID")))
    print(f"Synced {len(synced)} global slash commands")
    check_alerts.start()

@tree.command(name="list", description="List your alerts in this channel")
async def list_alert(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = str(interaction.channel_id)

    if channel_id not in alerts or not alerts[channel_id]:
        await interaction.response.send_message("You have no alerts in this channel.")
        return

    user_alerts = [
        (i, a) for i, a in enumerate(alerts[channel_id]) if a["user_id"] == user_id
    ]

    if not user_alerts:
        await interaction.response.send_message("You have no alerts in this channel.")
        return

    msg_lines = []
    for i, a in user_alerts:
        msg_lines.append(
            f"**ID {i}:** {a['ticker']} {a['operator']} {a['value']} until {a['end_date'] or 'no limit'}"
        )

    await interaction.response.send_message("\n".join(msg_lines))


@tree.command(name="delete", description="Delete one of your alerts by ID")
async def delete_alert(interaction: discord.Interaction, alert_id: int):
    user_id = interaction.user.id
    channel_id = str(interaction.channel_id)

    if channel_id not in alerts or alert_id >= len(alerts[channel_id]):
        await interaction.response.send_message("Invalid alert ID.")
        return

    alert = alerts[channel_id][alert_id]
    if alert["user_id"] != user_id:
        await interaction.response.send_message("You can only delete your own alerts.")
        return

    removed = alerts[channel_id].pop(alert_id)
    save_alerts(alerts)

    await interaction.response.send_message(
        f"Deleted alert: {removed['ticker']} {removed['operator']} {removed['value']}"
    )


@tree.command(name="alert", description="Set a stock price alert")
async def set_alert(interaction: discord.Interaction, ticker: str, operator: str, value: float, end_date: str = None):
    end_dt = None
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            await interaction.response.send_message("Invalid date format. Use YYYY-MM-DD.")
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
        "channel": interaction.channel_id,
        "user_id": interaction.user.id
    }

    alerts.setdefault(str(interaction.channel_id), []).append(alert_data)
    save_alerts(alerts)

    await interaction.response.send_message(
        f"Alert set for <@{interaction.user.id}>: **{company_name} ({ticker.upper()})** {operator} {value} until {end_date or 'no limit'}"
    )

@bot.command(name="list")
async def list_alert(ctx):
    """List all alerts for the current user in this channel"""
    user_id = ctx.author.id
    channel_id = str(ctx.channel.id)

    if channel_id not in alerts or not alerts[channel_id]:
        await ctx.send("You have no alerts in this channel.")
        return

    user_alerts = [
        (i, a) for i, a in enumerate(alerts[channel_id]) if a["user_id"] == user_id
    ]

    if not user_alerts:
        await ctx.send("You have no alerts in this channel.")
        return

    msg_lines = []
    for i, a in user_alerts:
        msg_lines.append(
            f"**ID {i}:** {a['ticker']} {a['operator']} {a['value']} until {a['end_date'] or 'no limit'}"
        )

    await ctx.send("\n".join(msg_lines))


@bot.command(name="delete")
async def delete_alert(ctx, alert_id: int):
    """Delete one of your alerts by ID (use !myalerts to see IDs)"""
    user_id = ctx.author.id
    channel_id = str(ctx.channel.id)

    if channel_id not in alerts or alert_id >= len(alerts[channel_id]):
        await ctx.send("? Invalid alert ID.")
        return

    alert = alerts[channel_id][alert_id]
    if alert["user_id"] != user_id:
        await ctx.send("? You can only delete your own alerts.")
        return

    removed = alerts[channel_id].pop(alert_id)
    save_alerts(alerts)

    await ctx.send(
        f"Deleted alert: {removed['ticker']} {removed['operator']} {removed['value']}"
    )

@bot.command(name="alert")
async def set_alert(ctx, ticker: str, operator: str, value: float, end_date: str = None):
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
    save_alerts(alerts)

    await ctx.send(
        f"Alert set for <@{ctx.author.id}>: **{company_name} ({ticker.upper()})** {operator} {value} until {end_date or 'no limit'}"
    )

@tasks.loop(seconds=10)
async def check_alerts():
    now = datetime.now()

    for channel_id, alert_list in list(alerts.items()):
        channel = bot.get_channel(int(channel_id))
        if not channel:
            continue

        for alert in alert_list[:]:
            ticker = alert["ticker"]
            operator = alert["operator"]
            value = alert["value"]
            end_date = alert["end_date"]
            user_id = alert["user_id"]

            if end_date and now > datetime.strptime(end_date, "%Y-%m-%d"):
                await channel.send(f"Alert expired for <@{user_id}> ({ticker})")
                alert_list.remove(alert)
                save_alerts(alerts)
                continue

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
                    f"<@{user_id}> Alert! **{company_name} {ticker}** is {last_price:.2f} ({operator} {value})"
                )
                alert_list.remove(alert)
                save_alerts(alerts)

bot.run(os.getenv("TOKEN"))

