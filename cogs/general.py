from discord import (
    Embed,
    Interaction,
    app_commands,
)
from discord.ext.commands import (
    Cog,
)

from classes.bot import Bot


class General(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: Interaction):
        embed = Embed(title="🏓 Pong!")
        embed.add_field(name="", value=f"{interaction.client.latency * 1000:.0f}ms")

        await interaction.response.send_message(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(General(bot))
