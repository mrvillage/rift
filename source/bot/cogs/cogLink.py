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
        if any(True for i in links if user_id in i):
            await ctx.send(embed=rift.get_embed_author_member(user, f"<@!{user_id}> is already linked!"))
            return
        if any(True for i in links if nation_id in i):
            await ctx.send(embed=rift.get_embed_author_member(user, f"Nation {nation_id} is already linked!"))
            return
        await rift.add_link(self.bot.connection, user_id, nation_id)
        await ctx.send(embed=rift.get_embed_author_member(user, f"<@!{user_id}> is now linked to nation {nation_id}!"))

    @commands.command(name="!?unlink", verify=["!?unverify", "!?remove-link", "!?removelink"], hidden=True)
    @commands.is_owner()
    async def unlink(self, ctx, arg):
        try:
            user = await commands.MemberConverter().convert(ctx, arg)
            user_id = user.id
            try:
                nation_id = (await rift.get_link_user(self.bot.connection, user_id))[1]
            except:
                await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"<@{user_id}> is not linked."))
                return
        except:
            try:
                if "politicsandwar" in arg:
                    if "http" in arg:
                        arg = arg.replace("https://", "")
                    nation_id = int(
                        arg.strip("/\\").replace("politicsandwar.com/nation/id=", ""))
                else:
                    nation_id = int(arg)
                try:
                    link = await rift.get_link_nation(self.bot.connection, nation_id)
                    user_id = link[1]
                except:
                    await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"`{nation_id}` is not linked!"))
            except ValueError:
                await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"`{arg}` is not a valid argument!"))
                return
        await rift.remove_link_nation(self.bot.connection, nation_id)
        await ctx.send(embed=rift.get_embed_author_member(user, f"<@{user_id}> has been unlinked from nation `{nation_id}`."))

    @link.error
    async def link_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"That member couldn't be found!"))
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"You forgot to give the nation to link!"))


def setup(bot):
    bot.add_cog(Link(bot))
