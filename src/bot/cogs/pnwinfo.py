import discord
from discord.ext import commands

from ... import find
from ... import funcs as rift
from ...errors import AllianceNotFoundError, NationNotFoundError

NEWLINE = "\n"


class PnWInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="nation",
        aliases=["n", "check-link", "checklink", "nat"],
        help="Get information about a nation.",
    )
    async def nation(self, ctx, *, search=None):
        try:
            author, nation = await find.search_nation_author(ctx, search)
        except NationNotFoundError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"No nation found with argument `{search}`."
                )
            )
            return
        fields = [
            {"name": "Nation ID", "value": nation.id},
            {"name": "Nation Name", "value": nation.name},
            {"name": "Leader Name", "value": nation.leader},
            {"name": "War Policy", "value": nation.war_policy},
            {"name": "Domestic Policy", "value": nation.domestic_policy},
            {"name": "Continent", "value": nation.continent},
            {
                "name": "Color",
                "value": nation.color
                if nation.color != "Beige"
                else f"Beige ({nation.beige_turns:,} Turns)",
            },
            {
                "name": "Alliance",
                "value": f'[{repr(nation.alliance)}](https://politicsandwar.com/alliance/id={nation.alliance.id} "https://politicsandwar.com/alliance/id={nation.alliance.id}")'
                if nation.alliance is not None
                else "None",
            },
            {"name": "Alliance Position", "value": nation.alliance_position},
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
            {"name": "Average Infrastructure", "value": f"{nation.avg_infra():,.2f}"},
            {
                "name": "Actions",
                "value": f"[\U0001f4e7](https://politicsandwar.com/inbox/message/receiver={'+'.join(nation.leader.split(' '))} \"https://politicsandwar.com/inbox/message/receiver={'+'.join(nation.leader.split(' '))}\") "
                f"[\U0001f4e4](https://politicsandwar.com/nation/trade/create/nation={'+'.join(nation.name.split(' '))} \"https://politicsandwar.com/nation/trade/create/nation={'+'.join(nation.name.split(' '))}\") "
                f"[\U000026d4](https://politicsandwar.com/index.php?id=68&name={'+'.join(nation.name.split(' '))}&type=n \"https://politicsandwar.com/index.php?id=68&name={'+'.join(nation.name.split(' '))}&type=n\") "
                f'[\U00002694](https://politicsandwar.com/nation/war/declare/id={nation.id} "https://politicsandwar.com/nation/war/declare/id={nation.id}") '
                f'[\U0001f575](https://politicsandwar.com/nation/espionage/eid={nation.id} "https://politicsandwar.com/nation/espionage/eid={nation.id}") ',
            },
        ]
        embed = (
            rift.get_embed_author_guild(
                author,
                f'[Nation Page](https://politicsandwar.com/nation/id={nation.id} "https://politicsandwar.com/nation/id={nation.id}")',
                timestamp=self.bot.nations_update,
                footer="Data collected at",
                fields=fields,
            )
            if isinstance(author, discord.Guild)
            else rift.get_embed_author_member(
                author,
                f'[Nation Page](https://politicsandwar.com/nation/id={nation.id} "https://politicsandwar.com/nation/id={nation.id}")',
                timestamp=self.bot.nations_update,
                footer="Data collected at",
                fields=fields,
            )
        )
        await ctx.reply(embed=embed)

    @commands.command(name="me")
    async def me(self, ctx):
        await ctx.invoke(self.nation, search=None)

    @commands.command(
        name="alliance",
        aliases=["a"],
        help="Get information about an alliance.",
        case_insensitive=True,
    )
    async def alliance(self, ctx, *, search=None):
        alliance = await find.search_alliance(ctx, search)
        alliance_members = alliance.list_members(vm=False)
        alliance_score = sum(i.score for i in alliance_members)
        leaders = alliance.list_leaders()
        heirs = alliance.list_heirs()
        officers = alliance.list_officers()
        embed = rift.get_embed_author_member(
            ctx.author,
            f'[Alliance Page](https://politicsandwar.com/alliance/id={alliance.id} "https://politicsandwar.com/alliance/id={alliance.id}")\n[War Activity](https://politicsandwar.com/alliance/id={alliance.id}&display=war "https://politicsandwar.com/alliance/id={alliance.id}&display=war")',
            timestamp=self.bot.alliances_update,
            footer="Data collected at",
            fields=[
                {"name": "Alliance ID", "value": alliance.id},
                {"name": "Alliance Name", "value": alliance.name},
                {
                    "name": "Alliance Acronym",
                    "value": alliance.acronym if not alliance.acronym == "" else "None",
                },
                {"name": "Color", "value": alliance.color},
                {"name": "Rank", "value": f"#{alliance.rank}"},
                {
                    "name": "Members",
                    "value": f"[{len(alliance_members):,}](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true \"https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true\")",
                },
                {"name": "Score", "value": f"{alliance_score:,.2f}"},
                {
                    "name": "Average Score",
                    "value": f"{alliance_score/len(alliance_members) if len(alliance_members) != 0 else 0:,.2f}",
                },
                {"name": "Applicants", "value": f"{len(alliance.list_applicants()):,}"},
                {
                    "name": "Leaders",
                    "value": NEWLINE.join(
                        f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                        for i in leaders
                    )
                    if len(leaders) != 0
                    else "None",
                },
                {
                    "name": "Heirs",
                    "value": NEWLINE.join(
                        f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                        for i in heirs
                    )
                    if len(heirs) != 0
                    else "None",
                },
                {
                    "name": "Officers",
                    "value": NEWLINE.join(
                        f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                        for i in officers
                    )
                    if len(officers) != 0
                    else "None",
                },
                {
                    "name": "Forum Link",
                    "value": f'[Click Here]({alliance.forumurl} "{alliance.forumurl}")'
                    if alliance.forumurl is not None
                    else "None",
                },
                {
                    "name": "Discord Link",
                    "value": f'[Click Here]({alliance.discord} "{alliance.discord}")'
                    if alliance.discord is not None
                    else "None",
                },
                {
                    "name": "Vacation Mode",
                    "value": f"{len(alliance.list_members(vm=True)):,}",
                },
            ],
        ).set_thumbnail(url=alliance.flagurl)
        await ctx.reply(embed=embed)

    @commands.command(name="who", alises=["w", "who-is", "whois"])
    async def who(self, ctx, *, search=None):
        try:
            await find.search_nation(ctx, search)
            await ctx.invoke(self.nation, search=search)
        except NationNotFoundError:
            try:
                await find.search_alliance(ctx, search)
                await ctx.invoke(self.alliance, search=search)
            except AllianceNotFoundError:
                embed = rift.get_embed_author_member(
                    ctx.author, f"No nation or alliance found with argument `{search}`."
                )
                await ctx.reply(embed=embed)

    @commands.command(name="members")
    async def members(self, ctx, *, search=None):
        search = str(ctx.author.id) if search is None else search
        try:
            alliance = await rift.search_alliance(ctx, search)
        except AllianceNotFoundError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"No alliance found with argument `{search}`."
                )
            )
            raise AllianceNotFoundError
        members = alliance.list_members(vm=False)
        full = (
            "\n".join(
                [
                    f'[{i+1}. {member.id} | {member.name} | {member.score:,.2f}](https://politicsandwar.com/nation/id={member.id} "https://politicsandwar.com/nation/id={member.id}")'
                    for i, member in enumerate(members)
                ]
            )
            + "\n"
        )
        fields = []
        if len(full) >= 6000:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author,
                    f"There's too many members to display! You can find the full list [here](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true \"https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true\").",
                    title=alliance.name,
                )
            )
            return
        while full:
            i = full[:1024].rfind("\n")
            fields.append({"name": "\u200b", "value": full[: i + 1].strip("\n")})
            full = full[i + 1 :]
        embed = rift.get_embed_author_member(
            ctx.author,
            f"You can find the full list [here](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true \"https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true\").",
            timestamp=self.bot.nations_update,
            fields=fields,
            title=alliance.name,
        )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(PnWInfo(bot))
