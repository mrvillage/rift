from typing import TYPE_CHECKING, Union
from src.errors.spies import SpiesNotFoundError
import discord
from discord.ext import commands

from ... import find
from ... import funcs
from ...data.classes import Alliance, Nation
from ...errors import AllianceNotFoundError, NationNotFoundError


class PnWInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="nation",
        aliases=["n", "check-link", "checklink", "nat"],
        help="Get information about a nation.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def nation(self, ctx, *, nation=None):
        nation = await Nation.convert(ctx, nation)
        await ctx.reply(embed=await nation.get_info_embed(ctx))

    @commands.command(
        name="me",
        help="Get information about your nation.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def me(self, ctx):
        await ctx.invoke(self.nation, nation=None)

    @commands.command(
        name="alliance",
        aliases=["a"],
        help="Get information about an alliance.",
        case_insensitive=True,
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def alliance(self, ctx, *, alliance=None):
        alliance = await Alliance.convert(ctx, alliance)
        await ctx.reply(embed=await alliance.get_info_embed(ctx))

    @commands.command(
        name="who",
        aliases=["w", "who-is", "whois"],
        help="Get information about a nation or alliance.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def who(self, ctx, *, search=None):
        try:
            await find.search_nation(ctx, search)
            await ctx.invoke(self.nation, nation=search)
        except NationNotFoundError:
            try:
                await find.search_alliance(ctx, search)
                await ctx.invoke(self.alliance, alliance=search)
            except AllianceNotFoundError:
                embed = funcs.get_embed_author_member(
                    ctx.author, f"No nation or alliance found with argument `{search}`."
                )
                await ctx.reply(embed=embed)

    @commands.command(
        name="members",
        help="Get a list of the members of an alliance.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def members(self, ctx, *, search=None):
        search = str(ctx.author.id) if search is None else search
        try:
            alliance = await funcs.search_alliance(ctx, search)
        except AllianceNotFoundError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, f"No alliance found with argument `{search}`."
                )
            )
            raise AllianceNotFoundError
        await alliance.make_attrs("members")
        full = (
            "\n".join(
                f'[{i+1}. {member.id} | {member.name} | {member.score:,.2f}](https://politicsandwar.com/nation/id={member.id} "https://politicsandwar.com/nation/id={member.id}")'
                for i, member in enumerate(alliance.members)
            )
            + "\n"
        )
        fields = []
        if len(full) >= 6000:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
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
        embed = funcs.get_embed_author_member(
            ctx.author,
            f"You can find the full list [here](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true \"https://politicsandwar.com/index.php?id=15&keyword={'+'.join(alliance.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true\").",
            fields=fields,
            title=alliance.name,
        )
        await ctx.reply(embed=embed)

    @commands.command(
        name="treaties",
        aliases=["t", "treaty"],
        description="Get the treaties of an alliance.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def treaties(self, ctx: commands.Context, *, alliance=None):
        alliance = await Alliance.convert(ctx, alliance)
        await alliance.make_attrs("treaties")
        await ctx.reply(
            embed=funcs.get_embed_author_member(ctx.author, str(alliance.treaties))
        )

    @commands.command(
        name="spies",
        help="Get the spies of a nation.",
        type=commands.CommandType.chat_input,
    )
    async def spies(self, ctx, *, nation: Nation):
        await ctx.interaction.response.defer()
        num = await funcs.calculate_spies(nation)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{repr(nation)} has **{num}** spies.",
            )
        )

    @commands.command(
        name="revenue",
        help="Get the revenue of a nation or alliance.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def revenue(self, ctx, *, search: Union[Alliance, Nation] = None):
        search = search if search is not None else await Nation.convert(ctx, search)
        message = await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author, f"Fetching revenue for {repr(search)}..."
            )
        )
        try:
            rev = await search.calculate_revenue()
        except IndexError:
            return await message.edit(
                content=f"Something went wrong calculating {repr(search)}'s revenue. It's probably a turn, try again in a few minutes!"
            )
        if TYPE_CHECKING:
            from ...data.classes import Resources

            assert (
                isinstance(rev["gross_income"], Resources)
                and isinstance(rev["net_income"], Resources)
                and isinstance(rev["gross_total"], dict)
                and isinstance(rev["net_total"], dict)
            )
        fields = [
            {
                "name": key.capitalize(),
                "value": f"Gross: {getattr(rev['gross_income'], key):,.2f} (${rev['gross_total'][key]:,.2f})\nNet: {getattr(rev['net_income'], key):,.2f} (${rev['net_total'][key]:,.2f})",
            }
            for key in rev["gross_income"].__dict__
            if key not in {"money", "credit"}
        ]
        fields.insert(
            0,
            {
                "name": "Money",
                "value": f"Gross: {rev['gross_income'].money:,.2f}\nNet: {rev['net_income'].money:,.2f}"
                + (
                    f"\nTrade Bonus: {rev['trade_bonus']:,}"
                    if "trade_bonus" in rev
                    else ""
                )
                + (
                    f"\nNew Player Bonus: {rev['new_player_bonus']:,}"
                    if "new_player_bonus" in rev
                    else ""
                ),
            },
        )
        fields.append(
            {
                "name": "Total",
                "value": f"Gross: ${sum(rev['gross_total'].__dict__.values())+rev['gross_income'].money:,.2f}\nNet: ${sum(rev['net_total'].__dict__.values())+rev['net_income'].money:,.2f}",
            }
        )
        await message.edit(
            embed=funcs.get_embed_author_member(
                ctx.author, f"Revenue for {repr(search)}", fields=fields
            )
        )


def setup(bot):
    bot.add_cog(PnWInfo(bot))
