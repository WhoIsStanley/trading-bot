import discord
from discord import app_commands
from discord.ext import commands
from alert_update import alerts, save_alerts

class DeleteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash Command
    @app_commands.command(name="delete", description="Delete one of your alerts by ID")
    async def delete_alert(self, interaction: discord.Interaction, alert_id: int):
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
        save_alerts()

        await interaction.response.send_message(
            f"Deleted alert: {removed['ticker']} {removed['operator']} {removed['value']}"
        )
    
    # Prefix
    @commands.command(name="delete")
    async def delete_alert_prefix(self, ctx, alert_id: int):
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
        save_alerts()

        await ctx.send(
            f"Deleted alert: {removed['ticker']} {removed['operator']} {removed['value']}"
        )

async def setup(bot):
    await bot.add_cog(DeleteCog(bot))



