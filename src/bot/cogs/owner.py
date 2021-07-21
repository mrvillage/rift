import asyncio
from typing import Union

import discord
from discord.ext import commands

from ... import funcs as rift
from ...data.classes import Alliance
from ...data.db import execute_query
from ...data.query import get_alliances
from ...errors import NationNotFoundError


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: rift.Rift):
        self.bot = bot

    async def cog_check(self, ctx):  # pylint: disable=invalid-overridden-method
        return await self.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        if not isinstance(error, commands.CheckFailure):
            await rift.handler(ctx, error)

    @commands.command(name="unlink", aliases=["unverify", "remove-link", "removelink"])
    async def unlink(self, ctx, arg):
        nation = await rift.search_nation(ctx, arg)
        link = await rift.get_link_nation(nation.id)
        await rift.remove_link_nation(nation.id)
        user = await commands.UserConverter().convert(ctx, str(link[0]))
        await ctx.send(
            embed=rift.get_embed_author_member(
                user, f"{user.mention} has been unlinked from nation `{nation.id}`."
            )
        )

    @commands.command(name="force-link", aliases=["force-verify"])
    async def force_link(
        self, ctx, nation, user: Union[discord.Member, discord.User] = None
    ):
        try:
            nation = await rift.search_nation(ctx, nation)
        except NationNotFoundError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"No nation found with argument `{nation}`."
                )
            )
            return
        user = ctx.author if user is None else user
        links = await rift.get_links()
        if any(user.id in tuple(i) for i in links):
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    user, f"{user.mention} is already linked!"
                )
            )
            return
        if any(user.id in tuple(i) for i in links):
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    user, f"Nation `{nation.id}` is already linked!"
                )
            )
            return
        await ctx.reply(
            embed=rift.get_embed_author_member(
                user,
                f"Success! {user.mention} is now linked to nation `{nation.id}`!",
            )
        )

    @commands.group(name="extension", invoke_without_command=True)
    async def extension(self, ctx):
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, "You forgot to give a subcommand!"
            )
        )

    @extension.command(name="reload")
    async def extension_reload(self, ctx, *, extension):
        try:
            self.bot.reload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` has been reloaded."
                )
            )
        except commands.ExtensionNotLoaded:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` is not loaded."
                )
            )
        except commands.ExtensionNotFound:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` does not exist."
                )
            )

    @extension.command(name="load")
    async def extension_load(self, ctx, *, extension):
        try:
            self.bot.load_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` has been loaded."
                )
            )
        except commands.ExtensionAlreadyLoaded:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` is already loaded."
                )
            )
        except commands.ExtensionNotFound:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` does not exist."
                )
            )

    @extension.command(name="unload")
    async def extension_unload(self, ctx, *, extension):
        try:
            self.bot.unload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` has been unloaded."
                )
            )
        except commands.ExtensionNotLoaded:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` is not loaded."
                )
            )
        except commands.ExtensionNotFound:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Extension `{extension}` does not exist."
                )
            )

    @commands.group(name="staff", invoke_without_command=True)
    async def staff(self, ctx):
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, "You forgot to give a subcommand!"
            )
        )

    @staff.command(name="add")
    async def staff_add(self, ctx, member: discord.Member):
        staff = await self.bot.get_staff()
        if member.id in staff:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"{member.mention} is already Staff."
                )
            )
            return
        await execute_query("INSERT INTO staff VALUES ($1);", member.id)
        self.bot.staff.append(member.id)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, f"{member.mention} is now Staff."
            )
        )

    @staff.command(name="remove")
    async def staff_remove(self, ctx, member: discord.Member):
        staff = await self.bot.get_staff()
        if member.id not in staff:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"{member.mention} is not Staff."
                )
            )
            return
        await execute_query("DELETE FROM staff WHERE id = $1;", member.id)
        self.bot.staff.remove(member.id)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, f"{member.mention} has been removed from Staff."
            )
        )

    @staff.command(name="list")
    async def staff_list(self, ctx):
        staff = await self.bot.get_staff()
        staff = [await self.bot.fetch_user(s) for s in staff]
        staff = [i for i in staff if i is not None]
        mentions = "\n".join(i.mention for i in staff)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, f"There are {len(staff):,} Staff:\n{mentions}"
            )
        )

    @commands.command(name="server-dump")
    async def server_dump(self, ctx, purge=0):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        if purge > 0:
            await ctx.channel.purge(limit=purge)
        message = await ctx.send("Fetching...")
        invites = []
        alliances = [Alliance(tuple(i)) for i in await get_alliances()]
        for alliance in alliances:
            try:
                if alliance.discord is None:
                    continue
                await self.bot.fetch_invite(alliance.discord)
                invites.append(alliance)
            except discord.NotFound:
                pass
            await asyncio.sleep(1)
        try:
            await message.delete()
        except discord.Forbidden:
            pass
        for invite in invites:
            await ctx.send(
                f"**{invite.name} ({invite.acronym} - {invite.id})**\n{invite.discord}"
            )
            await asyncio.sleep(1)
        await ctx.send("Servers sent!")

    @commands.command(name="gib")
    @commands.is_owner()
    async def gib(self, ctx):
        if ctx.guild.id == 654109011473596417 and ctx.author.id == 258298021266063360:
            role = ctx.guild.get_role(809556716780912734)
            await ctx.author.add_roles(role)

    @commands.command(name="discs")
    @commands.is_owner()
    async def discs(self, ctx):
        alliance = await Alliance.fetch(7719)
        await alliance.make_attrs("members")
        for nat in alliance.members:
            await nat.make_attrs("user")
        discs = [i.user.mention for i in alliance.members if i.user is not None]
        no_disc = [str(i.id) for i in alliance.members if i.user is None]
        await ctx.send(", ".join(discs))
        await ctx.send(", ".join(no_disc))


def setup(bot: rift.Rift):
    bot.add_cog(Owner(bot))
