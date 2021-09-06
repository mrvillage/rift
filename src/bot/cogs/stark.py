from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

import discord
import pnwkit
from discord.ext import commands, tasks
from src.data.classes.bank.transaction import Transaction
from src.data.classes.resources import Resources
from src.funcs.bank.bank import withdraw

from ... import funcs
from ...data.classes import Alliance, Nation, TradePrices
from ...ref import Rift
from ...errors import AllianceNotFoundError

OFFSHORE_ID = 9014


class Confirm(discord.ui.View):
    """
    self.interaction is available so the command can perform a result on it's own
    """

    value: Optional[bool]

    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)
        return 240113452616515584 in [role.id for role in interaction.user.roles]

    @discord.ui.button(
        custom_id="bVks6is6YFCGzORPwfmLJXrcIWBK9HzyWg8DpYJGrqyl2UKc4aWmrUTmbsNfwCgWOV3BkUXp087FOvEK",
        label="Yes",
        style=discord.ButtonStyle.green,
    )
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.interaction = interaction
        self.value = True
        await interaction.response.defer()
        main = await Alliance.fetch(3683)
        offshore = await Alliance.fetch(OFFSHORE_ID)
        resources = await main.get_resources()
        transaction = Transaction(resources=resources)
        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)
        complete = await withdraw(
            transaction=transaction,
            receiver=offshore,
            note=f"Automatic offshore deposit approved by {interaction.user.name}#{interaction.user.discriminator}",
        )
        if not complete:
            complete = await withdraw(
                transaction=transaction,
                receiver=offshore,
                note=f"Automatic offshore deposit approved by {interaction.user.name}#{interaction.user.discriminator}",
            )
        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)
        if not complete:
            return await interaction.followup.send(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    "Something went wrong sending the alliance bank. Please try again later.",
                )
            )
        await interaction.followup.send(
            embed=funcs.get_embed_author_member(
                interaction.user, f"Alliance bank transfer complete. Sent {resources}"
            )
        )
        self.stop()

    @discord.ui.button(
        custom_id="r2eTyOp98ZMQ7MHdGkskhxK7QEVZKPfOmmZoYD5Ncj3IcKdOfVOzHA58O9zSWn9mL0SuXjxcZ6V5dQVW",
        label="No",
        style=discord.ButtonStyle.red,
    )
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.interaction = interaction
        self.value = False
        await interaction.edit_original_message(view=None)
        self.stop()


class HouseStark(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.bank_send_task.start()

    @commands.command(name="mmr", help="Check to see if a nation meets MMR.")
    async def mmr(self, ctx: commands.Context, *, nation: Nation = None):
        nation = nation or await Nation.convert(ctx, nation)
        author_nation = await Nation.convert(ctx, None)
        if nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Stockpiles doesn't apply to that nation!",
                    color=discord.Color.red(),
                )
            )
            return
        if author_nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have permission to use that command!!",
                    color=discord.Color.red(),
                )
            )
            return
        mmr = {
            "soldiers": 0 * 3000 * nation.cities,
            "tanks": 2 * 250 * nation.cities,
            "aircraft": 5 * 15 * nation.cities,
            "ships": 0 * 5 * nation.cities,
        }
        if all(getattr(nation, key) >= mmr[key] for key in mmr):
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, f"{nation} meets MMR!", color=discord.Color.green()
                )
            )
            return
        amounts = "\n".join(
            f"**{key.capitalize()}** - {getattr(nation, key):,}/{mmr[key]:,} ({getattr(nation, key)/mmr[key]:.2%})"
            for key in mmr
            if getattr(nation, key) < mmr[key]
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{nation} doesn't meet MMR!\n\n{amounts}",
                color=discord.Color.orange(),
            )
        )

    @commands.command(
        name="stockpile",
        aliases=["stockpiles"],
        help="Check to see if a nation meets stockpile requirements.",
    )
    async def stockpile(self, ctx: commands.Context, *, nation: Nation = None):
        nation = nation or await Nation.convert(ctx, nation)
        nat = await pnwkit.async_nation_query(
            {"id": nation.id},
            "money",
            "food",
            "uranium",
            "steel",
            "aluminum",
            "gasoline",
            "munitions",
        )
        if TYPE_CHECKING:
            assert isinstance(nat, tuple)
        nat = nat[0]
        author_nation = await Nation.convert(ctx, None)
        if nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Stockpiles doesn't apply to that nation!",
                    color=discord.Color.red(),
                )
            )
            return
        if author_nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have permission to use that command!!",
                    color=discord.Color.red(),
                )
            )
            return
        stockpile = {
            "money": 1000000 * nation.cities,
            "food": 10000 + (2000 * nation.cities),
            "uranium": 100 * nation.cities,
            "steel": 3000 * nation.cities,
            "aluminum": 1000 * nation.cities,
            "gasoline": 3600 * nation.cities,
            "munitions": 5400 * nation.cities,
        }
        if all(getattr(nat, key) >= stockpile[key] for key in stockpile):
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{nation} meets stockpiles!",
                    color=discord.Color.green(),
                )
            )
            return
        prices: TradePrices = await funcs.get_trade_prices()
        amounts = []
        cost = 0
        for key, needs in stockpile.items():
            has = getattr(nat, key)
            if has < needs:
                if key != "money":
                    price = getattr(prices, key)
                    amount = (needs - has) * price.lowest_sell.price
                    amounts.append(
                        f"**{key.capitalize()}** - {has:,.2f}/{needs:,.2f} ({has/needs:.2%})\n${amount:,.2f} for {needs-has:,.2f}"
                    )
                else:
                    amount = needs - has
                    amounts.append(
                        f"**{key.capitalize()}** - {has:,.2f}/{needs:,.2f} ({has/needs:.2%})\n${amount:,.2f}"
                    )
                cost += amount
        amounts = "\n".join(amounts)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{nation} doesn't meet stockpiles!\n\n{amounts}\n\n**Total:** ${cost:,.2f}",
                color=discord.Color.orange(),
            )
        )

    @tasks.loop(hours=24)
    async def bank_send_task(self):
        channel = self.bot.get_channel(239099900174925824)
        if not channel:
            return
        try:
            offshore = await Alliance.fetch(OFFSHORE_ID)
        except AllianceNotFoundError:
            return
        if TYPE_CHECKING:
            assert isinstance(channel, discord.TextChannel)
        await channel.send(
            embed=funcs.get_embed_author_guild(
                channel.guild,
                f"Please authorize sending the contents of the to {repr(offshore)}.",
            ),
            view=Confirm(),
        )

    @bank_send_task.before_loop
    async def before_bank_send_task(self):
        await self.bot.wait_until_ready()
        now = discord.utils.utcnow()
        wait = now.replace(hour=22, minute=5, second=0)
        while wait < now:
            wait += datetime.timedelta(days=1)
        print(f"Waiting until {wait} to send bank!")
        await self.bot.update_pnw_session()
        await discord.utils.sleep_until(wait)


def setup(bot: Rift) -> None:
    bot.add_cog(HouseStark(bot))
