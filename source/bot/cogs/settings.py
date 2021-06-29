from discord.ext import commands

from ... import funcs as rift


class Settings(commands.Cog):
    def __init__(self, bot: rift.Rift):
        self.bot = bot

    @commands.group(
        name="user-settings", aliases=["usersettings"], invoke_without_command=True
    )
    async def user_settings(self, ctx):
        pass

    @commands.group(
        name="server-settings", aliases=["serversettings"], invoke_without_command=True
    )
    async def server_settings(self, ctx):
        pass


def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))
