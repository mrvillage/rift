import discord
import asyncio
import json
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", help="Gets information about the user.", case_insensitive=True)
    async def user_info(self, ctx, user=None):
        if user == None:
            user = ctx.author
        else:
            user = await commands.MemberConverter().convert(ctx, user)
        await ctx.send(embed=rift.get_embed_author_member(ctx.author, f""))

    @user_info.error
    async def user_info_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"I couldn't find that member!"))


def setup(bot):
    bot.add_cog(Info(bot))