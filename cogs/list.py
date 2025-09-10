import discord
from discord import app_commands
from discord.ext import commands
from alert_update import alerts, save_alerts, load_alerts

class ListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #slash command
    @app_commands.command(name="list", description="List your alerts in this channel")
    async def list_alert(self, interaction: discord.Interaction):
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

    #prefix
    @commands.command(name="list")
    async def list_alert_prefix(self, ctx):
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
        

async def setup(bot):
    await bot.add_cog(ListCog(bot))