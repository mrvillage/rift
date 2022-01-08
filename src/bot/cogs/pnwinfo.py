from __future__ import annotations

import time
from datetime import datetime
from typing import TYPE_CHECKING, List

import discord
from discord.ext import commands
from discord.utils import MISSING

from _typings import Field

from ... import funcs
from ...cache import cache
from ...data.classes import Alliance, Nation
from ...errors import (
    AllianceNotFoundError,
    EmbedErrorMessage,
    NationNotFoundError,
    NationOrAllianceNotFoundError,
)
from ...ref import Rift, RiftContext
from ...views import AlliancesPaginator, Colors, TreasuresView


class PnWInfo(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.command(
        name="nation",
        aliases=["n", "check-link", "checklink", "nat"],
        brief="Get information about a nation.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
        descriptions={
            "nation": "The nation to get information about, defaults to your nation.",
        },
    )
    async def nation(self, ctx: RiftContext, *, nation: Nation = MISSING):
        nation = nation or await Nation.convert(ctx, nation)
        await ctx.reply(embed=nation.get_info_embed(ctx))

    @commands.command(
        name="me",
        brief="Get information about your nation.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def me(self, ctx: RiftContext):
        await ctx.invoke(self.nation, nation=MISSING)

    @commands.command(
        name="alliance",
        aliases=["a"],
        brief="Get information about an alliance.",
        case_insensitive=True,
        type=(commands.CommandType.default, commands.CommandType.chat_input),
        descriptions={
            "alliance": "The alliance to get information about, defaults to your alliance.",
        },
    )
    async def alliance(self, ctx: RiftContext, *, alliance: Alliance = MISSING):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        await ctx.reply(embed=alliance.get_info_embed(ctx))

    @commands.command(
        name="who",
        aliases=["w", "who-is", "whois"],
        brief="Get information about a nation or alliance.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
        descriptions={
            "search": "The nation or alliance to get information about, defaults to your nation.",
        },
    )
    async def who(self, ctx: RiftContext, *, search: str = MISSING):
        if search is MISSING:
            try:
                return await ctx.invoke(
                    self.nation,
                    nation=await Nation.convert(ctx, search, False),
                )
            except NationNotFoundError:
                raise NationOrAllianceNotFoundError(search)
        try:
            await ctx.invoke(
                self.nation, nation=await Nation.convert(ctx, search, False)
            )
        except NationNotFoundError:
            try:
                await ctx.invoke(
                    self.alliance, alliance=await Alliance.convert(ctx, search, False)
                )
            except AllianceNotFoundError:
                try:
                    await ctx.invoke(
                        self.nation, nation=await Nation.convert(ctx, search, True)
                    )
                except NationNotFoundError:
                    try:
                        await ctx.invoke(
                            self.alliance,
                            alliance=await Alliance.convert(ctx, search, True),
                        )
                    except AllianceNotFoundError:
                        raise NationOrAllianceNotFoundError(search)

    @commands.command(
        name="members",
        brief="Get a list of the members of an alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "alliance": "The alliance to get members of, defaults to your alliance.",
        },
    )
    async def members(self, ctx: RiftContext, *, alliance: Alliance = MISSING):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        await alliance.make_attrs("members")
        full = (
            "\n".join(
                f"[{i+1}. {member.id} | {member.name} | {member.score:,.2f}](https://politicsandwar.com/nation/id={member.id})"
                for i, member in enumerate(alliance.members)
            )
            + "\n"
        )
        fields: List[Field] = []
        if len(full) >= 5120:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"There's too many members to display! You can find the full list [here](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true).",
                    title=alliance.name,
                    color=discord.Color.orange(),
                )
            )
            return
        while full:
            i = full[:1024].rfind("\n")
            fields.append({"name": "\u200b", "value": full[: i + 1].strip("\n")})
            full = full[i + 1 :]
        embed = funcs.get_embed_author_member(
            ctx.author,
            f"You can find the full list [here](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true).",
            fields=fields,
            title=alliance.name,
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)

    @commands.command(
        name="treaties",
        aliases=["t", "treaty"],
        brief="Get the treaties of an alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "alliance": "The alliance to get treaties of, defaults to your alliance.",
        },
    )
    async def treaties(self, ctx: RiftContext, *, alliance: Alliance = MISSING):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        await alliance.make_attrs("treaties")
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(str(i) for i in alliance.treaties),
                color=discord.Color.blue(),
            )
        )

    @commands.command(
        name="spies",
        brief="Get the spies of a nation.",
        type=commands.CommandType.chat_input,
        descriptions={
            "nation": "The nation to get spies of.",
        },
    )
    async def spies(self, ctx: RiftContext, *, nation: Nation):
        await ctx.interaction.response.defer()
        num = await funcs.calculate_spies(nation)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{repr(nation)} has **{num}** spies.",
                color=discord.Color.blue(),
            )
        )

    @commands.command(
        name="revenue",
        brief="Get the revenue of a nation or alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "search": "The nation or alliance to get revenue of, defaults to your nation.",
            "alliance": "Whether to only search for a matching alliance.",
            "fetch_spies": "Fetches spies for every nation being calculated. Incredibly slow, need to be whitelisted.",
        },
    )
    async def revenue(
        self,
        ctx: RiftContext,
        *,
        search: str = MISSING,
        alliance: bool = False,
        fetch_spies: bool = False,
    ):  # sourcery no-metrics
        if search is MISSING and alliance or search is not MISSING and alliance:
            search_ = await Alliance.convert(ctx, search)
        elif search is MISSING:
            search_ = await Nation.convert(ctx, search)
        else:
            search_ = await funcs.convert_nation_or_alliance(ctx, search)
        if fetch_spies and ctx.author.id != 258298021266063360:
            fetch_spies = False
        await ctx.interaction.response.defer()
        try:
            rev = await search_.calculate_revenue(fetch_spies=fetch_spies)
        except IndexError:
            raise EmbedErrorMessage(
                ctx.author,
                f"Something went wrong calculating {repr(search_)}'s revenue. It's probably a turn, try again in a few minutes!",
            )
        if TYPE_CHECKING:
            from ...data.classes import Resources

            assert (
                isinstance(rev["gross_income"], Resources)
                and isinstance(rev["net_income"], Resources)
                and isinstance(rev["upkeep"], Resources)
                and isinstance(rev["gross_total"], dict)
                and isinstance(rev["net_total"], dict)
                and isinstance(rev["upkeep_total"], dict)
            )
        upkeeps = {
            key: f"Upkeep: {getattr(rev['upkeep'], key):,.2f} (${rev['upkeep_total'][key]:,.2f})\n"
            for key in rev["gross_income"].to_dict()
            if key not in {"credit", "gasoline", "munitions", "steel", "aluminum"}
        }
        fields: List[Field] = [
            {
                "name": key.capitalize(),
                "value": f"Gross: {getattr(rev['gross_income'], key):,.2f} (${rev['gross_total'][key]:,.2f})\n{upkeeps.get(key, '')}Net: {getattr(rev['net_income'], key):,.2f} (${rev['net_total'][key]:,.2f})",
            }
            for key in rev["gross_income"].to_dict()
            if key not in {"money", "credit"}
        ]
        fields.insert(
            0,
            {
                "name": "Money",
                "value": f"Gross: ${rev['gross_income'].money:,.2f}\nUpkeep: ${rev['upkeep'].money:,.2f}\nNet: ${rev['net_income'].money:,.2f}"
                + (
                    f"\nTrade Bonus: ${rev['trade_bonus']:,}"
                    if "trade_bonus" in rev
                    else ""
                )
                + (
                    f"\nNew Player Bonus: ${rev['new_player_bonus']:,}"
                    if "new_player_bonus" in rev
                    else ""
                ),
            },
        )
        fields.append(
            {
                "name": "Total",
                "value": f"Gross: ${sum(rev['gross_total'].to_dict().values())+rev['gross_income'].money:,.2f}\nUpkeep: ${sum(rev['upkeep_total'].to_dict().values())+rev['upkeep'].money:,.2f}\nNet: ${sum(rev['net_total'].to_dict().values())+rev['net_income'].money:,.2f}"
                + ("" if fetch_spies else "\nNote: Spies not included"),
            }
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Revenue for {repr(search_)}",
                fields=fields,
                color=discord.Color.green(),
            )
        )

    @commands.command(
        name="alliances",
        aliases=["as"],
        brief="Get a list of alliances.",
        type=commands.CommandType.chat_input,
        descriptions={
            "page": "The page of alliances to get, defaults to 1.",
        },
    )
    async def alliances(self, ctx: RiftContext, page: int = 1):
        max_page = (
            (len(cache.alliances) // 50) + 1
            if len(cache.alliances) % 50
            else (len(cache.alliances) // 50)
        )
        if page > max_page or page < 0:
            raise EmbedErrorMessage(
                ctx.author,
                f"Page {page} does not exist.",
            )
        offset = (page - 1) * 50
        alliances = sorted(iter(cache.alliances), key=lambda x: x.rank)[
            offset : offset + 50
        ]
        embed = funcs.get_embed_author_member(
            ctx.author,
            f"Page **{page}** of **{max_page}**\n"
            + "Rank: ID, Name, Score, Members\n"
            + "\n".join(
                f"**#{i.rank}**: {i.id}, {i.name}, {i.score:,.2f}, {i.member_count}"
                for i in alliances
            ),
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed, view=AlliancesPaginator(max_page, page))

    @commands.command(
        name="colors",
        brief="Get a list of color bloc information.",
        type=commands.CommandType.chat_input,
    )
    async def colors(self, ctx: RiftContext):
        colors = {i.color: i for i in cache.colors}
        nations = [i.color for i in cache.nations]
        nations = {i.color: nations.count(i.color.capitalize()) for i in cache.colors}
        average_bonus = (
            sum(i.bonus for i in colors.values() if i.color not in {"beige", "gray"})
            / len(colors)
        ) - 2
        fields: List[Field] = [
            {
                "name": i.color.capitalize(),
                "value": f"Name: {i.name}\nTurn Bonus: ${i.bonus:,.0f}\nNations on Color: {nations[i.color]:,}",
            }
            for i in colors.values()
        ]
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Average Bonus: ${average_bonus:,.2f}",
                fields=fields,
                color=discord.Color.blue(),
            ),
            view=Colors(),
        )

    @commands.command(
        name="treasures",
        brief="Get a list of treasure information.",
        type=commands.CommandType.chat_input,
        descriptions={
            "page": "The page of treasures to get, can be 1 or 2, defaults to 1.",
        },
    )
    async def treasures(self, ctx: RiftContext, page: int = 1):
        if page < 1:
            page = 1
        elif page > 2:
            page = 2
        fields: List[Field] = [
            {
                "name": i.name,
                "value": f"Color: {i.color.capitalize()}\nBonus: %{i.bonus}\nSpawn Date: <t:{int(time.mktime(datetime.fromisoformat(i.spawn_date).timetuple()))}:D>\nNation: [{i.nation}](https://politicsandwar.com/nation/id={i.nation_id})",
            }
            for i in list(cache.treasures)[(page - 1) * 15 : (page) * 15]
        ]
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Page **{page}** of **2**",
                fields=fields,
                color=discord.Color.blue(),
            ),
            view=TreasuresView(page),
        )

    @commands.command(  # type: ignore
        name="projects",
        brief="Get a nations projects.",
        type=commands.CommandType.chat_input,
        descriptions={
            "nation": "The nation to get information about, defaults to your nation.",
        },
    )
    async def projects(self, ctx: RiftContext, nation: Nation = MISSING):
        nation = nation or await Nation.convert(ctx, nation)
        projs = await nation.fetch_projects()
        projects = {
            "Advanced Engineering Corps": projs.adv_engineering_corps,
            "Advanced Urban Planning": projs.adv_city_planning,
            "Arable Land Agency": projs.arable_land_agency,
            "Arms Stockpile": projs.armss,
            "Bauxiteworks": projs.bauxitew,
            "Center for Civil Engineering": projs.cfce,
            "Clinical Research Center": projs.clinical_research_center,
            "Emergency Gasoline Reserve": projs.egr,
            "Green Technologies": projs.green_tech,
            "Intelligence Agency": projs.cia,
            "International Trade Center": projs.itc,
            "Iron Dome": projs.irond,
            "Ironworks": projs.ironw,
            "Mass Irrigation": projs.massirr,
            "Missile Launch Pad": projs.mlp,
            "Moon Landing": projs.moon_landing,
            "Nuclear Research Facility": projs.nrf,
            "Pirate Economy": projs.pirate_economy,
            "Propaganda Bureau": projs.propb,
            "Recycling Initiative": projs.recycling_initiative,
            "Space Program": projs.space_program,
            "Specialized Police Training Program": projs.specialized_police_training,
            "Spy Satellite": projs.spy_satellite,
            "Telecommunication Satellite": projs.telecom_satellite,
            "Uranium Enrichment Program": projs.uap,
            "Urban Planning": projs.city_planning,
            "Vital Defense System": projs.vds,
        }
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"[{repr(nation)}](https://politicsandwar.com/nation/id={nation.id}) has {sum(projects.values()):,}/{len(projects.keys()):,} projects and is using {sum(projects.values())}/{sum(i.infrastructure for i in nation.partial_cities)//5000 + 1:,.0f} project slots.\n\n{', '.join(key for key, value in projects.items() if value)}",
                color=discord.Color.blue(),
            )
        )

    @commands.group(
        name="top-revenue",
        brief="Get top revenue information.",
        type=commands.CommandType.chat_input,
    )
    async def top_revenue(self, ctx: RiftContext):
        ...

    @top_revenue.command(  # type: ignore
        name="alliances",
        brief="Get top alliance revenue information.",
        type=commands.CommandType.chat_input,
        descriptions={
            "top_fifty": "Calculate top fifty alliances instead of the top twenty-five, adds about two minutes of wait time."
        },
    )
    async def top_revenue_alliances(self, ctx: RiftContext, top_fifty: bool = False):
        await ctx.interaction.response.defer()
        top_alliances = sorted(
            [
                (i, await i.calculate_revenue())
                for i in sorted(cache.alliances, key=lambda x: x.score, reverse=True)[
                    : 25 + (25 * top_fifty)
                ]
            ],
            key=lambda x: sum(x[1]["net_total"].to_dict().values())
            + x[1]["net_income"].money,
            reverse=True,
        )[:10]
        fields: List[Field] = [
            {
                "name": f"#{index+1}",
                "value": f"[{repr(i[0])}](https://politicsandwar.com/alliance/id={i[0].id})\nGross: ${sum(i[1]['gross_total'].to_dict().values())+i[1]['gross_income'].money:,.2f}\nUpkeep: ${sum(i[1]['upkeep_total'].to_dict().values())+i[1]['upkeep'].money:,.2f}\nNet: ${sum(i[1]['net_total'].to_dict().values())+i[1]['net_income'].money:,.2f}",
            }
            for index, i in enumerate(top_alliances)
        ]
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Note: For performance, only the top {'fifty' if top_fifty else 'twenty-five'} alliances are taken into account.",
                title="Top Alliance Revenues:",
                fields=fields,
                color=discord.Color.green(),
            ),
        )

    @top_revenue.command(  # type: ignore
        name="nations",
        brief="Get top nation revenue information.",
        type=commands.CommandType.chat_input,
    )
    async def top_revenue_nations(self, ctx: RiftContext):
        await ctx.interaction.response.defer()
        top_alliances = sorted(
            [
                (i, await i.calculate_revenue())
                for i in sorted(cache.nations, key=lambda x: x.score, reverse=True)[:50]
            ],
            key=lambda x: sum(x[1]["net_total"].to_dict().values())
            + x[1]["net_income"].money,
            reverse=True,
        )[:10]
        fields: List[Field] = [
            {
                "name": f"#{index+1}",
                "value": f"[{repr(i[0])}](https://politicsandwar.com/alliance/id={i[0].id})\nGross: ${sum(i[1]['gross_total'].to_dict().values())+i[1]['gross_income'].money:,.2f}\nUpkeep: ${sum(i[1]['upkeep_total'].to_dict().values())+i[1]['upkeep'].money:,.2f}\nNet: ${sum(i[1]['net_total'].to_dict().values())+i[1]['net_income'].money:,.2f}",
            }
            for index, i in enumerate(top_alliances)
        ]
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                title="Top Nation Revenues:",
                fields=fields,
                color=discord.Color.green(),
            ),
        )

    @top_revenue.command(  # type: ignore
        name="alliance",
        brief="Get top nation revenue information of an alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "alliance": "The alliance to get revenue about, defaults to your alliance.",
        },
    )
    async def top_revenue_alliance(
        self, ctx: RiftContext, alliance: Alliance = MISSING
    ):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        await ctx.interaction.response.defer()
        top_alliances = sorted(
            [(i, await i.calculate_revenue()) for i in alliance.members],
            key=lambda x: sum(x[1]["net_total"].to_dict().values())
            + x[1]["net_income"].money,
            reverse=True,
        )[:10]
        fields: List[Field] = [
            {
                "name": f"#{index+1}",
                "value": f"[{repr(i[0])}](https://politicsandwar.com/alliance/id={i[0].id})\nGross: ${sum(i[1]['gross_total'].to_dict().values())+i[1]['gross_income'].money:,.2f}\nUpkeep: ${sum(i[1]['upkeep_total'].to_dict().values())+i[1]['upkeep'].money:,.2f}\nNet: ${sum(i[1]['net_total'].to_dict().values())+i[1]['net_income'].money:,.2f}",
            }
            for index, i in enumerate(top_alliances)
        ]
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                title=f"Top Nation Revenues for {repr(alliance)}:",
                fields=fields,
                color=discord.Color.green(),
            ),
        )


def setup(bot: Rift):
    bot.add_cog(PnWInfo(bot))
