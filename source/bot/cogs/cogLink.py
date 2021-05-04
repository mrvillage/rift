import discord
import asyncio
import json
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level


class Link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="link", aliases=["verify"], help="Links your Politics and War nation to your Discord account.", case_insensitive=True)
    async def link(self, ctx, nation, user: discord.Member = None):
        try:
            if "politicsandwar" in nation:
                nation_id = int(nation.strip(
                    "/\\").replace("https://politicsandwar.com/nation/id=", ""))
            else:
                nation_id = int(nation)
        except ValueError:
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"`{nation_id}` is not a valid nation!"))
            return
        if user == None:
            user = ctx.author
            user_id = ctx.author.id
        else:
            user_id = user.id
        links = await rift.get_links(self.bot.connection)
        if any(user_id in tuple(i) for i in links):
            await ctx.send(embed=rift.get_embed_author_member(user, f"<@!{user_id}> is already linked!"))
            return
        if any(user_id in tuple(i) for i in links):
            await ctx.send(embed=rift.get_embed_author_member(user, f"Nation {nation_id} is already linked!"))
            return
        await rift.add_link(self.bot.connection, user_id, nation_id)
        await ctx.send(embed=rift.get_embed_author_member(user, f"<@!{user_id}> is now linked to nation {nation_id}!"))


def setup(bot):
    bot.add_cog(Link(bot))
