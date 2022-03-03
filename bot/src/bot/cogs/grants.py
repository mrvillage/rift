from __future__ import annotations

import datetime
from typing import Literal, Union

import discord
import pnwkit
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...data.classes import (
    Alliance,
    AllianceSettings,
    Grant,
    Nation,
    Resources,
    Transaction,
)
from ...enums import (
    AccountType,
    GrantPayoff,
    GrantStatus,
    TransactionStatus,
    TransactionType,
)
from ...errors import EmbedErrorMessage, NoRolesError
from ...ref import Rift, RiftContext
from ...views import PayConfirm


class Grants(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="grant",
        brief="A group of commands related to grants.",
        type=commands.CommandType.chat_input,
    )
    async def grant(self, ctx: RiftContext):
        ...

    @grant.command(  # type: ignore
        name="send", brief="Send a grant.", type=commands.CommandType.chat_input
    )
    async def grant_send(
        self,
        ctx: RiftContext,
        recipient: Union[discord.Member, discord.User],
        resources: Resources,
        payoff: Literal["NONE", "DEPOSIT"],
        note: str = MISSING,
        deadline: str = MISSING,
        alliance: Alliance = MISSING,
        request: bool = True,
    ):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        time = datetime.datetime.now(tz=datetime.timezone.utc)
        if deadline is not MISSING:
            try:
                deadline_datetime = datetime.datetime.fromtimestamp(
                    time.timestamp() + funcs.utils.parse_time_to_seconds(deadline)
                )
            except ValueError:
                raise EmbedErrorMessage(ctx.author, "Invalid time format.")
        else:
            deadline_datetime = None
        permissions = alliance.permissions_for(ctx.author)
        if not (permissions.leadership or permissions.manage_grants):
            raise NoRolesError(alliance, "Manage Grants")
        payoff_ = getattr(GrantPayoff, payoff)
        if payoff_ is not GrantPayoff.NONE:
            request = True
        grant = await Grant.create(
            recipient,
            time,
            resources,
            alliance,
            payoff_,
            note or None,
            deadline_datetime,
            Resources(),
            GrantStatus.PENDING,
        )
        await grant.send(ctx.author, request)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Sent a grant with ID {grant.id} from alliance {alliance} to <@{recipient.id}> for {resources} with a payoff method of `{payoff}` and {'no deadline' if deadline_datetime is None else f'is due <t:{int(deadline_datetime.timestamp())}:R>'} and {f'a note of {note}' if note else 'no note'}.\nGrant ID: {grant.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @grant.command(  # type: ignore
        name="accept", brief="Accept a grant.", type=commands.CommandType.chat_input
    )
    async def grant_accept(
        self, ctx: RiftContext, grant: Grant, nation: Nation = MISSING
    ):
        nation = nation or await Nation.convert(ctx, nation)
        if grant.recipient_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author, "You are not the recipient of this grant."
            )
        if grant.status is not GrantStatus.PENDING:
            raise EmbedErrorMessage(ctx.author, "This grant is not pending.")
        await grant.save()
        transaction = await Transaction.create(
            datetime.datetime.now(tz=datetime.timezone.utc),
            TransactionStatus.PENDING,
            TransactionType.GRANT_WITHDRAW,
            ctx.author,
            nation,
            grant,
            grant.resources,
            grant.note,
            to_type=AccountType.NATION,
            from_type=AccountType.GRANT,
        )
        await transaction.send_for_approval()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Grant {grant.id} has been sent to have the resources transferred.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @grant.command(  # type: ignore
        name="reject", brief="Reject a grant.", type=commands.CommandType.chat_input
    )
    async def grant_decline(self, ctx: RiftContext, grant: Grant):
        if grant.recipient_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author, "You are not the recipient of this grant."
            )
        if grant.status is not GrantStatus.PENDING:
            raise EmbedErrorMessage(ctx.author, "This grant is not pending.")
        grant.status = GrantStatus.REJECTED
        await grant.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Grant {grant.id} has been rejected.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @grant.command(  # type: ignore
        name="cancel", brief="Cancel a grant.", type=commands.CommandType.chat_input
    )
    async def grant_cancel(self, ctx: RiftContext, grant: Grant):
        alliance = grant.alliance
        if alliance is None:
            raise EmbedErrorMessage(
                ctx.author, "The alliance that grant belongs to no longer exists!"
            )
        permissions = Alliance.permissions_for_id(grant.alliance_id, ctx.author)
        if not (permissions.leadership or permissions.manage_grants):
            raise NoRolesError(alliance, "Manage Grants")
        if grant.status is not GrantStatus.PENDING:
            raise EmbedErrorMessage(ctx.author, "This grant is not pending.")
        grant.status = GrantStatus.CANCELLED
        await grant.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Grant {grant.id} has been cancelled.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @grant.command(  # type: ignore
        name="info",
        brief="Get info about a grant.",
        type=commands.CommandType.chat_input,
    )
    async def grant_info(self, ctx: RiftContext, grant: Grant):
        permissions = Alliance.permissions_for_id(grant.alliance_id, ctx.author)
        if grant.recipient_id != ctx.author.id and not (
            permissions.leadership
            or permissions.view_grants
            or permissions.manage_grants
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You don't have permission to view information on this grant.",
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"ID: {grant.id}\n"
                f"Recipient: <@{grant.recipient_id}>\n"
                f"Resources: {grant.resources or 'None'}\n"
                f"Payoff: `{grant.payoff.name}`\n"
                f"Deadline: {'None' if grant.deadline is None else f'<t:{int(grant.deadline.timestamp())}:f>'}\n"
                f"Note: {grant.note}\n"
                f"Status: `{grant.status.name}`"
                + (
                    f"\nPaid: {grant.paid or 'None'}\nCode: {grant.code}"
                    if grant.payoff is GrantPayoff.DEPOSIT
                    else ""
                ),
                color=discord.Color.green(),
            ),
        )

    @grant.command(  # type: ignore
        name="list",
        brief="List all grants.",
        type=commands.CommandType.chat_input,
    )
    async def grant_list(self, ctx: RiftContext, alliance: Alliance = MISSING):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        permissions = alliance.permissions_for(ctx.author)
        if not (
            permissions.leadership
            or permissions.view_grants
            or permissions.manage_grants
        ):
            raise NoRolesError(alliance, "View Grants")
        grants = [i for i in cache.grants if i.alliance_id == alliance.id]
        if not grants:
            raise EmbedErrorMessage(
                ctx.author, "There are no grants for this alliance."
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Grants for {alliance}:\n\n"
                + "\n".join(
                    f"#{i.id} to <@{i.recipient_id}>"
                    for i in sorted(grants, key=lambda x: x.id, reverse=True)
                ),
                color=discord.Color.blue(),
            )
        )

    @grant.command(  # type: ignore
        name="edit",
        brief="Edit a grant.",
        type=commands.CommandType.chat_input,
    )
    async def grant_edit(
        self,
        ctx: RiftContext,
        grant: Grant,
        paid: Resources = MISSING,
        payoff: Literal["NONE", "DEPOSIT"] = MISSING,
        deadline: str = MISSING,
    ):
        alliance = grant.alliance
        if alliance is None:
            raise EmbedErrorMessage(
                ctx.author, "The alliance that grant belongs to no longer exists!"
            )
        permissions = alliance.permissions_for_id(grant.alliance_id, ctx.author)
        if not (permissions.leadership or permissions.manage_grants):
            raise NoRolesError(alliance, "Manage Grants")
        if grant.status is not GrantStatus.PENDING:
            raise EmbedErrorMessage(ctx.author, "This grant is not pending.")
        if paid is not MISSING:
            grant.paid = paid
        if deadline is not MISSING:
            if deadline.lower() == "none":
                grant.deadline = None
            else:
                time = datetime.datetime.now(tz=datetime.timezone.utc)
                try:
                    deadline_datetime = datetime.datetime.fromtimestamp(
                        time.timestamp() + funcs.utils.parse_time_to_seconds(deadline)
                    )
                except ValueError:
                    raise EmbedErrorMessage(ctx.author, "Invalid time format.")
                grant.deadline = deadline_datetime
        if payoff is not MISSING:
            grant.payoff = getattr(GrantPayoff, payoff)
        await grant.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Grant {grant.id} now has {paid} paid off with payoff method `{grant.payoff.name}` and is {'never ' if grant.deadline is None else f'due at <t:{int(grant.deadline.timestamp())}:R>'}.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @grant.command(  # type: ignore
        name="pay",
        brief="Pay off a grant.",
        type=commands.CommandType.chat_input,
        descriptions={
            "grant": "The grant to pay off.",
            "resources": "The amount of resources to pay off.",
            "note": "A note to attach to the transaction.",
        },
    )
    async def grant_pay(
        self,
        ctx: RiftContext,
        resources: Resources,
        grant: Grant,
        note: str = MISSING,
    ):
        if grant.recipient_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can pay off your own grants!",
            )
        if not resources or resources < 0:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify an amount of resources to pay!",
            )
        nation = await Nation.convert(ctx, None)
        credentials = cache.get_credentials(nation.id)
        view = PayConfirm(grant, resources, credentials, note)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Are you sure you want to pay off {resources} of grant #{grant.id:,}?",
                color=discord.Color.orange(),
            ),
            view=view,
            ephemeral=True,
        )
        if await view.wait():
            await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Paying off {resources} of grant #{grant.id:,} timed out! Please try again.",
                    color=discord.Color.red(),
                ),
                view=None,
            )

    @grant.command(  # type: ignore
        name="pay-check",
        brief="Check for any new deposits in-game.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to check for new deposits to, defaults to your primary account.",
        },
    )
    async def grant_pay_check(
        self,
        ctx: RiftContext,
        grant: Grant,
    ):
        if grant.recipient_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can pay off your own grants!",
            )
        await ctx.interaction.response.defer(ephemeral=True)
        nation = await Nation.convert(ctx, None)
        data = await pnwkit.async_nation_query(
            {"id": nation.id, "first": 1},
            {
                "sent_bankrecs": [
                    "id",
                    "sid",
                    "stype",
                    "rid",
                    "rtype",
                    "note",
                    "money",
                    "coal",
                    "oil",
                    "uranium",
                    "iron",
                    "bauxite",
                    "lead",
                    "gasoline",
                    "munitions",
                    "steel",
                    "aluminum",
                    "food",
                ]
            },
        )
        if not data:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "I could not retrieve bank information!",
                    color=discord.Color.red(),
                ),
            )
        data = data[0]
        if not data["sent_bankrecs"]:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "No new deposits found!",
                    color=discord.Color.green(),
                ),
            )
        alliance_settings = await AllianceSettings.fetch(grant.alliance_id)
        if alliance_settings.offshore_id is not None:
            offshore_id = alliance_settings.offshore_id
        else:
            offshore_id = -1
        try:
            deposit = next(
                i
                for i in data["sent_bankrecs"]
                if int(i["rid"]) in {grant.alliance_id, offshore_id}
                and i["note"].strip() == grant.code
            )
        except StopIteration:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "No new deposits found!",
                    color=discord.Color.green(),
                ),
            )
        resources = Resources.from_dict(deposit)
        transaction = await Transaction.create(
            datetime.datetime.now(tz=datetime.timezone.utc),
            TransactionStatus.ACCEPTED,
            TransactionType.GRANT_DEPOSIT,
            ctx.author,
            grant,
            nation,
            resources,
            None,
            to_type=AccountType.GRANT,
            from_type=AccountType.NATION,
        )
        grant.paid += resources
        grant.regenerate_code()
        await grant.save()
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Payment of {resources} towards grant #{grant.id:,} recorded successfully!. The transaction ID is {transaction.id:,}.",
                color=discord.Color.green(),
            ),
        )

    @grant.command(  # type: ignore
        name="summary",
        brief="Get a summary of a user's grants.",
        type=commands.CommandType.chat_input,
        descriptions={
            "user": "The user to get the summary of.",
            "alliance": "The alliance to get the summary in.",
        },
    )
    async def grant_summary(
        self,
        ctx: RiftContext,
        user: Union[discord.User, discord.Member] = MISSING,
        alliance: Alliance = MISSING,
    ):
        user = user or ctx.author
        alliance = alliance or await Alliance.convert(ctx, None)
        permissions = alliance.permissions_for(ctx.author)
        if (
            not (
                permissions.leadership
                or permissions.view_grants
                or permissions.manage_grants
            )
            and ctx.author.id != user.id
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have permission to view grants!",
            )
        grants = [
            i
            for i in cache.grants
            if i.alliance_id == alliance.id and i.recipient_id == user.id
        ]
        if not grants:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "That user has no active grants!",
                    color=discord.Color.red(),
                ),
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Grant summary for <@{user.id}>:\n\nPending payment: {sum((i.resources - i.paid for i in grants if i.payoff is GrantPayoff.DEPOSIT), Resources()) or 'None'}\n\nGrants taken:\n"
                + "\n".join(
                    f"#{i.id}" for i in sorted(grants, key=lambda x: x.id, reverse=True)
                ),
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Grants(bot))
