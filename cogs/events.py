from discord.ext import commands

from classes.bot import Bot


class Events(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # for demo purposes
    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog is ready")


async def setup(bot: Bot):
    await bot.add_cog(Events(bot))
