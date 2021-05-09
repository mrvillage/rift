import discord
from asyncio import TimeoutError
import json
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level
from ... import find  # pylint: disable=relative-beyond-top-level


class Link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="link", aliases=["verify"], help="Links your Politics and War nation to your Discord account.", case_insensitive=True)
    async def link(self, ctx, nation, user: discord.Member = None):
        nation = await rift.search_nation(ctx, nation)
        user = ctx.author if user is None else user
        links = await rift.get_links(self.bot.connection)
        if any(user.id in tuple(i) for i in links):
            await ctx.reply(embed=rift.get_embed_author_member(user, f"{user.mention} is already linked!"))
            return
        if any(user.id in tuple(i) for i in links):
            await ctx.reply(embed=rift.get_embed_author_member(user, f"Nation `{nation.id}` is already linked!"))
            return
        await ctx.reply(embed=rift.get_embed_author_member(user, f"A verification code has been send via in-game message to nation `{nation.id}`. Please send the code within the next ten minutes to complete verification."))
        code = await rift.generate_code()
        await nation.send_message(subject="Rift Verification", content=f"Your verification code is:\n\n{code}")
        def check(message):
            return message.author.id == user.id and message.channel.id == ctx.channel.id and code in message.content
        try:
            message = await self.bot.wait_for("message", check=check, timeout=30)
        except TimeoutError:
            await ctx.reply(embed=rift.get_embed_author_member(user, f"Verification timed out."))
            return
        await rift.add_link(user.id, nation.id)
        await message.reply(embed=rift.get_embed_author_member(user, f"Success! {user.mention} is now linked to nation `{nation.id}`!"))


def setup(bot):
    bot.add_cog(Link(bot))
