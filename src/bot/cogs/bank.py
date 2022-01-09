from __future__ import annotations

import datetime
from typing import Literal, Optional, Union

import discord
import pnwkit
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...data.classes import (
    Account,
    Alliance,
    AllianceSettings,
    Nation,
    Resources,
    Transaction,
    TransactionRequest,
)
from ...enums import AccountType, TransactionStatus, TransactionType
from ...errors import EmbedErrorMessage, NoCredentialsError, NoRolesError
from ...ref import Rift, RiftContext
from ...views import (
    Confirm,
    DepositConfirm,
    TransactionHistoryView,
    TransactionRequestView,
)


class Bank(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="bank",
        brief="A group of commands related to alliance banks.",
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    async def bank(self, ctx: RiftContext):
        ...

    @bank.command(  # type: ignore
        name="transfer",
        brief="Send money from an alliance bank.",
        type=commands.CommandType.chat_input,
        descriptions={
            "recipient": "The nation or alliance to send to.",
            "resources": "The resources to send.",
            "alliance": "The alliance to send money from, defaults to your alliance.",
        },
    )
    async def bank_transfer(
        self,
        ctx: RiftContext,
        recipient: str,
        resources: Resources,
        alliance: Alliance = MISSING,
        note: Optional[str] = None,
    ):
        recipient_ = await funcs.convert_nation_or_alliance(ctx, recipient)
        alliance_ = alliance or await Alliance.convert(ctx, None)
        if alliance_ is None:
            raise EmbedErrorMessage(
                ctx.author,
                "You're not in an alliance and didn't specify one to send from! Please try again with an alliance.",
            )
        if not len(resources):
            raise EmbedErrorMessage(
                ctx.author, "You didn't specify any resources to send!"
            )
        if resources < 0:
            raise EmbedErrorMessage(
                ctx.author,
                "You can't send negative resources! Please try again with a positive amount.",
            )
        permissions = alliance.permissions_for(ctx.author)
        if not (permissions.leadership or permissions.send_alliance_bank):
            raise NoRolesError(alliance_, "Send Alliance Bank")
        view = Confirm(defer=True)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Are you sure you want to transfer {resources} to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}** from the alliance of **{repr(alliance_)}**",
                color=discord.Color.orange(),
            ),
            view=view,
            ephemeral=True,
        )
        r = await view.wait()
        if r:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You didn't confirm the transaction in time!",
                    color=discord.Color.red(),
                ),
                view=None,
            )
        if not view.value:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"You have cancelled the transfer of {resources} from **{repr(alliance_)}** to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}**.",
                    color=discord.Color.red(),
                ),
                view=None,
            )
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Sending {resources} from **{repr(alliance_)}** to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}**...",
                color=discord.Color.orange(),
            ),
            view=None,
        )
        credentials = funcs.credentials.find_highest_alliance_credentials(
            alliance_, "send_alliance_bank"
        )
        if credentials is None or (
            credentials.username is None and credentials.password is None
        ):
            raise NoCredentialsError()
        complete = await funcs.withdraw(
            resources,
            recipient_,
            credentials,
            note=f"Transfer by {ctx.author.name}#{ctx.author.discriminator} with note: {note}",
        )
        if not complete:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Something went wrong with the transaction. Please try again.",
                    color=discord.Color.red(),
                )
            )
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"You successfully transferred {resources} from **{repr(alliance_)}** to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}**.",
                color=discord.Color.green(),
            )
        )

    @bank.command(  # type: ignore
        name="balance",
        aliases=["bal"],
        brief="Check the balance of an alliance bank.",
        type=commands.CommandType.chat_input,
        descriptions={
            "alliance": "The alliance to check the balance of, defaults to your alliance.",
        },
    )
    async def bank_balance(self, ctx: RiftContext, *, alliance: Alliance = MISSING):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        permissions = alliance.permissions_for(ctx.author)
        if not (permissions.view_alliance_bank or permissions.leadership):
            raise NoRolesError(alliance, "View Alliance Bank")
        resources = await alliance.fetch_bank()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The **{repr(alliance)}** alliance bank has {resources}.",
                color=discord.Color.blue(),
            )
        )

    @bank.group(  # type: ignore
        name="account",
        brief="Manage your bank accounts.",
        type=commands.CommandType.chat_input,
    )
    async def bank_account(self, ctx: RiftContext):
        ...

    @bank_account.command(  # type: ignore
        name="create",
        brief="Create a bank account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "name": "The name of the account",
            "war_chest": "Whether or not the account's balance counts towards your war chest requirements",
            "alliance": "The alliance to register the account in, defaults to your alliance.",
            "primary": "Whether or not the account is your primary account.",
        },
    )
    async def bank_account_create(
        self,
        ctx: RiftContext,
        name: str,
        war_chest: bool = True,
        alliance: Alliance = MISSING,
        primary: bool = False,
    ):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        permissions = alliance.permissions_for(ctx.author)
        if not (
            permissions.create_bank_accounts
            or permissions.manage_bank_accounts
            or permissions.leadership
        ):
            raise EmbedErrorMessage(
                ctx.author,
                f"You don't have permission to create bank accounts in alliance {repr(alliance)}.",
            )
        if not accounts:
            primary = True
        elif primary:
            for i in accounts:
                if i.primary:
                    i.primary = False
                    await i.save()
                    break
        account = await Account.create(ctx.author, alliance, name, war_chest, primary)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"You have successfully created a {'primary ' if primary else ' '}bank account for **{repr(alliance)}** with ID **{account.id}**.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @bank_account.command(  # type: ignore
        name="delete",
        brief="Delete a bank account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to delete.",
        },
    )
    async def bank_account_delete(self, ctx: RiftContext, account: Account = MISSING):
        if account.owner_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can only delete your own accounts!",
            )
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        primary_account = next(i for i in accounts if i.primary)
        account = account or primary_account
        if account.primary and account.resources:
            raise EmbedErrorMessage(
                ctx.author,
                "You cannot delete your primary account while it has resources!",
            )
        primary_account.resources += account.resources
        await primary_account.save()
        await account.delete()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"You have successfully deleted the bank account with ID **{account.id}**. {account.resources or 'No'} resources have been transferred to your primary account.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @bank_account.command(  # type: ignore
        name="transfer",
        brief="Transfer resources from one bank account to another.",
        type=commands.CommandType.chat_input,
        descriptions={
            "from": "The bank account to transfer from, defaults to your primary account.",
            "to": "The bank account to transfer to.",
            "amount": "The amount of resources to transfer.",
            "note": "A note to attach to the transaction.",
        },
    )
    async def bank_account_transfer(
        self,
        ctx: RiftContext,
        to: Account,
        amount: Resources,
        from_: Account = MISSING,
        note: Optional[str] = None,
    ):
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        if not accounts:
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have any bank accounts!",
            )
        if not amount:
            raise EmbedErrorMessage(
                ctx.author,
                "You cannot transfer no resources!",
            )
        from_ = from_ or next(i for i in accounts if i.primary)
        if from_.id == to.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You cannot transfer resources to the same account!",
            )
        if from_.owner_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can only transfer from your own accounts!",
            )
        if any(
            value < getattr(amount, key)
            for key, value in from_.resources.to_dict().items()
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You cannot transfer more resources than you have!",
            )
        if to.owner_id == from_.owner_id:
            status = TransactionStatus.ACCEPTED
        else:
            status = TransactionStatus.PENDING
        transaction = await Transaction.create(
            datetime.datetime.utcnow(),
            status,
            TransactionType.TRANSFER,
            ctx.author,
            to,
            from_ or next(i for i in accounts if i.primary),
            amount,
            note=note,
        )
        await transaction.send_for_approval()
        if transaction.status is TransactionStatus.ACCEPTED:
            from_.resources -= amount
            to.resources += amount
            await from_.save()
            await to.save()
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"You have successfully transferred **{amount}** resources from **{from_.name}** to **{to.name}**.\n"
                    f"The transaction ID is **{transaction.id}**.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"You have successfully created a transfer request with ID **{transaction.id}**.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @bank_account.command(  # type: ignore
        name="info",
        brief="Get information about a bank account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to get information about.",
        },
    )
    async def bank_account_info(self, ctx: RiftContext, account: Account = MISSING):
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        if not accounts:
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have any bank accounts!",
            )
        account = account or next(i for i in accounts if i.primary)
        permissions = Alliance.permissions_for_id(account.alliance_id, ctx.author)
        if account.owner_id != ctx.author.id and not (
            permissions.leadership
            or permissions.view_bank_accounts
            or permissions.manage_bank_accounts
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You don't have permission to get information about that bank account!",
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"**{account.name}**\n"
                f"ID: {account.id}\n"
                f"Owner: <@{account.owner_id}>\n"
                f"Alliance: {repr(account.alliance)}\n"
                f"Resources: {account.resources or None}\n"
                f"Single Use Deposit Code:\n"
                f"{account.deposit_code}\n"
                f"Primary: {account.primary}\n"
                f"War Chest: {account.war_chest}",
                color=discord.Color.blue(),
            )
        )

    @bank_account.command(  # type: ignore
        name="list",
        brief="List all of your bank accounts.",
        type=commands.CommandType.chat_input,
        descriptions={
            "user": "The user to list the accounts of, defaults to you.",
            "alliance": "The alliance to list the accounts of, defaults to your alliance.",
        },
    )
    async def bank_account_list(
        self,
        ctx: RiftContext,
        user: Union[discord.Member, discord.User] = MISSING,
        alliance: Alliance = MISSING,
    ):
        if user is MISSING:
            user = ctx.author
            accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        else:
            link = cache.get_user(ctx.author.id)
            nation = cache.get_nation(link.nation_id) if link is not None else None
            alliance_position = nation.alliance_position if nation is not None else 0
            roles = [
                i
                for i in cache.roles
                if (
                    ctx.author.id in i.member_ids
                    or alliance_position in i.alliance_positions
                )
                and (
                    i.permissions.leadership
                    or i.permissions.view_bank_accounts
                    or i.permissions.manage_bank_accounts
                )
            ]
            accounts = [
                i
                for i in cache.accounts
                if i.owner_id == user.id
                and (
                    i.owner_id == ctx.author.id
                    or [r for r in roles if i.alliance_id == r.alliance_id]
                )
            ]
        if alliance is not MISSING:
            accounts = [i for i in accounts if i.alliance_id == alliance.id]
        if not accounts:
            raise EmbedErrorMessage(
                ctx.author,
                "No bank accounts found!",
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"**{user.mention}'s Bank Accounts**\n"
                + "\n".join(
                    f"**{i.id} - {i.name} - {i.alliance_id}**: {i.resources or None}"
                    for i in accounts
                ),
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @bank_account.command(  # type: ignore
        name="edit",
        brief="Edit a bank account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to edit.",
            "name": "The new name of the account.",
            "war_chest": "Whether or not the account's balance counts towards your war chest requirements.",
            "primary": "Whether or not the account is your primary account.",
            "resources": "The new amount of resources in the account.",
        },
    )
    async def bank_account_edit(
        self,
        ctx: RiftContext,
        account: Account,
        name: str = MISSING,
        war_chest: bool = MISSING,
        primary: bool = MISSING,
        resources: Resources = MISSING,
    ):
        if (
            name is MISSING
            and war_chest is MISSING
            and primary is MISSING
            and resources is MISSING
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify at least one field to edit!",
            )
        permissions = Alliance.permissions_for_id(account.alliance_id, ctx.author)
        if ctx.author.id != account.owner_id and not (
            permissions.leadership or permissions.manage_bank_accounts
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You don't have permission to edit that account!",
            )
        if name is not MISSING:
            account.name = name
        if war_chest is not MISSING:
            account.war_chest = war_chest
        if primary is not MISSING:
            if not primary:
                raise EmbedErrorMessage(
                    ctx.author,
                    "You can't unset your primary account!",
                )
            account.primary = primary
            accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
            for i in accounts:
                if i.primary:
                    i.primary = False
                    await i.save()
        if resources is not MISSING:
            if not permissions.manage_bank_accounts:
                raise EmbedErrorMessage(
                    ctx.author,
                    "You do not have permission to edit resources on this account!",
                )
            account.resources = resources
        await account.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"You have successfully edited **{account.id} - {account.name}**.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @bank_account.command(  # type: ignore
        name="deposit",
        brief="Deposit resources into a bank account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to deposit into, defaults to your primary account.",
            "resources": "The amount of resources to deposit.",
            "note": "A note to attach to the transaction.",
        },
    )
    async def bank_account_deposit(
        self,
        ctx: RiftContext,
        resources: Resources,
        account: Account = MISSING,
        note: str = MISSING,
    ):
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        if not accounts:
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have any bank accounts!",
            )
        account = account or next(i for i in accounts if i.primary)
        if account.owner_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can only deposit into your own accounts!",
            )
        if not resources or any(i < 0 for i in resources):
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify an amount of resources to deposit!",
            )
        nation = await Nation.convert(ctx, None)
        credentials = cache.get_credentials(nation.id)
        view = DepositConfirm(account, resources, credentials, note)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Are you sure you want to deposit {resources} into account #{account.id:,}?",
                color=discord.Color.orange(),
            ),
            view=view,
            ephemeral=True,
        )
        if await view.wait():
            await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Deposit of {resources} into account #{account.id:,} timed out! Please try again.",
                    color=discord.Color.red(),
                ),
                view=None,
            )

    @bank_account.command(  # type: ignore
        name="deposit-check",
        brief="Check for any new deposits in-game.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to check for new deposits to, defaults to your primary account.",
        },
    )
    async def bank_account_deposit_check(
        self,
        ctx: RiftContext,
        account: Account = MISSING,
    ):
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        if not accounts:
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have any bank accounts!",
            )
        account = account or next(i for i in accounts if i.primary)
        if account.owner_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can only check deposits for your own accounts!",
            )
        await ctx.interaction.response.defer(ephemeral=True)
        nation = await Nation.convert(ctx, None)
        data = await pnwkit.async_nation_query(
            {"id": nation.id},
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
        alliance_settings = await AllianceSettings.fetch(account.alliance_id)
        if alliance_settings.offshore_id is not None:
            offshore_id = alliance_settings.offshore_id
        else:
            offshore_id = -1
        try:
            deposit = next(
                i
                for i in data["sent_bankrecs"]
                if int(i["rid"]) in {account.alliance_id, offshore_id}
                and i["note"].strip() == account.deposit_code
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
            datetime.datetime.utcnow(),
            TransactionStatus.ACCEPTED,
            TransactionType.DEPOSIT,
            ctx.author,
            account,
            nation,
            resources,
            None,
            from_type=AccountType.NATION,
        )
        account.resources += resources
        account.regenerate_deposit_code()
        await account.save()
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Deposit of {resources} into account #{account.id:,} recorded successfully!. The transaction ID is {transaction.id:,}.",
                color=discord.Color.green(),
            ),
        )

    @bank_account.command(  # type: ignore
        name="withdraw",
        brief="Withdraw resources from a bank account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to withdraw from, defaults to your primary account.",
            "resources": "The amount of resources to withdraw.",
            "nation": "The nation to withdraw the resources to.",
            "note": "A note to attach to the transaction.",
        },
    )
    async def bank_account_withdraw(
        self,
        ctx: RiftContext,
        resources: Resources,
        account: Account = MISSING,
        nation: Nation = MISSING,
        note: str = MISSING,
    ):  # sourcery no-metrics
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        if not accounts:
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have any bank accounts!",
            )
        account = account or next(i for i in accounts if i.primary)
        if account.owner_id != ctx.author.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can only deposit into your own accounts!",
            )
        if not resources or resources < 0:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify an amount of resources to deposit!",
            )
        if any(
            value > getattr(account.resources, key)
            for key, value in resources.to_dict().items()
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have enough resources in your account!",
            )
        if account.alliance is None:
            raise EmbedErrorMessage(
                ctx.author,
                "The alliance associated with that account no longer exists!",
            )
        nation = nation or await Nation.convert(ctx, None)
        settings = await AllianceSettings.fetch(nation.alliance_id)
        if not settings.require_withdraw_approval:
            await ctx.interaction.response.defer(ephemeral=True)
            alliance_settings = await AllianceSettings.fetch(account.alliance_id)
            offshore = alliance_settings.offshore
            if offshore is not None and alliance_settings.withdraw_from_offshore:
                credentials = funcs.credentials.find_highest_alliance_credentials(
                    offshore, "send_alliance_bank"
                )
                if credentials is not None:
                    success = await funcs.withdraw(
                        resources,
                        nation,
                        credentials,
                        note=f"Rift Withdrawal from Account #{account.id} and note: {note}",
                    )
                else:
                    success = False
            else:
                success = False
            if not success:
                credentials = funcs.credentials.find_highest_alliance_credentials(
                    account.alliance, "send_alliance_bank"
                )
                if credentials is None:
                    raise NoCredentialsError(account.alliance)
                success = await funcs.withdraw(
                    resources,
                    nation,
                    credentials,
                    note=f"Rift Withdrawal from Account #{account.id} and note: {note}",
                )
            if success:
                transaction = await Transaction.create(
                    datetime.datetime.utcnow(),
                    TransactionStatus.ACCEPTED,
                    TransactionType.WITHDRAW,
                    ctx.author,
                    nation,
                    account,
                    resources,
                    note or None,
                    to_type=AccountType.NATION,
                )
                account.resources -= resources
                await account.save()
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        f"Withdrawal of {resources} from account #{account.id:,} recorded successfully!. The transaction ID is {transaction.id:,}.",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
        transaction = await Transaction.create(
            datetime.datetime.utcnow(),
            TransactionStatus.PENDING,
            TransactionType.WITHDRAW,
            ctx.author,
            nation,
            account,
            resources,
            note or None,
            to_type=AccountType.NATION,
        )
        await transaction.send_for_approval()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Withdrawal of {resources} from account #{account.id:,} requested successfully!. The transaction ID is {transaction.id:,}.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @bank_account.command(  # type: ignore
        name="history",
        brief="Check the transaction history of a bank account.",
        type=commands.CommandType.chat_input,
        descriptions={
            "account": "The bank account to check the history of, defaults to your primary account.",
            "page": "The page of the history to view.",
            "status": "The status of transactions to view, defaults to all.",
        },
    )
    async def bank_account_history(
        self,
        ctx: RiftContext,
        account: Account = MISSING,
        page: int = 1,
        status: Literal["PENDING", "ACCEPTED", "REJECTED", "CANCELLED"] = MISSING,
    ):
        accounts = [i for i in cache.accounts if i.owner_id == ctx.author.id]
        if not accounts:
            raise EmbedErrorMessage(
                ctx.author,
                "You do not have any bank accounts!",
            )
        account = account or next(i for i in accounts if i.primary)
        permissions = Alliance.permissions_for_id(account.alliance_id, ctx.author)
        if account.owner_id != ctx.author.id and not (
            permissions.leadership or permissions.manage_bank_accounts
        ):
            raise EmbedErrorMessage(
                ctx.author,
                "You don't have permission to view the transaction history of that account!",
            )
        transactions = [
            i
            for i in cache.transactions
            if (i.to_id == account.id and i.to_type is AccountType.ACCOUNT)
            or (i.from_id == account.id and i.from_type is AccountType.ACCOUNT)
        ]
        if status is not MISSING:
            status = getattr(TransactionStatus, status)
            transactions = [i for i in transactions if i.status is status]
        if not transactions:
            raise EmbedErrorMessage(
                ctx.author,
                "There are no transactions for that account!",
            )
        transactions.sort(key=lambda x: x.id, reverse=True)
        view = TransactionHistoryView(
            ctx.author,
            transactions,
            f"Showing transactions for account #{account.id:,} owned by <@{account.owner_id}>.\n"
            f"{len(transactions)} transactions found.\n"
            "Page **{page}** of **{pages}**.",
            page,
        )
        await ctx.reply(embed=view.get_embed(ctx.author), view=view)
        if await view.wait():
            await ctx.interaction.edit_original_message(view=None)

    @bank.group(  # type: ignore
        name="transaction",
        brief="Manage transactions.",
        type=commands.CommandType.chat_input,
    )
    async def bank_transaction(self, ctx: RiftContext):
        ...

    @bank_transaction.command(  # type: ignore
        name="review",
        brief="Review a pending transaction.",
        type=commands.CommandType.chat_input,
        descriptions={
            "transaction": "The pending transaction to review.",
        },
    )
    async def bank_account_review(
        self, ctx: RiftContext, transaction: Transaction
    ):  # sourcery no-metrics
        if transaction.status is not TransactionStatus.PENDING:
            raise EmbedErrorMessage(
                ctx.author,
                "That transaction is not pending!",
            )
        if transaction.type is TransactionType.WITHDRAW:
            if transaction.from_ is None:
                raise EmbedErrorMessage(
                    ctx.author,
                    "One account involved in that transaction does not exist!",
                )
            permissions = Alliance.permissions_for_id(
                transaction.from_.alliance_id, ctx.author
            )
            if not (permissions.leadership or permissions.manage_bank_accounts):
                raise EmbedErrorMessage(
                    ctx.author,
                    "You don't have permission to review that transaction!",
                )
        elif transaction.type is TransactionType.TRANSFER:
            if transaction.to is None:
                raise EmbedErrorMessage(
                    ctx.author,
                    "One account involved that transaction does not exist!",
                )
            if transaction.to.owner_id != ctx.author.id:
                raise EmbedErrorMessage(
                    ctx.author,
                    "You don't have permission to review that transaction!",
                )
        elif transaction.type is TransactionType.DEPOSIT:
            raise EmbedErrorMessage(
                ctx.author,
                "You can't review a deposit!",
            )
        elif transaction.type is TransactionType.GRANT:
            if transaction.from_ is None:
                raise EmbedErrorMessage(
                    ctx.author,
                    "One account involved in that transaction does not exist!",
                )
            permissions = Alliance.permissions_for_id(
                transaction.from_.alliance_id, ctx.author
            )
            if not (
                permissions.leadership
                or permissions.manage_grants
                or permissions.approve_grants
            ):
                raise EmbedErrorMessage(
                    ctx.author,
                    "You don't have permission to review that transaction!",
                )
        request = await TransactionRequest.create(transaction, ctx.author)
        view = TransactionRequestView(request, ctx.author.id, 60)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Reviewing transaction #{transaction.id:,}\n\n"
                + transaction.field["value"]
                + "\n\nYou have 60 seconds to review before this review times out.",
                color=discord.Color.orange(),
            ),
            view=view,
            ephemeral=True,
        )
        if await view.wait():
            await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Review of transaction #{transaction.id:,} timed out.",
                    color=discord.Color.red(),
                ),
                view=None,
            )


def setup(bot: Rift):
    bot.add_cog(Bank(bot))
