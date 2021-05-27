
import discord
from discord.ext import commands
from ... import funcs as rift
from ...errors import NationNotFoundError


class Link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="link", aliases=["verify"], help="Links your Politics and War nation to your Discord account.")
    async def link(self, ctx, nation, user: Union[discord.Member, discord.User] = None):
        try:
            nation = await rift.search_nation(ctx, nation)
        except NationNotFoundError:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"No nation found with argument `{nation}`."))
            return
        user = ctx.author if user is None else user
        links = await rift.get_links()
        if any(user.id in tuple(i) for i in links):
            await ctx.reply(embed=rift.get_embed_author_member(user, f"{user.mention} is already linked!"))
            return
        if any(user.id in tuple(i) for i in links):
            await ctx.reply(embed=rift.get_embed_author_member(user, f"Nation `{nation.id}` is already linked!"))
            return
        try:
            message = await ctx.reply(embed=rift.get_embed_author_member( user, "Fetching Discord username..."))
            name = await nation.get_discord_page_username()
            if name == f"{user.name}#{user.discriminator}":
                await rift.add_link(user.id, nation.id)
                await message.edit(embed=rift.get_embed_author_member(user, f"Success! {user.mention} is now linked to nation `{nation.id}`!"))
            else:
                await message.edit(embed=rift.get_embed_author_member(
                    user,
                    f"""
                    The Discord username on your nation page doesn't match the one on your account!
                    Head down to https://politicsandwar.com/nation/edit/ and scroll to the very bottom where it says "Discord Username:" and put `{user.name}#{user.discriminator}` in the space, hit Save Changes and run the command again!
                    """
                ))
        except IndexError:
            await message.edit(embed=rift.get_embed_author_member(
                user,
                f"""
                The Discord username on your nation page doesn't match the one on your account!
                Head down to https://politicsandwar.com/nation/edit/ and scroll to the very bottom where it says "Discord Username:" and put `{user.name}#{user.discriminator}` in the space, hit Save Changes and run the command again!
                """
            ))


def setup(bot):
    bot.add_cog(Link(bot))
