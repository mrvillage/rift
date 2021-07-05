from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="toot")
    async def link(self, ctx):
        await ctx.send("Toot tooooooot!")


def setup(bot):
    bot.add_cog(Fun(bot))
