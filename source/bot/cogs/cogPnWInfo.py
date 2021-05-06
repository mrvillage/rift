import discord
import asyncio
import json
import time
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level
from ...data.get import get_nation  # pylint: disable=relative-beyond-top-level


class PnWInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nation", aliases=["whois", "who", "check-link", "checklink", "nat"], help="Get information about a nation.", case_insensitive=True)
    async def nation(self, ctx, *, search=None):
        user = None
        if search == None:
            user = ctx.author
            user_id = ctx.author.id
            nation_id = (await rift.get_link_user(self.bot.connection, user_id))[1]
            nation = await rift.get_nation(self.bot.connection, nation_id)
        else:
            try:
                user = await commands.MemberConverter().convert(ctx, search)
                user_id = user.id
                nation_id = (await rift.get_link_user(self.bot.connection, user_id))[1]
                nation = await rift.get_nation(self.bot.connection, nation_id)
            except commands.errors.MemberNotFound:
                user = None
                try:
                    nation_id = int(search)
                    nation = await rift.get_nation(self.bot.connection, nation_id)
                    # await ctx.reply(embed=rift.get_embed_author_guild(ctx.guild,f"[Nation Page](https://politicsandwar.com/nation/id={nation_id})",timestamp=self.bot.nations_update,footer="Data collected at").add_field(name="Nation ID",value=nation_id,inline=True).add_field(name="Nation Name",value=nation[1],inline=True).add_field(name="Leader Name",value=nation[2],inline=True).add_field(name="War Policy",value=rift.get_war_policy(nation[4]),inline=True).add_field(name="Domestic Policy",value=rift.get_domestic_policy(nation[5]),inline=True).add_field(name="Color",value=rift.get_color(nation[6],nation[16]),inline=True).add_field(name="Alliance ID",value=rift.get_alliance_id(nation[7]),inline=True).add_field(name="Alliance Name",value=nation[8],inline=True).add_field(name="Alliance Position",value=rift.get_alliance_position(nation[9]),inline=True).add_field(name="Cities",value=nation[10],inline=True).add_field(name="Score",value=f"{nation[13]:.2f}",inline=True).add_field(name="Vacation Mode",value=nation[14]).add_field(name="Soldiers",value=f"{nation[19]:,}",inline=True).add_field(name="Tanks",value=f"{nation[20]:,}",inline=True).add_field(name="Aircraft",value=f"{nation[21]:,}",inline=True).add_field(name="Ships",value=f"{nation[22]:,}",inline=True).add_field(name="Missiles",value=f"{nation[23]:,}",inline=True).add_field(name="Nukes",value=f"{nation[24]:,}",inline=True))
                    # return
                except:
                    try:
                        nation = await rift.get_nation_name(self.bot.connection, search)
                        nation_id = nation[0]
                        # await ctx.reply(embed=rift.get_embed_author_guild(ctx.guild,f"[Nation Page](https://politicsandwar.com/nation/id={nation_id})",timestamp=self.bot.nations_update,footer="Data collected at").add_field(name="Nation ID",value=nation_id,inline=True).add_field(name="Nation Name",value=nation[1],inline=True).add_field(name="Leader Name",value=nation[2],inline=True).add_field(name="War Policy",value=rift.get_war_policy(nation[4]),inline=True).add_field(name="Domestic Policy",value=rift.get_domestic_policy(nation[5]),inline=True).add_field(name="Color",value=rift.get_color(nation[6],nation[16]),inline=True).add_field(name="Alliance ID",value=rift.get_alliance_id(nation[7]),inline=True).add_field(name="Alliance Name",value=nation[8],inline=True).add_field(name="Alliance Position",value=rift.get_alliance_position(nation[9]),inline=True).add_field(name="Cities",value=nation[10],inline=True).add_field(name="Score",value=f"{nation[13]:.2f}",inline=True).add_field(name="Vacation Mode",value=nation[14]).add_field(name="Soldiers",value=f"{nation[19]:,}",inline=True).add_field(name="Tanks",value=f"{nation[20]:,}",inline=True).add_field(name="Aircraft",value=f"{nation[21]:,}",inline=True).add_field(name="Ships",value=f"{nation[22]:,}",inline=True).add_field(name="Missiles",value=f"{nation[23]:,}",inline=True).add_field(name="Nukes",value=f"{nation[24]:,}",inline=True))
                        # return
                    except Exception:
                        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Nation `{search}` not found."))
                        return
        if user == None:
            try:
                user = self.bot.get_user((await rift.get_link_nation(self.bot.connection, nation[0]))[0])
            except Exception:
                await ctx.reply(embed=rift.get_embed_author_guild(ctx.guild, f"[Nation Page](https://politicsandwar.com/nation/id={nation_id})", timestamp=self.bot.nations_update, footer="Data collected at").add_field(name="Nation ID", value=nation_id, inline=True).add_field(name="Nation Name", value=nation[1], inline=True).add_field(name="Leader Name", value=nation[2], inline=True).add_field(name="War Policy", value=rift.get_war_policy(nation[4]), inline=True).add_field(name="Domestic Policy", value=rift.get_domestic_policy(nation[5]), inline=True).add_field(name="Color", value=rift.get_color(nation[6]) if nation[6] != 0 else f"Beige ({nation[16]} Turns)", inline=True).add_field(name="Alliance ID", value=rift.get_alliance_id(nation[7]), inline=True).add_field(name="Alliance Name", value=nation[8], inline=True).add_field(name="Alliance Position", value=rift.get_alliance_position(nation[9]), inline=True).add_field(name="Cities", value=nation[10], inline=True).add_field(name="Score", value=f"{nation[13]:.2f}", inline=True).add_field(name="Vacation Mode", value=nation[14]).add_field(name="Soldiers", value=f"{nation[19]:,}", inline=True).add_field(name="Tanks", value=f"{nation[20]:,}", inline=True).add_field(name="Aircraft", value=f"{nation[21]:,}", inline=True).add_field(name="Ships", value=f"{nation[22]:,}", inline=True).add_field(name="Missiles", value=f"{nation[23]:,}", inline=True).add_field(name="Nukes", value=f"{nation[24]:,}", inline=True))
                return
        await ctx.reply(embed=rift.get_embed_author_member(user, f"[Nation Page](https://politicsandwar.com/nation/id={nation_id})", timestamp=self.bot.nations_update, footer="Data collected at").add_field(name="Nation ID", value=nation_id, inline=True).add_field(name="Nation Name", value=nation[1], inline=True).add_field(name="Leader Name", value=nation[2], inline=True).add_field(name="War Policy", value=rift.get_war_policy(nation[4]), inline=True).add_field(name="Domestic Policy", value=rift.get_domestic_policy(nation[5]), inline=True).add_field(name="Color", value=rift.get_color(nation[6]) if nation[6] != 0 else f"Beige ({nation[16]} Turns)", inline=True).add_field(name="Alliance ID", value=rift.get_alliance_id(nation[7]), inline=True).add_field(name="Alliance Name", value=nation[8], inline=True).add_field(name="Alliance Position", value=rift.get_alliance_position(nation[9]), inline=True).add_field(name="Cities", value=nation[10], inline=True).add_field(name="Score", value=f"{nation[13]:,.2f}", inline=True).add_field(name="Vacation Mode", value=nation[14]).add_field(name="Soldiers", value=f"{nation[19]:,}", inline=True).add_field(name="Tanks", value=f"{nation[20]:,}", inline=True).add_field(name="Aircraft", value=f"{nation[21]:,}", inline=True).add_field(name="Ships", value=f"{nation[22]:,}", inline=True).add_field(name="Missiles", value=f"{nation[23]:,}", inline=True).add_field(name="Nukes", value=f"{nation[24]:,}", inline=True))

    @nation.error
    async def nation_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"No link found."))

    @commands.command(name="alliance", help="Get information about an alliance.", case_insensitive=True)
    async def alliance(self, ctx, *, search=None):
        user = ctx.author
        # user_id = ctx.author.id
        # nation_id = (await rift.get_link_user(self.bot.connection,user_id))[1]
        if search == None:
            try:
                nation_id = (await rift.get_link_user(self.bot.connection, ctx.author.id))[1]
                alliance_id = (await rift.get_nation(self.bot.connection, nation_id))[7]
                alliance = await rift.get_alliance(self.bot.connection, alliance_id)
            except:
                try:
                    alliance_id = int(search)
                    alliance = await rift.get_alliance(self.bot.connection, alliance_id)
                except:
                    try:
                        alliance = await rift.get_alliance_name(self.bot.connection, search)
                        alliance_id = alliance[0]
                    except:
                        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Alliance `{search}` not found."))
                        return
        else:
            try:
                alliance_id = int(search)
                alliance = await rift.get_alliance(self.bot.connection, alliance_id)
            except:
                try:
                    alliance = await rift.get_alliance_name(self.bot.connection, search)
                    alliance_id = alliance[0]
                except:
                    await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Alliance `{search}` not found."))
                    return
        alliance_members = await rift.calculate_alliance_members(self.bot.connection, alliance_id)
        alliance_vm_members = await rift.calculate_vm_alliance_members(self.bot.connection, alliance_id)
        embed = rift.get_embed_author_member(user, f"[Alliance Page](https://politicsandwar.com/alliance/id={alliance_id})", timestamp=self.bot.alliances_update, footer="Data collected at").add_field(name="Alliance ID", value=alliance_id, inline=True).add_field(name="Alliance Name", value=alliance[2], inline=True).add_field(name="Alliance Acronym", value=alliance[3] if not alliance[3] == "" else "None", inline=True).add_field(name="Color", value=alliance[4].capitalize(), inline=True).add_field(name="Rank", value=f"#{alliance[5]}", inline=True).add_field(
            name="Members", value=f"{len(alliance_members):,}", inline=True).add_field(name="Score", value=f"{sum([i[0] for i in alliance_members]):,.2f}", inline=True).add_field(name="Average Score", value=f"{sum([i[0] for i in alliance_members])/len(alliance_members) if len(alliance_members) != 0 else 0:,.2f}", inline=True).add_field(name="Applicants", value=f"{alliance[6]-len(alliance_members)-len(alliance_vm_members):,}", inline=True).set_thumbnail(url=alliance[12])
        if alliance[8] == None:
            embed.add_field(name="Leaders", value="None", inline=True)
        else:
            embed.add_field(name="Leaders", value=", ".join(
                [str(i) for i in json.loads(alliance[8])]), inline=True)
        if alliance[10] == None:
            embed.add_field(name="Heirs", value="None", inline=True)
        else:
            embed.add_field(name="Heirs", value=", ".join(
                [str(i) for i in json.loads(alliance[10])]), inline=True)
        if alliance[9] == None:
            embed.add_field(name="Officers", value="None", inline=True)
        else:
            embed.add_field(name="Officers", value=", ".join(
                [str(i) for i in json.loads(alliance[9])]), inline=True)
        if alliance[13] is not None:
            embed.add_field(
                name="Forums Link", value=f"[Click Here]({str(alliance[13])}\"{str(alliance[13])}\")", inline=True)
        else:
            embed.add_field(name="Forums Link", value="None", inline=True)
        if alliance[14] is not None:
            embed.add_field(
                name="Discord Link", value=f"[Click Here]({str(alliance[14])}\"{str(alliance[14])}\")", inline=True)
        else:
            embed.add_field(name="Discord Link", value="None", inline=True)
        embed.add_field(name="Vacation Mode",
                        value=f"{len(alliance_vm_members):,}", inline=True)
        await ctx.reply(embed=embed)

    @commands.command(name="members")
    async def members(self, ctx, *, search=None):
        user = ctx.author
        user_id = ctx.author.id
        nation_id = (await rift.get_link_user(self.bot.connection, user_id))[1]
        if search == None:
            nation_id = (await rift.get_link_user(self.bot.connection, ctx.author.id))[1]
            alliance_id = (await rift.get_nation(self.bot.connection, nation_id))[7]
            alliance = await rift.get_alliance(self.bot.connection, alliance_id)
        else:
            try:
                alliance_id = int(search)
                alliance = await rift.get_alliance(self.bot.connection, alliance_id)
            except:
                try:
                    alliance = await rift.get_alliance_name(self.bot.connection, search)
                    alliance_id = alliance[0]
                except:
                    await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Alliance `{search}` not found."))
                    return
        members = await rift.execute_read_query(self.bot.connection, f"SELECT nation_id,nation,score FROM nations WHERE alliance_id = {alliance_id} AND alliance_position != 1 AND v_mode = 'False' ORDER BY score DESC;")
        full = "\n".join(
            [f"{i+1}. {members[i][0]} | {members[i][1]} | {members[i][2]:,.2f}" for i in range(len(members))])+"\n"
        fields = []
        while len(full) >= 2048:
            i = full[:2048].rfind("\n")
            fields.append(full[:i+2].strip("\n"))
            full = full[i+3:]
        if len(fields) == 0:
            fields.append(full)
        embed = rift.get_embed_author_member(
            user, fields[0], timestamp=self.bot.nations_update)
        if len(fields) > 1:
            for i in range(1, len(fields)):
                embed.add_field(name="\u200b", value=fields[i])
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(PnWInfo(bot))
