import asyncio
from typing import Union

import discord
from discord.ext import commands

from ... import funcs
from ...data.classes import Alliance, Nation
from ...data.query import query_alliances
from ...ref import Rift


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: Rift):
        self.bot = bot

    async def cog_check(self, ctx):  # pylint: disable=invalid-overridden-method
        return await self.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        if not isinstance(error, commands.CheckFailure):
            await funcs.handler(ctx, error)

    @commands.command(name="unlink", aliases=["unverify", "remove-link", "removelink"])
    async def unlink(self, ctx: commands.Context, nation: Nation):
        link = await funcs.get_link_nation(nation.id)
        await funcs.remove_link_nation(nation.id)
        user = self.bot.get_user(link["user_id"])
        if not user:
            user = await self.bot.fetch_user(link["user_id"])
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                user,
                f"{user.mention} has been unlinked from nation `{nation.id}`.",
                color=discord.Color.green(),
            )
        )

    @commands.command(
        name="force-link", aliases=["forcelink", "force-verify", "forceverify"]
    )
    async def force_link(
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
                )
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
                )
            )
        except IndexError:
            pass
        await funcs.add_link(member.id, nation.id)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                member,
                f"Success! {member.mention} is now linked to {repr(nation)}!",
                color=discord.Color.green(),
            )
        )

    @commands.group(name="extension", invoke_without_command=True)
    async def extension(self, ctx):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "You forgot to give a subcommand!",
                color=discord.Color.red(),
            )
        )

    @extension.command(name="reload")
    async def extension_reload(self, ctx, *, extension):
        try:
            self.bot.reload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` has been reloaded.",
                    color=discord.Color.green(),
                )
            )
        except commands.ExtensionNotLoaded:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` is not loaded.",
                    color=discord.Color.red(),
                )
            )
        except commands.ExtensionNotFound:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` does not exist.",
                    color=discord.Color.red(),
                )
            )

    @extension.command(name="load")
    async def extension_load(self, ctx, *, extension):
        try:
            self.bot.load_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` has been loaded.",
                    color=discord.Color.green(),
                )
            )
        except commands.ExtensionAlreadyLoaded:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` is already loaded.",
                    color=discord.Color.red(),
                )
            )
        except commands.ExtensionNotFound:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` does not exist.",
                    color=discord.Color.red(),
                )
            )

    @extension.command(name="unload")
    async def extension_unload(self, ctx, *, extension):
        try:
            self.bot.unload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` has been unloaded.",
                    color=discord.Color.green(),
                )
            )
        except commands.ExtensionNotLoaded:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` is not loaded.",
                    color=discord.Color.red(),
                )
            )
        except commands.ExtensionNotFound:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` does not exist.",
                    color=discord.Color.red(),
                )
            )

    @commands.command(name="enable-debug", aliases=["debug", "enabledebug"])
    async def enable_debug(self, ctx: commands.Context):
        ctx.bot.enable_debug = not ctx.bot.enable_debug
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Debug mode has been {'enabled' if ctx.bot.enable_debug else 'disabled'}.",
            )
        )

    @commands.group(name="staff", invoke_without_command=True)
    async def staff(self, ctx):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "You forgot to give a subcommand!",
                color=discord.Color.red(),
            )
        )

    @staff.command(name="add")
    async def staff_add(self, ctx, member: discord.Member):
        staff = await self.bot.get_staff()
        if member.id in staff:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{member.mention} is already Staff.",
                    color=discord.Color.red(),
                )
            )
            return
        await execute_query("INSERT INTO staff VALUES ($1);", member.id)
        self.bot.staff.append(member.id)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{member.mention} is now Staff.",
                color=discord.Color.green(),
            )
        )

    @staff.command(name="remove")
    async def staff_remove(self, ctx, member: discord.Member):
        staff = await self.bot.get_staff()
        if member.id not in staff:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{member.mention} is not Staff.",
                    color=discord.Color.red(),
                )
            )
            return
        await execute_query("DELETE FROM staff WHERE id = $1;", member.id)
        self.bot.staff.remove(member.id)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{member.mention} has been removed from Staff.",
                color=discord.Color.green(),
            )
        )

    @staff.command(name="list")
    async def staff_list(self, ctx):
        staff = await self.bot.get_staff()
        staff = [await self.bot.fetch_user(s) for s in staff]
        staff = [i for i in staff if i is not None]
        mentions = "\n".join(i.mention for i in staff)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"There are {len(staff):,} Staff:\n{mentions}",
                color=discord.Color.blue(),
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
        alliances = [Alliance(dict(i)) for i in await query_alliances()]
        for alliance in alliances:
            try:
                if alliance.ircchan is None:
                    continue
                await self.bot.fetch_invite(alliance.ircchan)
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


def setup(bot: Rift):
    bot.add_cog(Owner(bot))
