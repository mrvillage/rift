import discord
import asyncio
import json
import time
import aiohttp
from io import BytesIO
from discord.ext import commands, tasks
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level
from ... import cache  # pylint: disable=relative-beyond-top-level


class Military(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="target", invoke_without_command=True)
    async def target(self, ctx, target_id=None):
        if id == None:
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"You forgot an argument!\n\n`?target <add/remove/list>`"))
            return
        try:
            target = await rift.get_target(self.bot.connection, int(target_id))
        except:
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"`{target_id}` is not a valid target."))
            return
        nation = await rift.get_nation(self.bot.connection, target[1])
        embed = rift.get_embed_author_member(discord.utils.find(lambda c: c.id == target[3], self.bot.get_all_members(
        )), f"{nation[1]} - {nation[0]}\nCurrent Color: {rift.get_color(nation[6]) if nation[6] != 0 else f'Beige ({nation[16]} Turns)'}")
        channels, roles, members = [str(i) for i in json.loads(target[4])], [str(
            i) for i in json.loads(target[5])], [str(i) for i in json.loads(target[6])]
        if len(channels) != 0:
            embed.add_field(name="Channel Notifications",
                            value=f"<#{f'><#'.join(channels)}>", inline=True)
        else:
            embed.add_field(name="Channel Notifications",
                            value=f"None", inline=True)
        if len(roles) != 0:
            embed.add_field(name="Role Mentions",
                            value=f"<@&{f'><@&'.join(roles)}>", inline=True)
        else:
            embed.add_field(name="Role Mentions", value=f"None", inline=True)
        if len(members) != 0:
            embed.add_field(name="Member Mentions",
                            value=f"<@{f'><@'.join(members)}>", inline=True)
        else:
            embed.add_field(name="Member Mentions", value=f"None", inline=True)
        await ctx.send(embed=embed)

    @target.command(name="add")
    async def target_add(self, ctx, search, *args):
        if "politicsandwar" in search:
            if "http" in search:
                search = search.replace("https://", "")
            nation_id = int(search.strip(
                "/\\").replace("politicsandwar.com/nation/id=", ""))
        elif search.isdigit():
            nation_id = int(search)
        else:
            try:
                nation_id = (await rift.get_nation_name(self.bot.connection, search))[0][0]
            except:
                await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"Nation `{search}` doesn't exist! Please try again.\n\nIf the nation name is multiple words remember to surround it in quotes (\"\")"))
                return
        nation = await rift.get_nation(self.bot.connection, nation_id)
        channels, roles, members = [], [], []
        for arg in args:
            try:
                channels.append((await commands.TextChannelConverter().convert(ctx, arg)).id)
            except:
                try:
                    roles.append((await commands.RoleConverter().convert(ctx, arg)).id)
                except:
                    try:
                        members.append((await commands.MemberConverter().convert(ctx, arg)).id)
                    except:
                        pass
        await rift.add_target(self.bot.connection, nation_id, nation[6], ctx.author.id, channels, roles, members)
        embed = rift.get_embed_author_member(
            ctx.author, f"`{nation[1]}` added as target.\nCurrent Color: {rift.get_color(nation[6]) if nation[6] != 0 else f'Beige ({nation[16]} Turns)'}")
        channels, roles, members = [str(i) for i in channels], [
            str(i) for i in roles], [str(i) for i in members]
        if len(channels) != 0:
            embed.add_field(name="Channel Notifications",
                            value=f"<#{f'><#'.join(channels)}>", inline=True)
        else:
            embed.add_field(name="Channel Notifications",
                            value=f"None", inline=True)
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"You forgot to set a channel!"))
            return
        if len(roles) != 0:
            embed.add_field(name="Role Mentions",
                            value=f"<@&{f'><@&'.join(roles)}>", inline=True)
        else:
            embed.add_field(name="Role Mentions", value=f"None", inline=True)
        if len(members) != 0:
            embed.add_field(name="Member Mentions",
                            value=f"<@{f'><@'.join(members)}>", inline=True)
        else:
            embed.add_field(name="Member Mentions", value=f"None", inline=True)
        await ctx.send(embed=embed)

    @target.command(name="remove")
    async def target_remove(self, ctx, target_id):
        try:
            target = await rift.get_target(self.bot.connection, int(target_id))
        except:
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"`{target_id}` is not a valid target."))
            return
        if target[3] == ctx.author.id:
            await rift.remove_target(self.bot.connection, int(target_id))
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"Removed target `{target_id}`."))
        else:
            await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"You're not the owner of that target."))

    @target.command(name="list")
    async def target_list(self, ctx):
        targets = await rift.get_targets_owner(self.bot.connection, ctx.author.id)
        await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"**Target ID | Nation ID | Nation Name**\n\n{f'{rift.NEWLINE}'.join([f'{target[0]} | {target[1]} | {(await rift.get_nation(self.bot.connection, target[1]))[1]}' for target in targets])}"))

    @commands.group(name="militarization", aliases=["mil", "military"], case_insensitive=True, invoke_without_command=True)
    async def militarization(self, ctx, *, search=None):
        if search == None:
            nation_id = (await rift.get_link_user(self.bot.connection, ctx.author.id))[1]
            alliance = (cache.nations[nation_id]).alliance
            if isinstance(alliance, str):
                alliance = cache.alliances[(await rift.get_alliance_name(self.bot.connection, alliance))[0]]
        else:
            try:
                user = (await commands.UserConverter().convert(ctx, search))
                try:
                    nation_id = (await rift.get_link_user(self.bot.connection, user.id))[1]
                except IndexError:
                    await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"No link found for user {user.mention}."))
                    return
                alliance = cache.nations[nation_id].alliance
            except commands.BadArgument:
                try:
                    alliance_id = int(search)
                    alliance = cache.alliances[alliance_id]
                except ValueError:
                    try:
                        alliance = await rift.get_alliance_name(self.bot.connection, search)
                        alliance = cache.alliances[alliance[0]]
                    except IndexError:
                        await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"Alliance `{search}` not found."))
                        return
                except KeyError:
                    await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"Alliance `{search}` not found."))
                    return
        async with ctx.typing():
            async with aiohttp.request("GET", f"https://checkapi.bsnk.dev/getChart?allianceID={alliance.id}") as req:
                byte = await req.read()
        militarization = alliance.get_militarization(vm=False)
        image = discord.File(
            BytesIO(byte), f"militarization_{alliance.id}.png")
        cities = alliance.get_cities()
        embed = rift.get_embed_author_member(ctx.author, f"Total Militarization: {militarization['total']*100:.2f}%\nSoldier Militarization: {militarization['soldiers']*100:.2f}%\nTank Militarization: {militarization['tanks']*100:.2f}%\nAircraft Militarization: {militarization['aircraft']*100:.2f}\nShip Militarization: {militarization['ships']*100:.2f}%", title=f"Militarization Graph for {alliance.name} (`{alliance.id}`)", image_url=f"attachment://militarization_{alliance.id}.png", timestamp=self.bot.nations_update, footer="Data collected at", fields=[
            {"name": "Soldiers", "value": f"{alliance.get_soldiers():,}/{cities*15000:,}"},
            {"name": "Tanks", "value": f"{alliance.get_tanks():,}/{cities*1250:,}"},
            {"name": "Aircraft", "value": f"{alliance.get_aircraft():,}/{cities*75:,}"},
            {"name": "Ships", "value": f"{alliance.get_ships():,}/{cities*15:,}"},
            {"name": "Missiles", "value": f"{alliance.get_missiles():,}"},
            {"name": "Nukes", "value": f"{alliance.get_nukes():,}"},
        ])
        await ctx.send(file=image, embed=embed)

    @militarization.command(name="nation", aliases=["n", "nat", "me"])
    async def militarization_nation(self, ctx, *, search=None):
        if search == None:
            nation_id = (await rift.get_link_user(self.bot.connection, ctx.author.id))[1]
            nation = cache.nations[nation_id]
        else:
            try:
                user = (await commands.UserConverter().convert(ctx, search))
                try:
                    nation_id = (await rift.get_link_user(self.bot.connection, user.id))[1]
                except IndexError:
                    await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"No link found for user {user.mention}."))
                    return
                nation = cache.nations[nation_id]
            except commands.BadArgument:
                try:
                    nation_id = int(search)
                    nation = cache.nations[nation_id]
                except ValueError:
                    try:
                        nation = await rift.get_nation_name(self.bot.connection, search)
                        nation = cache.nations[nation[0]]
                    except IndexError:
                        await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"Nation `{search}` not found."))
                        return
                except KeyError:
                    await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"Nation `{search}` not found."))
                    return
        militarization = nation.get_militarization()
        await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"Total Militarization: {militarization['total']*100:.2f}%\nSoldier Militarization: {militarization['soldiers']*100:.2f}%\nTank Militarization: {militarization['tanks']*100:.2f}%\nAircraft Militarization: {militarization['aircraft']*100:.2f}%\nShip Militarization: {militarization['ships']*100:.2f}%", title=f"Militarization for {nation.name} (`{nation.id}`)", timestamp=self.bot.nations_update, footer="Data collected at", fields=[
            {"name": "Soldiers", "value": f"{nation.soldiers:,}/{nation.cities*15000:,}"},
            {"name": "Tanks", "value": f"{nation.tanks:,}/{nation.cities*1250:,}"},
            {"name": "Aircraft", "value": f"{nation.aircraft:,}/{nation.cities*75:,}"},
            {"name": "Ships", "value": f"{nation.ships:,}/{nation.cities*15:,}"},
            {"name": "Missiles", "value": f"{nation.missiles:,}"},
            {"name": "Nukes", "value": f"{nation.nukes:,}"},
        ]))


def setup(bot):
    bot.add_cog(Military(bot))
