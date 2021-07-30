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

    @commands._slash  # type: ignore
    @commands.command(
        name="nation",
        aliases=["n", "check-link", "checklink", "nat"],
        help="Get information about a nation.",
    )
    async def nation(self, ctx, *, nation=None):
        nation = await Nation.convert(ctx, nation)
        await ctx.reply(embed=await nation.get_info_embed(ctx))

    @commands._slash  # type: ignore
    @commands.command(name="me")
    async def me(self, ctx):
        await ctx.invoke(self.nation, nation=None)

    @commands._slash  # type: ignore
    @commands.command(
        name="alliance",
        aliases=["a"],
        help="Get information about an alliance.",
        case_insensitive=True,
    )
    async def alliance(self, ctx, *, alliance=None):
        alliance = await Alliance.convert(ctx, alliance)
        await ctx.reply(embed=await alliance.get_info_embed(ctx))

    @commands._slash  # type: ignore
    @commands.command(name="who", alises=["w", "who-is", "whois"])
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

    @commands._slash  # type: ignore
    @commands.command(name="members")
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

    @commands._slash  # type: ignore
    @commands.command(
        name="treaties",
        aliases=["t", "treaty"],
        description="Displays the treaties of the target alliance.",
    )
    async def treaties(self, ctx: commands.Context, *, alliance=None):
        alliance = await Alliance.convert(ctx, alliance)
        await alliance.make_attrs("treaties")
        await ctx.reply(
            embed=funcs.get_embed_author_member(ctx.author, str(alliance.treaties))
        )

    @commands._slash  # type: ignore
    @commands.command(name="spies")
    async def spies(self, ctx, *, nation: Nation):
        message = await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author, f"Fetching spies for {repr(nation)}..."
            )
        )
        num = await funcs.calculate_spies(nation)
        await message.edit(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{repr(nation)} has **{num}** spies.",
            )
        )


def setup(bot):
    bot.add_cog(PnWInfo(bot))
