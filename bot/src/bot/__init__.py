from __future__ import annotations

import contextlib
import datetime
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import aiohttp
import discord
from discord.ext import commands

from .. import funcs
from ..cache import cache
from ..env import DEBUG_TOKEN, TOKEN, __version__
from ..ref import RiftContext, bot
from ..views import (
    AlliancesPaginator,
    Colors,
    EventExtraInformationView,
    Margins,
    Prices,
    TreasuresView,
)


@contextlib.contextmanager
def setup_logging():
    logging.getLogger("discord").setLevel(logging.INFO)
    logger = logging.getLogger()
    try:
        handler = logging.FileHandler(filename="rift.log", encoding="utf-8", mode="a")
        handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        logger.addHandler(handler)
        yield
    finally:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)


@bot.event
async def on_message(message: discord.Message):
    ctx = await bot.get_context(message)  # type: ignore
    if not await bot.is_owner(message.author) and ctx.command is not None and ctx.command.name not in {"mmr", "stockpile", "mmr-check", "stockpile-check"}:  # type: ignore
        return
    try:
        await bot.invoke(ctx)  # type: ignore
    except Exception as error:
        await funcs.handler(ctx, error)  # type: ignore


@bot.event
async def on_raw_message_edit(payload: discord.RawMessageUpdateEvent):
    channel = bot.get_channel(payload.channel_id)
    if channel is None:
        return
    if TYPE_CHECKING:
        assert isinstance(channel, (discord.TextChannel, discord.DMChannel))
    try:
        message = await channel.fetch_message(payload.message_id)
    except discord.NotFound:
        return
    if TYPE_CHECKING:
        assert isinstance(message.edited_at, datetime.datetime)
    if not await bot.is_owner(message.author):  # type: ignore
        return
    try:
        if message.created_at + datetime.timedelta(minutes=10) >= message.edited_at:
            await bot.process_commands(message)
    except TypeError:
        pass


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.application_command:
        return
    ctx = await bot.get_interaction_context(interaction)  # type: ignore
    try:
        await bot.invoke(ctx)  # type: ignore
    except Exception as error:
        await funcs.handler(ctx, error)  # type: ignore


@bot.event
async def on_ready():
    print("Startup complete!", flush=True)


@bot.command(  # type: ignore
    name="about",
    aliases=["version", "rift", "credits"],
    brief="Get the bot credits, version, and about.",
    type=(commands.CommandType.default, commands.CommandType.chat_input),
)
async def about(ctx: RiftContext):
    await ctx.reply(
        embed=funcs.get_embed_author_member(
            ctx.author,
            f"**Welcome to Rift!**\n\nRift is a free-to-use general purpose Discord bot for Politics and War created by <@!258298021266063360>!\n\nIf you have any questions feel free to join the Rift server [here](https://rift.mrvillage.dev/discord) or send a DM to <@!258298021266063360>! Check out more information on the website [here](https://rift.mrvillage.dev), read the documentation [here](https://rift.mrvillage.dev/docs), or check out the code on GitHub [here](https://rift.mrvillage.dev/github).\n\nRift Current Version: {__version__}\n\nRift is licensed under under [GNU GPL v3](https://rift.mrvillage.dev/https://license/) and comes with absolutely no warranty.",
            color=discord.Color.blue(),
        )
    )


async def main() -> None:
    with setup_logging():
        try:
            if bot.debug:  # type: ignore
                await bot.login(DEBUG_TOKEN)
            else:
                await bot.login(TOKEN)

            await bot.update_pnw_session()

            await cache.initialize()
            print("Cache initialized!", flush=True)

            for menu in cache.menus:
                bot.add_view(menu.get_view())
            for request in cache.transaction_requests:
                bot.add_view(request.view)
            views = [
                Margins(),
                Prices(),
                AlliancesPaginator(1, 50),
                EventExtraInformationView(),
                TreasuresView(),
                Colors(),
            ]
            for view in views:
                bot.add_view(view)
            print("Loaded persistent views!", flush=True)

            async with aiohttp.request("GET", bot.user.display_avatar.url) as req:  # type: ignore
                bot.bytes_avatar = await req.read()

            bot.load_extension("jishaku")
            cogPath = Path.cwd() / "src" / "bot" / "cogs"
            cogs = [i.name.replace(".py", "") for i in cogPath.glob("*.py")]
            for cog in cogs:
                bot.load_extension(f"src.bot.cogs.{cog}")
            if bot.debug:  # type: ignore
                bot.unload_extension("src.bot.cogs.logs")
                bot.unload_extension("src.bot.cogs.event_messages")
                bot.unload_extension("src.bot.cogs.database_cache")
            print("Loaded cogs!", flush=True)

            await bot.register_application_commands()
            print("Application commands registered!", flush=True)

            await bot.connect(reconnect=True)
        finally:
            await bot.close()
