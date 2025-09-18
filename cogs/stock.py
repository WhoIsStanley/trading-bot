import discord
from discord import app_commands
from discord.ext import commands
import yfinance as yf
from utils import yahoo_search
import os

def logo_finder(info):
    logo_url = info.get("logo_url")

    if not logo_url and "website" in info:
        domain = info["website"].split("/")[2] 
        logo_url = f"https://logo.clearbit.com/{domain}"
    
    return logo_url

def get_stock_info(info): 
    try:
        # Price Handling
        price = info.get("regularMarketPrice")
        change = info.get("regularMarketChange")
        change_pct = info.get("regularMarketChangePercent")

        if info.get("preMarketPrice"):
            price = info.get("preMarketPrice")
            change = info.get("preMarketChange")
            change_pct = info.get("preMarketChangePercent")
        elif info.get("postMarketPrice"):
            price = info.get("postMarketPrice")
            change = info.get("postMarketChange")
            change_pct = info.get("postMarketChangePercent")

        return {
            "Current Price": price,
            "Company Name": info.get("longName"),
            "Price Change": change,
            "Price Change %": change_pct,
            "Volume": info.get("regularMarketVolume"),
            "Open": info.get("regularMarketOpen"),
            "Prev. Close": info.get("regularMarketPreviousClose"),
            "52-wk High": info.get("fiftyTwoWeekHigh"),
            "52-wk Low": info.get("fiftyTwoWeekLow"),
            "P/E Ratio": info.get("trailingPE"),
            "EPS": info.get("trailingEps"),
        }

    except Exception as e:
        print(f"Error fetching data for {info.get('symbol')}: {e}")
        return None
    
def embed_maker(info,ticker):
    ticker_info = get_stock_info(info)
    logo = logo_finder(info)
    if logo == None:
        logo = "attachment://yahoo.png"

    embed = discord.Embed(
        title=f"{ticker_info['Current Price']:.2f} | {ticker_info['Price Change']:.2f} | {ticker_info['Price Change %']:.2f}%",
        color=discord.Color.green()
    )
    
    embed.set_author(
        name=f"{ticker_info['Company Name']} ({ticker.upper()})",   
        icon_url=logo 
    )

    embed.add_field(name="Volume", value=f"{ticker_info['Volume']:,}", inline=True)
    embed.add_field(name="Open", value=ticker_info['Open'], inline=True)
    embed.add_field(name="Prev. Close", value=ticker_info['Prev. Close'], inline=True)
    embed.add_field(name="52-wk High", value=ticker_info['52-wk High'], inline=True)
    embed.add_field(name="52-wk Low", value=ticker_info['52-wk Low'], inline=True)
    embed.add_field(name="P/E Ratio", value=ticker_info['P/E Ratio'], inline=True)
    embed.add_field(name="EPS", value=ticker_info['EPS'], inline=True)

    embed.set_footer(
        text="Data from Yahoo Finance",
        icon_url="attachment://yahoo.png"
    )

    base_dir = os.path.dirname(os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, "yahoo-finance.png")
    file = discord.File(icon_path, filename="yahoo.png")

    return embed, file
    
# Searching ticker by embed message (wrong typing)
class YahooSearchView(discord.ui.View):
    def __init__(self, results, user):
        super().__init__(timeout=30)
        self.results = results
        self.user = user

        # Create one button per search result
        for r in results:
            label = f"{r['symbol']} - {r.get('shortname','')}"
            button = discord.ui.Button(
                label=label[:80],
                style=discord.ButtonStyle.primary,
                custom_id=r["symbol"]
            )
            button.callback = self.make_callback(r) 
            self.add_item(button)

    def make_callback(self, result):
        async def callback(interaction: discord.Interaction):
            if interaction.user != self.user:
                await interaction.response.send_message("This menu is not for you.", ephemeral=True)
                return
            
            info = yf.Ticker(result['symbol']).info
            embed,file = embed_maker(info,result['symbol'])

            await interaction.response.edit_message(embed=embed, view=None, attachments=[file])
            self.stop()

        return callback

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("This menu is not for you.", ephemeral=True)
            return
        await interaction.response.edit_message(content=":exclamation: Stock creation canceled.", embed=None, view=None)
        self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True


class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command
    @app_commands.command(name="stock", description="Finding stock information")
    async def stock_price_slash(self, interaction: discord.Interaction, ticker: str):
        if not ticker:
            await interaction.response.send_message(":x: You need to provide a ticker.")
            return
        await self.handle_stock(interaction, ticker, slash=True)

    # Prefix command
    @commands.command(name="stock", aliases=["s"])
    async def stock_price_prefix(self, ctx: commands.Context, ticker: str = None):
        if not ticker:
            await ctx.send(":x: You need to provide a ticker.")
            return
        await self.handle_stock(ctx, ticker, slash=False)

    # Shared logic
    async def handle_stock(self, source, ticker: str, slash: bool):
        try:
            info = yf.Ticker(ticker).info
            if not info or list(info.keys()) == ["trailingPegRatio"] or not info.get("regularMarketPrice"):
                raise ValueError("Invalid ticker response from yfinance")
        except Exception:
            results = yahoo_search(ticker, count=5)
            if not results:
                if slash:
                    await source.response.send_message(f":x: Could not find ticker `{ticker}`.", ephemeral=True)
                else:
                    await source.send(f":x: Could not find ticker `{ticker}`.")
                return

            embed = discord.Embed(
                title="Search Results",
                description="\n".join(
                    [f"**{r['symbol']}** - {r.get('shortname','')} ({r['exchange']}, {r['type']})"
                     for r in results]
                ),
                color=discord.Color.yellow()
            )
            view = YahooSearchView(results, source.user if slash else source.author)

            if slash:
                await source.response.send_message(embed=embed, view=view, ephemeral=True)
            else:
                await source.send(embed=embed, view=view)
            return

        embed, file = embed_maker(info,ticker)

        if slash:
            await source.response.send_message(embed=embed, ephemeral=True, file=file)
        else:
            await source.send(embed=embed,file=file)


async def setup(bot):
    await bot.add_cog(StockCog(bot))
