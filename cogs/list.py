import discord
from discord import app_commands
from discord.ext import commands
from utils import alerts

class Paginator(discord.ui.View):
    def __init__(self, entries, per_page=10):
        super().__init__(timeout=60)  # auto-disable after 60s of no use
        self.entries = entries
        self.per_page = per_page
        self.current_page = 0

    def format_page(self):
        start = self.current_page * self.per_page
        end = start + self.per_page
        page_entries = self.entries[start:end]

        embed = discord.Embed(
            title=f":bar_chart: Your Alerts (Page {self.current_page + 1}/{self.total_pages})",
            color=discord.Color.blue()
        )

        if not page_entries:
            embed.description = "No alerts on this page."
        else:
            lines = []
            for i, a in page_entries:
                lines.append(
                    f"ID {i:<3} | {a['ticker']:<6} {a['operator']} {a['value']:<8} until {a['end_date'] or 'no limit'}"
                )

        embed.description = "```\n" + "\n".join(lines) + "\n```"

        return embed

    @property
    def total_pages(self):
        return max(1, (len(self.entries) + self.per_page - 1) // self.per_page)

    async def update_message(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.format_page(), view=self)

    @discord.ui.button(label="\u2B05\ufe0f Previous", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
        await self.update_message(interaction)

    @discord.ui.button(label="Next \u27A1\ufe0f", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        await self.update_message(interaction)


class ListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command
    @app_commands.command(name="list", description="List your alerts in this channel")
    async def list_alert_slash(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        channel_id = str(interaction.channel_id)

        if channel_id not in alerts or not alerts[channel_id]:
            await interaction.response.send_message("You have no alerts in this channel.", ephemeral=True)
            return

        user_alerts = [(i, a) for i, a in enumerate(alerts[channel_id]) if a["user_id"] == user_id]

        if not user_alerts:
            await interaction.response.send_message("You have no alerts in this channel.", ephemeral=True)
            return

        view = Paginator(user_alerts, per_page=10)
        await interaction.response.send_message(embed=view.format_page(), view=view, ephemeral=True)

    # Prefix command
    @commands.command(name="list")
    async def list_alert_prefix(self, ctx: commands.Context):
        user_id = ctx.author.id
        channel_id = str(ctx.channel.id)

        if channel_id not in alerts or not alerts[channel_id]:
            await ctx.send("You have no alerts in this channel.")
            return

        user_alerts = [(i, a) for i, a in enumerate(alerts[channel_id]) if a["user_id"] == user_id]

        if not user_alerts:
            await ctx.send("You have no alerts in this channel.")
            return

        view = Paginator(user_alerts, per_page=10)
        await ctx.send(embed=view.format_page(), view=view)


async def setup(bot):
    await bot.add_cog(ListCog(bot))
