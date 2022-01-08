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
    await bot.process_commands(message)


@bot.event
async def on_raw_message_edit(payload: discord.RawMessageUpdateEvent):
    channel = bot.get_channel(payload.channel_id)
    if TYPE_CHECKING:
        assert isinstance(channel, (discord.TextChannel, discord.DMChannel))
    message = await channel.fetch_message(payload.message_id)
    if TYPE_CHECKING:
        assert isinstance(message.edited_at, datetime.datetime)
    try:
        if message.created_at + datetime.timedelta(minutes=10) >= message.edited_at:
            await bot.process_commands(message)
    except TypeError:
        pass


@bot.event
async def on_interaction(interaction: discord.Interaction):
    await bot.process_commands(interaction)


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
            f'**Welcome to Rift!**\n\nRift is a multi-purpose bot for Politics and War created by <@!258298021266063360>!\n\nIf you have any questions feel free to join the House Stark server [here](https://discord.gg/AMse6jNen4 "https://discord.gg/AMse6jNen4"), the Database server [here](https://discord.gg/86Hzkp2CWU "https://discord.gg/86Hzkp2CWU"), or send a DM to <@!258298021266063360>!\n\nRift Current Version: {__version__}',
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
            bot.unload_extension("src.bot.cogs.odds")
            bot.unload_extension("src.bot.cogs.grants")
            print("Loaded cogs!", flush=True)

            await bot.register_application_commands()
            print("Application commands registered!", flush=True)

            await bot.connect(reconnect=True)
        finally:
            await bot.close()
