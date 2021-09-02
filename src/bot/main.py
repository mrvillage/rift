from __future__ import annotations

import contextlib
import datetime
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import discord
from discord.ext.commands import Context

from .. import funcs
from ..data.classes import Menu
from ..data.query import query_menus
from ..env import TOKEN, __version__
from ..ref import bot
from ..views import Margins, Prices


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
    try:
        message = await channel.fetch_message(payload.message_id)
    except discord.NotFound:
        return
    if TYPE_CHECKING:
        assert isinstance(message.edited_at, datetime.datetime)
    try:
        if message.created_at + datetime.timedelta(minutes=10) >= message.edited_at:
            await bot.process_commands(message)
    except TypeError:
        pass


@bot.event
async def on_ready():
    bot.persistent_views_loaded = True
    if not bot.persistent_views_loaded:
        views = await query_menus()
        views = [Menu(data=i) for i in views]
        for view in views:
            bot.add_view(await view.get_view())
        bot.add_view(Margins())
        bot.add_view(Prices())
        bot.persistent_views_loaded = True
        print("Loaded persistent views!")

    if not bot.cogs_loaded:
        cogPath = Path.cwd() / "src" / "bot" / "cogs"
        cogs = [i.name.replace(".py", "") for i in cogPath.glob("*.py")]
        for cog in cogs:
            bot.load_extension(f"src.bot.cogs.{cog}")
        bot.unload_extension("src.bot.cogs.database")
        bot.unload_extension("src.bot.cogs.server")
        bot.unload_extension("src.bot.cogs.logs")
        bot.cogs_loaded = True
        print("Loaded cogs!")

    for guild in bot.guilds:
        if not guild.chunked:
            await guild.chunk()
    print("Guilds chunked!")

    print("Startup complete!")


@bot.command(
    name="rift",
    aliases=["version", "about", "credits"],
    help="Get the bot credits and version.",
)
async def rift_about(ctx: Context):
    await ctx.reply(
        embed=funcs.get_embed_author_member(
            ctx.author,
            f'**Welcome to Rift!**\n\nRift is a multi-purpose bot for Politics and War created by <@!258298021266063360>!\n\nIf you have any questions feel free to join the House Stark server [here](https://discord.gg/AMse6jNen4 "https://discord.gg/AMse6jNen4") or send a DM to <@!258298021266063360>!\n\nRift Current Version: {__version__}',
        )
    )


async def main() -> None:
    with setup_logging():
        try:
            await bot.login(TOKEN)
            bot.loop.create_task(bot.update_pnw_session())
            bot.loop.create_task(bot.get_staff())
            await bot.connect(reconnect=True)
        finally:
            await bot.close()
