from discord import (
    Embed,
    Interaction,
    app_commands,
)
from discord.ext.commands import (
    Cog,
)

from classes.bot import Bot


class LevelingRule(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    group = app_commands.Group(name="rule", description="group")

    @group.command(name="get", description="get rule")
    async def getRule(self, interaction: Interaction):
        return await interaction.response.send_message("getrule")
    
    @group.command(name="set", description="set rule")
    @app_commands.describe(rule="The rule/formula for the leveling system.", )
    async def setRule(self, interaction: Interaction, rule: str):
        return await interaction.response.send_message(f"setrule - {rule}")

async def setup(bot: Bot):
    await bot.add_cog(LevelingRule(bot))
