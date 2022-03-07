from __future__ import annotations

import datetime
import os.path
from typing import TYPE_CHECKING, Any, List, Optional

import discord
import pnwkit
from discord.ext import commands, tasks
from discord.utils import MISSING
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from ... import funcs
from ...cache import cache
from ...data.classes import Alliance, Nation, Resources
from ...env import (
    HS_AIRCRAFT_MMR,
    HS_ALUMINUM_REQ,
    HS_FOOD_REQ,
    HS_FOOD_REQ_START,
    HS_GASOLINE_REQ,
    HS_MONEY_REQ,
    HS_MUNITIONS_REQ,
    HS_NO_CUSTOM_ID,
    HS_OFFSHORE_ID,
    HS_SHIP_MMR,
    HS_SOLDIER_MMR,
    HS_SPREADSHEET_ID,
    HS_STEEL_REQ,
    HS_TANK_MMR,
    HS_URANIUM_REQ,
    HS_YES_CUSTOM_ID,
)
from ...errors import AllianceNotFoundError
from ...funcs import withdraw
from ...ref import Rift, RiftContext


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

    @discord.ui.button(  # type: ignore
        custom_id=HS_YES_CUSTOM_ID,
        label="Yes",
        style=discord.ButtonStyle.green,
    )
    async def yes(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        self.interaction = interaction
        self.value = True
        await interaction.response.defer()
        main = await Alliance.fetch(3683)
        offshore = await Alliance.fetch(HS_OFFSHORE_ID)
        resources = await main.fetch_bank()
        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)
        credentials = cache.get_credentials(251584)
        if credentials is None:
            return await interaction.followup.send(
                embed=funcs.get_embed_author_member(
                    interaction.user, "No credentials found"
                )
            )
        complete = await withdraw(
            credentials=credentials,
            resources=resources,
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

    @discord.ui.button(  # type: ignore
        custom_id=HS_NO_CUSTOM_ID,
        label="No",
        style=discord.ButtonStyle.red,
    )
    async def no(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        self.interaction = interaction
        self.value = False
        await interaction.edit_original_message(view=None)


class HouseStark(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.bank_send_task.start()
        self.bot.add_view(Confirm())
        self.star_melting_task.start()

    @commands.command(name="mmr", help="Check to see if a nation meets MMR.")
    async def mmr(self, ctx: RiftContext, *, nation: Nation = MISSING):
        nation = nation or await Nation.convert(ctx, nation)
        author_nation = await Nation.convert(ctx, None)
        if nation.alliance_id not in {3683, 8139, HS_OFFSHORE_ID}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Stockpiles doesn't apply to that nation!",
                    color=discord.Color.red(),
                )
            )
            return
        if author_nation.alliance_id not in {3683, 8139, HS_OFFSHORE_ID}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have permission to use that command!!",
                    color=discord.Color.red(),
                )
            )
            return
        mmr = {
            "soldiers": HS_SOLDIER_MMR * 3000 * nation.cities,
            "tanks": HS_TANK_MMR * 250 * nation.cities,
            "aircraft": HS_AIRCRAFT_MMR * 15 * nation.cities,
            "ships": HS_SHIP_MMR * 5 * nation.cities,
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
    async def stockpile(self, ctx: RiftContext, *, nation: Nation = MISSING):
        nation = nation or await Nation.convert(ctx, nation)
        user = nation.user
        data = await pnwkit.async_nation_query(
            {"id": nation.id, "first": 1},
            "money",
            "food",
            "uranium",
            "steel",
            "aluminum",
            "gasoline",
            "munitions",
        )
        nat = sum(
            (
                i.resources
                for i in cache.accounts
                if i.alliance_id == 3683
                and i.war_chest
                and i.owner_id == (user and user.id)
            ),
            Resources.from_dict(
                {
                    "money": getattr(data[0], "money", 0),
                    "food": getattr(data[0], "food", 0),
                    "coal": getattr(data[0], "coal", 0),
                    "oil": getattr(data[0], "oil", 0),
                    "uranium": getattr(data[0], "uranium", 0),
                    "lead": getattr(data[0], "lead", 0),
                    "iron": getattr(data[0], "iron", 0),
                    "bauxite": getattr(data[0], "bauxite", 0),
                    "gasoline": getattr(data[0], "gasoline", 0),
                    "munitions": getattr(data[0], "munitions", 0),
                    "steel": getattr(data[0], "steel", 0),
                    "aluminum": getattr(data[0], "aluminum", 0),
                }
            ),
        )
        author_nation = await Nation.convert(ctx, None)
        if nation.alliance_id not in {3683, 8139, HS_OFFSHORE_ID}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Stockpiles doesn't apply to that nation!",
                    color=discord.Color.red(),
                )
            )
            return
        if author_nation.alliance_id not in {3683, 8139, HS_OFFSHORE_ID}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have permission to use that command!!",
                    color=discord.Color.red(),
                )
            )
            return
        stockpile = {
            "money": HS_MONEY_REQ * nation.cities,
            "food": HS_FOOD_REQ_START + (HS_FOOD_REQ * nation.cities),
            "uranium": HS_URANIUM_REQ * nation.cities,
            "steel": HS_STEEL_REQ * nation.cities,
            "aluminum": HS_ALUMINUM_REQ * nation.cities,
            "gasoline": HS_GASOLINE_REQ * nation.cities,
            "munitions": HS_MUNITIONS_REQ * nation.cities,
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
        prices = cache.prices
        amounts: List[str] = []
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
        amounts_str = "\n".join(amounts)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{nation} doesn't meet stockpiles!\n\n{amounts_str}\n\n**Total:** ${cost:,.2f}",
                color=discord.Color.orange(),
            )
        )

    @tasks.loop(hours=24)
    async def bank_send_task(self):
        channel = self.bot.get_channel(239099900174925824)
        if not channel:
            return
        try:
            offshore = await Alliance.fetch(HS_OFFSHORE_ID)
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
        print(f"Waiting until {wait} to send bank!", flush=True)
        await self.bot.update_pnw_session()
        await discord.utils.sleep_until(wait)

    @tasks.loop(hours=24)
    async def star_melting_task(self):
        nation = cache.get_nation(226169)
        if nation is not None:
            await nation.send_message(
                subject="The walls are melting", content="The walls are melting"
            )

    @star_melting_task.before_loop
    async def before_star_melting_task(self):
        await self.bot.wait_until_ready()
        now = discord.utils.utcnow()
        wait = now.replace(hour=9, minute=0, second=0)
        while wait < now:
            wait += datetime.timedelta(days=1)
        await self.bot.update_pnw_session()
        await discord.utils.sleep_until(wait)

    @commands.command(
        name="bank-sheet",
        aliases=[
            "bsheet",
            "banksheet",
            "deposits-sheet",
            "dsheet",
            "deposit-sheet",
            "depositssheet",
            "depositsheet",
        ],
        help="Update the deposits sheet.",
    )
    async def bank_sheet(self, ctx: RiftContext):
        alliance = cache.get_alliance(3683)
        if alliance is None:
            return
        permissions = alliance.permissions_for(ctx.author)
        if not (
            permissions.leadership
            or permissions.manage_bank_accounts
            or permissions.view_bank_accounts
        ):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have permission to use that command!!",
                    color=discord.Color.red(),
                )
            )
        accounts = [i for i in cache.accounts if i.alliance_id == 3683]
        users = {i.owner_id for i in accounts}
        links = {
            i.user_id: n
            for i in cache.users
            if i.user_id in users and (n := cache.get_nation(i.nation_id)) is not None
        }
        deposits: List[List[Any]] = []
        for user in users:
            nation = links.get(user)
            accounts_ = [i for i in accounts if i.owner_id == user]
            resources = sum((i.resources for i in accounts_), Resources())
            deposits.append(
                [
                    nation and nation.id,
                    nation and nation.name,
                    nation and nation.leader,
                    user,
                    1,
                    "",
                    len(accounts_),
                    resources.money,
                    resources.food,
                    resources.coal,
                    resources.oil,
                    resources.uranium,
                    resources.lead,
                    resources.iron,
                    resources.bauxite,
                    resources.gasoline,
                    resources.munitions,
                    resources.steel,
                    resources.aluminum,
                ]
            )
        write_deposits(deposits)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "Deposits sheet updated!",
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift) -> None:
    bot.add_cog(HouseStark(bot))


# this code is almost entirely from the sample code provided by Google
# i'm lazy
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_RANGE_NAME = "Deposits!A2:E"


def write_deposits(deposits: Any) -> None:
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)  # type: ignore
    if not creds or not creds.valid:  # type: ignore
        if creds and creds.expired and creds.refresh_token:  # type: ignore
            creds.refresh(Request())  # type: ignore
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)  # type: ignore
            creds = flow.run_local_server(port=0)  # type: ignore
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())  # type: ignore

    service = build("sheets", "v4", credentials=creds)  # type: ignore

    body = {"values": deposits}
    sheet = service.spreadsheets()  # type: ignore
    (
        sheet.values()  # type: ignore
        .update(
            spreadsheetId=HS_SPREADSHEET_ID,
            range="Deposits!A2:S",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )