import json
import discord
from .. import funcs as rift
from ..data.db import connection
from ..funcs import bot

async def target_check():
    targets = await rift.get_targets(connection)
    for target in targets:
        # print("target",target)
        try:
            nation = await rift.get_nation(connection, target[1])
            # print("nation",nation)
            if nation[6] != 0 and target[2] == 0:
                if target[3] == "[]":
                    # print("if")
                    # members = str(target[2]).strip('[]').split(',')
                    # # print("No channels!")
                    # for member in members:
                    #     pass
                    pass
                else:
                    # print("else")
                    for id in json.loads(target[4]):
                        channel = discord.utils.find(lambda c:c.id == int(id), list(bot.get_all_channels()))
                        # print("Got channel")
                        mentions = [i for i in json.loads(target[4])+json.loads(target[5])]
                        if len(json.loads(target[5])) != 0:
                            mentions = f"<@&{f'><@&'.join([str(i) for i in json.loads(target[5])])}>"
                        else:
                            mentions = ""
                        if len(json.loads(target[6])) != 0:
                            mentions += f"<@{f'><@'.join([str(i) for i in json.loads(target[6])])}>"
                        # print("Almost sent")
                        await channel.send(mentions,embed=rift.get_embed_author_guild(channel.guild,f"[Nation Page](https://politicsandwar.com/nation/id={nation[0]})",timestamp=bot.nations_update,footer="Data collected at").add_field(name="Nation ID",value=nation[0],inline=True).add_field(name="Nation Name",value=nation[1],inline=True).add_field(name="Leader Name",value=nation[2],inline=True).add_field(name="War Policy",value=rift.get_war_policy(nation[4]),inline=True).add_field(name="Domestic Policy",value=rift.get_domestic_policy(nation[5]),inline=True).add_field(name="Color",value=rift.get_color(nation[6]),inline=True).add_field(name="Alliance ID",value=rift.get_alliance_id(nation[7]),inline=True).add_field(name="Alliance Name",value=nation[8],inline=True).add_field(name="Alliance Position",value=rift.get_alliance_position(nation[9]),inline=True).add_field(name="Cities",value=nation[10],inline=True).add_field(name="Score",value=f"{nation[13]:.2f}",inline=True).add_field(name="Vacation Mode",value=nation[14]).add_field(name="Soldiers",value=f"{nation[19]:,}",inline=True).add_field(name="Tanks",value=f"{nation[20]:,}",inline=True).add_field(name="Aircraft",value=f"{nation[21]:,}",inline=True).add_field(name="Ships",value=f"{nation[22]:,}",inline=True).add_field(name="Missiles",value=f"{nation[23]:,}",inline=True).add_field(name="Nukes",value=f"{nation[24]:,}",inline=True))
            await rift.update_target_color(connection, nation[0], nation[6])
            # print("Color updated")
        except Exception as e:
            print(e)