import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command
    @app_commands.command(name="help", description="A manual about trading-bot command")
    async def help_slash(self, interaction: discord.Interaction):
        await self.help_handler(interaction, slash=True)

    # Prefix command
    @commands.command(name="help", aliases=['h'])
    async def help_prefix(self, ctx: commands.Context):
        await self.help_handler(ctx, slash=False)

    # Shared logic
    async def help_handler(self, source, slash):

        embed = discord.Embed(
                title="# Trading-bot Commands",
                description="## Stock Stats\n" \
                "/stock or `!s`/`!stock` follow by a ticker.\n" \
                "```!s VOO | !stock VOO```" \
                "\n" \
                "\n" \
                "## Alert Setting\n" \
                "/alert follow by ticker, operator, value, where end date is optional.\n" \
                "```/alert ticker: VOO operator: > value: 300 end_date: 2030-01-01```" \
                "\n" \
                "-# the date format must be `YYYY-MM-DD`" \
                "\n" \
                "/list or `!list` can show the alerts that have been set\n" \
                "\n" \
                "/delete or `!delete` follow by the alert's ID, shown by list command\n" \
                "```!delete 0```",
                color=discord.Color.yellow()
            )

        if slash:
            await source.response.send_message(embed=embed, ephemeral=True)
        else:
            await source.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
