import datetime
from pathlib import Path

from .. import funcs as rift

# from ..data import cache
from ..env import TOKEN, __version__
from ..ref import bot


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_raw_message_edit(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(
        payload.message_id
    )
    try:
        if message.created_at + datetime.timedelta(minutes=10) >= message.edited_at:
            await bot.process_commands(message)
    except TypeError:
        pass


@bot.event
async def on_ready():
    print("Startup complete!")


@bot.command(name="rift", aliases=["version", "about", "credits"])
async def rift_about(ctx):
    await ctx.reply(
        embed=rift.get_embed_author_member(
            ctx.author,
            f'**Welcome to Rift!**\n\nRift is a multi-purpose bot for Politics and War created by <@!258298021266063360>!\n\nIf you have any questions feel free to join the Ad Astra server [here](https://discord.gg/DegFNa3hs7 "https://discord.gg/86Hzkp2CWU"), the Database server [here](https://discord.gg/86Hzkp2CWU "https://discord.gg/86Hzkp2CWU"), or send a DM to <@!258298021266063360>!\n\nRift Current Version: {__version__}',
        )
    )


def main():
    cogPath = Path.cwd() / "source" / "bot" / "cogs"
    cogs = [i.name.replace(".py", "") for i in cogPath.glob("*.py")]
    for cog in cogs:
        bot.load_extension(f"source.bot.cogs.{cog}")
        print(f"Loaded {cog}!")

    # bot.loop.create_task(cache.create_cache())
    bot.loop.create_task(bot.update_pnw_session())
    bot.loop.create_task(bot.get_staff())
    bot.command_prefix = "!!"
    bot.run(TOKEN)
