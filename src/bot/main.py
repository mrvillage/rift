from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import discord
from discord.ext.commands import Context, _slash  # type: ignore

from .. import funcs
from ..data.classes import Menu
from ..data.query import get_menus
from ..env import TOKEN, __version__
from ..ref import bot
from ..views import Margins, Prices

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="rift.log", encoding="utf-8", mode="a")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


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
    if not bot.persistent_views_loaded:
        views = await get_menus()
        views = [Menu(data=i) for i in views]
        for view in views:
            bot.add_view(await view.get_view())
        bot.add_view(Margins())
        bot.add_view(Prices())
        bot.persistent_views_loaded = True

    if not bot.cogs_loaded:
        await bot.get_global_application_commands()
        _slash(bot.get_command("rift"))
        cogPath = Path.cwd() / "src" / "bot" / "cogs"
        cogs = [i.name.replace(".py", "") for i in cogPath.glob("*.py")]
        for cog in cogs:
            bot.load_extension(f"src.bot.cogs.{cog}")
            print(f"Loaded {cog}!")
        bot.unload_extension("src.bot.cogs.database")
        bot.unload_extension("src.bot.cogs.server")
        bot.cogs_loaded = True
    print("Startup complete!")


@bot.command(name="rift", aliases=["version", "about", "credits"])
async def rift_about(ctx: Context):
    await ctx.reply(
        embed=funcs.get_embed_author_member(
            ctx.author,
            f'**Welcome to Rift!**\n\nRift is a multi-purpose bot for Politics and War created by <@!258298021266063360>!\n\nIf you have any questions feel free to join the Ad Astra server [here](https://discord.gg/DegFNa3hs7 "https://discord.gg/86Hzkp2CWU"), the Database server [here](https://discord.gg/86Hzkp2CWU "https://discord.gg/86Hzkp2CWU"), or send a DM to <@!258298021266063360>!\n\nRift Current Version: {__version__}',
        )
    )


def main() -> None:
    bot.loop.create_task(bot.update_pnw_session())
    bot.loop.create_task(bot.get_staff())
    # bot.command_prefix = "!!"
    bot.run(TOKEN)
