import json

import discord

from .. import cache
from .. import funcs as rift
from ..funcs import bot


async def target_check():
    targets = await rift.get_targets()
    for target in targets:
        try:
            nation = cache.nations[target[1]]
            if nation.color != "Beige" and target[2] == 0:
                if target[3] == "[]":
                    pass
                else:
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
                            mentions += f"<@{f'><@'.join([str(i) for i in json.loads(target[6])])}>"
                        embed = rift.get_embed_author_guild(
                            channel.guild,
                            f'[Nation Page](https://politicsandwar.com/nation/id={nation.id} "https://politicsandwar.com/nation/id={nation.id}")',
                            timestamp=bot.nations_update,
                            footer="Data collected at",
                            fields=[
                                {"name": "Nation ID", "value": nation.id},
                                {"name": "Nation Name", "value": nation.name},
                                {"name": "Leader Name", "value": nation.leader},
                                {"name": "War Policy", "value": nation.war_policy},
                                {
                                    "name": "Domestic Policy",
                                    "value": nation.domestic_policy,
                                },
                                {"name": "Continent", "value": nation.continent},
                                {
                                    "name": "Color",
                                    "value": nation.color
                                    if nation.color != "Beige"
                                    else f"Beige ({nation.beige_turns:,} Turns",
                                },
                                {
                                    "name": "Alliance",
                                    "value": f'[{repr(nation.alliance)}](https://politicsandwar.com/alliance/id={nation.alliance.id} "https://politicsandwar.com/alliance/id={nation.alliance.id}")'
                                    if nation.alliance is not None
                                    else "None",
                                },
                                {
                                    "name": "Alliance Position",
                                    "value": nation.alliance_position,
                                },
                                {
                                    "name": "Cities",
                                    "value": f"[{nation.cities}](https://politicsandwar.com/?id=62&n={'+'.join(nation.name.split(' '))} \"https://politicsandwar.com/?id=62&n={'+'.join(nation.name.split(' '))}\")",
                                },
                                {"name": "Score", "value": f"{nation.score:,.2f}"},
                                {
                                    "name": "Vacation Mode",
                                    "value": f"True ({nation.v_mode_turns:,} Turns)"
                                    if nation.v_mode
                                    else "False",
                                },
                                {"name": "Soldiers", "value": f"{nation.soldiers:,}"},
                                {"name": "Tanks", "value": f"{nation.tanks:,}"},
                                {"name": "Aircraft", "value": f"{nation.aircraft:,}"},
                                {"name": "Ships", "value": f"{nation.ships:,}"},
                                {"name": "Missiles", "value": f"{nation.missiles:,}"},
                                {"name": "Nukes", "value": f"{nation.nukes:,}"},
                                {
                                    "name": "Offensive Wars",
                                    "value": f'[{nation.offensive_wars}](https://politicsandwar.com/nation/id={nation.id}&display=war "https://politicsandwar.com/nation/id={nation.id}&display=war")',
                                },
                                {
                                    "name": "Defensive Wars",
                                    "value": f'[{nation.defensive_wars}](https://politicsandwar.com/nation/id={nation.id}&display=war "https://politicsandwar.com/nation/id={nation.id}&display=war")',
                                },
                                {
                                    "name": "Average Infrastructure",
                                    "value": f"{nation.avg_infra():,.2f}",
                                },
                                {
                                    "name": "Actions",
                                    "value": f"[Message](https://politicsandwar.com/inbox/message/receiver={'+'.join(nation.leader.split(' '))} \"https://politicsandwar.com/inbox/message/receiver={'+'.join(nation.leader.split(' '))}\") "
                                    f"[Trade](https://politicsandwar.com/nation/trade/create/nation={'+'.join(nation.name.split(' '))} \"https://politicsandwar.com/nation/trade/create/nation={'+'.join(nation.name.split(' '))}\") "
                                    f"[Embargo](https://politicsandwar.com/index.php?id=68&name={'+'.join(nation.name.split(' '))}&type=n \"https://politicsandwar.com/index.php?id=68&name={'+'.join(nation.name.split(' '))}&type=n\") "
                                    f'[War](https://politicsandwar.com/nation/war/declare/id={nation.id} "https://politicsandwar.com/nation/war/declare/id={nation.id}") '
                                    f'[Espionage](https://politicsandwar.com/nation/espionage/eid={nation.id} "https://politicsandwar.com/nation/espionage/eid={nation.id}") ',
                                },
                            ],
                        )
                        await channel.send(mentions, embed=embed)
            await rift.update_target_color(nation.id, rift.get_color_id(nation.color))
        except Exception as e:
            print("ERROR IN TARGET CHECK", e)
