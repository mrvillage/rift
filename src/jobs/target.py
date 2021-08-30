import json
from src.data.classes.nation import Nation

import discord

from .. import funcs
from ..funcs import bot


async def target_check():
    targets = await funcs.get_targets()
    for target in targets:
        try:
            nation = await Nation.fetch(target[1])
            if nation.color != "Beige" and target[2] == 0 and target[3] == "[]":
                for id in json.loads(target[4]):
                    channel = discord.utils.find(
                        lambda c: c.id == int(id), list(bot.get_all_channels())
                    )
                    mentions = [
                        i for i in json.loads(target[4]) + json.loads(target[5])
                    ]
                    if len(json.loads(target[5])) != 0:
                        mentions = f"<@&{f'><@&'.join([str(i) for i in json.loads(target[5])])}>"
                    else:
                        mentions = ""
                    if len(json.loads(target[6])) != 0:
                        mentions += (
                            f"<@{f'><@'.join([str(i) for i in json.loads(target[6])])}>"
                        )
                    embed = await nation.get_info_embed(channel)
                    await channel.send(mentions, embed=embed)
            await funcs.update_target_color(nation.id, funcs.get_color_id(nation.color))
        except Exception as e:
            print("ERROR IN TARGET CHECK", e)
