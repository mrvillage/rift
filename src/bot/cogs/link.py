from __future__ import annotations

import discord
from discord.ext import commands

from ... import funcs
from ...data.classes import Nation
from ...ref import Rift


class Link(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.command(
        name="link",
        aliases=["verify", "validate"],
        brief="Link a nation to a Discord account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "nation": "The nation to link.",
            "discord": "The Discord account to link, defaults to your account.",
        },
    )
    async def link(
        self, ctx: commands.Context, nation: Nation, user: discord.User = None
    ):
        member = user or ctx.author
        try:
            await funcs.get_link_user(member.id)
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{member.mention} is already linked!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        except IndexError:
            pass
        try:
            await funcs.get_link_nation(nation.id)
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{repr(nation)} is already linked!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        except IndexError:
            pass
        await ctx.interaction.response.defer(ephemeral=True)
        try:
            name = await nation.get_discord_page_username()
            if name != f"{member.name}#{member.discriminator}":
                raise IndexError
            await funcs.add_link(member.id, nation.id)
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    member,
                    f"Success! {member.mention} is now linked to {repr(nation)}!",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        except IndexError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    member,
                    f"""
                The Discord username on your nation page doesn't match the one on your account!
                Head down to https://politicsandwar.com/nation/edit/ and scroll to the very bottom where it says "Discord Username:" and put `{member.name}#{member.discriminator}` in the space, hit Save Changes and run the command again!
                """,
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )


def setup(bot: Rift):
    bot.add_cog(Link(bot))
