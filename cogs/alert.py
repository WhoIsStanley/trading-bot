import discord
from discord import app_commands
from discord.ext import commands
import yfinance as yf
from datetime import datetime
from alert_update import alerts, save_alerts, yahoo_search

class YahooSearchView(discord.ui.View):
    def __init__(self, results, user, operator, value, end_date):
        super().__init__(timeout=30)
        self.results = results
        self.user = user
        self.operator = operator
        self.value = value
        self.end_date = end_date

        # Create one button per search result
        for r in results:
            label = f"{r['symbol']} - {r.get('shortname','')}"
            self.add_item(
                discord.ui.Button(
                    label=label[:80],  # Discord max = 80 chars
                    style=discord.ButtonStyle.primary,
                    custom_id=r["symbol"]
                )
            )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message("This menu is not for you.", ephemeral=True)
            return False

        chosen_symbol = interaction.data["custom_id"]
        match = next((r for r in self.results if r["symbol"] == chosen_symbol), None)
        if not match:
            return False

        # Save alert when user picks a symbol
        alert_data = {
            "ticker": match["symbol"].upper(),
            "operator": self.operator,
            "value": float(self.value),
            "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
            "channel": interaction.channel.id,
            "user_id": interaction.user.id
        }
        alerts.setdefault(str(interaction.channel.id), []).append(alert_data)
        save_alerts()

        await interaction.response.edit_message(
            content=f":rotating_light: Alert set for <@{interaction.user.id}>: "
                    f"**{match.get('shortname', match['symbol'])} ({match['symbol']})** "
                    f"{self.operator} {self.value} until {self.end_date or 'no limit'}",
            embed=None,
            view=None
        )
        self.stop()
        return True

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("This menu is not for you.", ephemeral=True)
            return
        await interaction.response.edit_message(content=":exclamation: Alert creation canceled.", embed=None, view=None)
        self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True


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
                await interaction.response.send_message(":x: Invalid date format. Use YYYY-MM-DD.", ephemeral=True)
                return

        company_name = None
        try:
            info = yf.Ticker(ticker).info
            # Detect the "useless dict" case
            if not info or list(info.keys()) == ["trailingPegRatio"] or not info.get("regularMarketPrice"):
                raise ValueError("Invalid ticker response from yfinance")

            company_name = info.get("longName", ticker.upper())
        except Exception:
            # Fallback to Yahoo search
            results = yahoo_search(ticker, count=5)
            if not results:
                await interaction.response.send_message(f":x: Could not find ticker `{ticker}`.", ephemeral=True)
                return

            # Show user options
            embed = discord.Embed(
                title="Did you mean one of these?",
                description="\n".join(
                    [f"**{r['symbol']}** - {r.get('shortname','')} ({r['exchange']}, {r['type']})"
                    for r in results]
                ),
                color=discord.Color.orange()
            )
            view = YahooSearchView(results, interaction.user, operator, value, end_dt)

            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            return

        # Save alert directly if ticker was valid
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
            f":rotating_light: Alert set for <@{interaction.user.id}>: **{company_name} ({ticker.upper()})** "
            f"{operator} {value} until {end_date or 'no limit'}"
        )


async def setup(bot):
    await bot.add_cog(AlertCog(bot))
