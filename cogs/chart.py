import discord
from discord import app_commands
from discord.ext import commands
from utils import StockChart
import os

class ChartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command
    @app_commands.command(name="chart", description="Polting a stock chart")
    async def chart_slash(self, interaction: discord.Interaction, ticker: str):
        if not ticker:
            await interaction.response.send_message(":x: You need to provide a ticker.")
            return
        await self.chart_handler(interaction, ticker.upper(), slash=True)

    # Prefix command
    @commands.command(name="chart", aliases=['c'])
    async def chart_prefix(self, ctx: commands.Context, ticker: str = None):
        if not ticker:
            await ctx.send(":x: You need to provide a ticker.")
            return
        await self.chart_handler(ctx, ticker.upper(), slash=False)

    # Shared logic
    async def chart_handler(self, source, ticker, slash):
        chart = StockChart(
            ticker=ticker
        )
        fig_file = chart.plot()

        base_dir = os.path.dirname(os.path.dirname(__file__))
        fig_path = os.path.join(base_dir, fig_file)
        file = discord.File(fig_path, filename=f"{ticker}.png")

        embed = discord.Embed(
                title=f"{ticker}",
                color=discord.Color.yellow()
            )
        embed.set_image(url=f"attachment://{ticker}.png")

        if slash:
            await source.response.send_message(embed=embed, file=file, ephemeral=True)
        else:
            await source.send(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(ChartCog(bot))
