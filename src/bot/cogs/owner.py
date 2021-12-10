from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...data import get
from ...data.classes import Nation
from ...env import __version__
from ...ref import Rift, RiftContext


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: Rift):
        self.bot = bot

    async def cog_check(self, ctx: RiftContext):  # type: ignore
        if TYPE_CHECKING:
            assert isinstance(ctx.author, discord.User)
        return await self.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx: RiftContext, error: Exception):  # type: ignore
        if not isinstance(error, commands.CheckFailure):
            await funcs.handler(ctx, error)

    @commands.command(name="unlink", aliases=["unverify", "remove-link", "removelink"])
    async def unlink(self, ctx: RiftContext, nation: Nation):
        link = await get.get_link_nation(nation.id)
        await get.remove_link_nation(nation.id)
        user = self.bot.get_user(link.user_id)
        if not user:
            user = await self.bot.fetch_user(link.user_id)
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
        self, ctx: RiftContext, nation: Nation, user: discord.User = MISSING
    ):
        member = user or ctx.author
        try:
            await get.get_link_user(member.id)
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
            await get.get_link_nation(nation.id)
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{repr(nation)} is already linked!",
                    color=discord.Color.red(),
                )
            )
        except IndexError:
            pass
        await get.add_link(member.id, nation.id)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                member,
                f"Success! {member.mention} is now linked to {repr(nation)}!",
                color=discord.Color.green(),
            )
        )

    @commands.group(name="extension", invoke_without_command=True)
    async def extension(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "You forgot to give a subcommand!",
                color=discord.Color.red(),
            )
        )

    @extension.command(name="reload")  # type: ignore
    async def extension_reload(self, ctx: RiftContext, *, extension: str):
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

    @extension.command(name="load")  # type: ignore
    async def extension_load(self, ctx: RiftContext, *, extension: str):
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

    @extension.command(name="unload")  # type: ignore
    async def extension_unload(self, ctx: RiftContext, *, extension: str):
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
    async def enable_debug(self, ctx: RiftContext):
        ctx.bot.enable_debug = not ctx.bot.enable_debug
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Debug mode has been {'enabled' if ctx.bot.enable_debug else 'disabled'}.",
            )
        )

    @commands.command(name="stats")
    async def stats(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                __version__,
                fields=[
                    {"name": "Guilds", "value": f"{len(self.bot.guilds):,}"},
                    {"name": "Users", "value": f"{len(self.bot.users):,}"},
                    {"name": "Latency", "value": f"{self.bot.latency:,}s"},
                    {"name": "Links", "value": f"{len(cache.users):,}"},
                    {
                        "name": "Owners",
                        "value": f"{len({i.owner.id for i in self.bot.guilds if i.owner is not None}):,}",
                    },
                    {
                        "name": "Unique",
                        "value": f"{len({i.owner.id for i in self.bot.guilds if i.owner is not None})/len(self.bot.guilds):,.2%}",
                    },
                ],
            )
        )

    @commands.command(name="guilds")
    async def guilds(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(f"{i.name} - {i.member_count}" for i in self.bot.guilds),
                title=f"{len(self.bot.guilds):,} guilds",
            )
        )

    @commands.command(name="owners")
    async def owners(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"{i.name} - {i.member_count} - {i.owner and i.owner.mention}"
                    for i in self.bot.guilds
                ),
                title=f"{len(self.bot.guilds):,} guilds",
            )
        )


def setup(bot: Rift):
    bot.add_cog(Owner(bot))
