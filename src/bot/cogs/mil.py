import json
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands

from ... import find
from ... import funcs as rift
from ...errors import AllianceNotFoundError, NationNotFoundError


class Military(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="target", invoke_without_command=True)
    async def target(self, ctx, target_id=None):
        if id == None:
            await ctx.send(
                embed=rift.get_embed_author_member(
                    ctx.author,
                    f"You forgot an argument!\n\n`?target <add/remove/list>`",
                )
            )
            return
        try:
            target = await rift.get_target(int(target_id))
        except:
            await ctx.send(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{target_id}` is not a valid target."
                )
            )
            return
        nation = await rift.get_nation(target[1])
        embed = rift.get_embed_author_member(
            discord.utils.find(lambda c: c.id == target[3], self.bot.get_all_members()),
            f"{nation[1]} - {nation[0]}\nCurrent Color: {rift.get_color(nation[6]) if nation[6] != 0 else f'Beige ({nation[16]} Turns)'}",
        )
        channels, roles, members = (
            [str(i) for i in json.loads(target[4])],
            [str(i) for i in json.loads(target[5])],
            [str(i) for i in json.loads(target[6])],
        )
        if len(channels) != 0:
            embed.add_field(
                name="Channel Notifications",
                value=f"<#{'><#'.join(channels)}>",
                inline=True,
            )
        else:
            embed.add_field(name="Channel Notifications", value="None", inline=True)
        if len(roles) != 0:
            embed.add_field(
                name="Role Mentions", value=f"<@&{'><@&'.join(roles)}>", inline=True
            )
        else:
            embed.add_field(name="Role Mentions", value="None", inline=True)
        if len(members) != 0:
            embed.add_field(
                name="Member Mentions", value=f"<@{'><@'.join(members)}>", inline=True
            )
        else:
            embed.add_field(name="Member Mentions", value="None", inline=True)
        await ctx.send(embed=embed)

    @target.command(name="add")
    async def target_add(self, ctx, search, *args):
        if "politicsandwar" in search:
            if "http" in search:
                search = search.replace("https://", "")
            nation_id = int(
                search.strip("/\\").replace("politicsandwar.com/nation/id=", "")
            )
        elif search.isdigit():
            nation_id = int(search)
        else:
            try:
                nation_id = (await rift.get_nation_name(search))[0][0]
            except:
                await ctx.send(
                    embed=rift.get_embed_author_member(
                        ctx.author,
                        f'Nation `{search}` doesn\'t exist! Please try again.\n\nIf the nation name is multiple words remember to surround it in quotes ("")',
                    )
                )
                return
        nation = await rift.get_nation(nation_id)
        channels, roles, members = [], [], []
        for arg in args:
            try:
                channels.append(
                    (await commands.TextChannelConverter().convert(ctx, arg)).id
                )
            except:
                try:
                    roles.append((await commands.RoleConverter().convert(ctx, arg)).id)
                except:
                    try:
                        members.append(
                            (await commands.MemberConverter().convert(ctx, arg)).id
                        )
                    except:
                        pass
        await rift.add_target(
            nation_id, nation[6], ctx.author.id, channels, roles, members
        )
        embed = rift.get_embed_author_member(
            ctx.author,
            f"`{nation[1]}` added as target.\nCurrent Color: {rift.get_color(nation[6]) if nation[6] != 0 else f'Beige ({nation[16]} Turns)'}",
        )
        channels, roles, members = (
            [str(i) for i in channels],
            [str(i) for i in roles],
            [str(i) for i in members],
        )
        if len(channels) != 0:
            embed.add_field(
                name="Channel Notifications",
                value=f"<#{f'><#'.join(channels)}>",
                inline=True,
            )
        else:
            embed.add_field(name="Channel Notifications", value=f"None", inline=True)
            await ctx.send(
                embed=rift.get_embed_author_member(
                    ctx.author, f"You forgot to set a channel!"
                )
            )
            return
        if len(roles) != 0:
            embed.add_field(
                name="Role Mentions", value=f"<@&{f'><@&'.join(roles)}>", inline=True
            )
        else:
            embed.add_field(name="Role Mentions", value=f"None", inline=True)
        if len(members) != 0:
            embed.add_field(
                name="Member Mentions", value=f"<@{f'><@'.join(members)}>", inline=True
            )
        else:
            embed.add_field(name="Member Mentions", value=f"None", inline=True)
        await ctx.send(embed=embed)

    @target.command(name="remove")
    async def target_remove(self, ctx, target_id):
        try:
            target = await rift.get_target(int(target_id))
        except:
            await ctx.send(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{target_id}` is not a valid target."
                )
            )
            return
        if target[3] == ctx.author.id:
            await rift.remove_target(int(target_id))
            await ctx.send(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Removed target `{target_id}`."
                )
            )
        else:
            await ctx.send(
                embed=rift.get_embed_author_member(
                    ctx.author, f"You're not the owner of that target."
                )
            )

    @target.command(name="list")
    async def target_list(self, ctx):
        targets = await rift.get_targets_owner(ctx.author.id)
        await ctx.send(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"**Target ID | Nation ID | Nation Name**\n\n{f'{rift.NEWLINE}'.join([f'{target[0]} | {target[1]} | {(await rift.get_nation(target[1]))[1]}' for target in targets])}",
            )
        )

    @commands.group(
        name="militarization",
        aliases=["m", "mil", "military"],
        case_insensitive=True,
        invoke_without_command=True,
    )
    async def militarization(self, ctx, *, search=None):
        search = str(ctx.author.id) if search is None else search
        try:
            alliance = await rift.search_alliance(ctx, search)
        except AllianceNotFoundError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"No alliance found with argument `{search}`."
                )
            )
            return
        await alliance.make_attrs("members", "member_count")
        async with ctx.typing():
            async with aiohttp.request(
                "GET", f"https://checkapi.bsnk.dev/getChart?allianceID={alliance.id}"
            ) as req:
                byte = await req.read()
        militarization = alliance.get_militarization(vm=False)
        image = discord.File(BytesIO(byte), f"militarization_{alliance.id}.png")
        cities = alliance.get_cities()
        embed = rift.get_embed_author_member(
            ctx.author,
            f"""
            Total Militarization: {militarization['total']*100:.2f}%
            Soldier Militarization: {militarization['soldiers']*100:.2f}%
            Tank Militarization: {militarization['tanks']*100:.2f}%
            Aircraft Militarization: {militarization['aircraft']*100:.2f}%
            Ship Militarization: {militarization['ships']*100:.2f}%
            """,
            title=f"Militarization Graph for {alliance.name} (`{alliance.id}`)",
            image_url=f"attachment://militarization_{alliance.id}.png",
            fields=[
                {
                    "name": "Soldiers",
                    "value": f"{alliance.get_soldiers():,}/{cities*15000:,}",
                },
                {"name": "Tanks", "value": f"{alliance.get_tanks():,}/{cities*1250:,}"},
                {
                    "name": "Aircraft",
                    "value": f"{alliance.get_aircraft():,}/{cities*75:,}",
                },
                {"name": "Ships", "value": f"{alliance.get_ships():,}/{cities*15:,}"},
                {"name": "Missiles", "value": f"{alliance.get_missiles():,}"},
                {"name": "Nukes", "value": f"{alliance.get_nukes():,}"},
            ],
        )
        await ctx.send(file=image, embed=embed)

    @commands.command(name="mn", hidden=True)
    async def mn_shortcut(self, ctx: commands.Context, *, search=None):
        await ctx.invoke(self.militarization_nation, search=search)

    @militarization.command(name="nation", aliases=["n", "nat", "me"])
    async def militarization_nation(self, ctx, *, search=None):
        try:
            author, nation = await find.search_nation_author(ctx, search)
        except NationNotFoundError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"No nation found with argument `{search}`."
                )
            )
            return
        militarization = nation.get_militarization()
        if isinstance(author, discord.Guild):
            embed = rift.get_embed_author_guild(
                author,
                f"Total Militarization: {militarization['total']*100:.2f}%\nSoldier Militarization: {militarization['soldiers']*100:.2f}%\nTank Militarization: {militarization['tanks']*100:.2f}%\nAircraft Militarization: {militarization['aircraft']*100:.2f}%\nShip Militarization: {militarization['ships']*100:.2f}%",
                title=f"Militarization for {nation.name} (`{nation.id}`)",
                fields=[
                    {
                        "name": "Soldiers",
                        "value": f"{nation.soldiers:,}/{nation.cities*15000:,}",
                    },
                    {
                        "name": "Tanks",
                        "value": f"{nation.tanks:,}/{nation.cities*1250:,}",
                    },
                    {
                        "name": "Aircraft",
                        "value": f"{nation.aircraft:,}/{nation.cities*75:,}",
                    },
                    {
                        "name": "Ships",
                        "value": f"{nation.ships:,}/{nation.cities*15:,}",
                    },
                    {"name": "Missiles", "value": f"{nation.missiles:,}"},
                    {"name": "Nukes", "value": f"{nation.nukes:,}"},
                ],
            )
        else:
            embed = rift.get_embed_author_member(
                author,
                f"Total Militarization: {militarization['total']*100:.2f}%\nSoldier Militarization: {militarization['soldiers']*100:.2f}%\nTank Militarization: {militarization['tanks']*100:.2f}%\nAircraft Militarization: {militarization['aircraft']*100:.2f}%\nShip Militarization: {militarization['ships']*100:.2f}%",
                title=f"Militarization for {nation.name} (`{nation.id}`)",
                fields=[
                    {
                        "name": "Soldiers",
                        "value": f"{nation.soldiers:,}/{nation.cities*15000:,}",
                    },
                    {
                        "name": "Tanks",
                        "value": f"{nation.tanks:,}/{nation.cities*1250:,}",
                    },
                    {
                        "name": "Aircraft",
                        "value": f"{nation.aircraft:,}/{nation.cities*75:,}",
                    },
                    {
                        "name": "Ships",
                        "value": f"{nation.ships:,}/{nation.cities*15:,}",
                    },
                    {"name": "Missiles", "value": f"{nation.missiles:,}"},
                    {"name": "Nukes", "value": f"{nation.nukes:,}"},
                ],
            )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Military(bot))
