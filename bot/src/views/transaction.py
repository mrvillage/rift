from __future__ import annotations

import datetime
import urllib.parse
from typing import TYPE_CHECKING

import discord

from .. import funcs
from ..cache import cache
from ..data.classes import Alliance, AllianceSettings, Transaction
from ..enums import AccountType, GrantStatus, TransactionStatus, TransactionType

__all__ = (
    "TransactionRequestView",
    "DepositConfirm",
    "TransactionHistoryView",
    "PayConfirm",
)

if TYPE_CHECKING:
    from typing import List, Optional, Union

    from _typings import Field

    from ..data.classes import (
        Account,
        Credentials,
        Grant,
        Resources,
        Transaction,
        TransactionRequest,
    )


class TransactionRequestView(discord.ui.View):
    def __init__(
        self,
        request: TransactionRequest,
        user_id: int,
        timeout: Optional[float] = None,
    ) -> None:
        super().__init__(timeout=timeout)
        self.request: TransactionRequest = request
        transaction = self.request.transaction
        if transaction is None:
            return
        self.user_id: int = user_id
        end = 100 if user_id == 0 else 90
        self.add_item(TransactionRequestAcceptButton(transaction, custom_id=request.accept_custom_id[:end]))  # type: ignore
        if (
            transaction.type is TransactionType.WITHDRAW
            or transaction.type is TransactionType.GRANT_WITHDRAW
        ):
            self.add_item(TransactionRequestManualAcceptButton(transaction, request.accept_custom_id[: end - 1]))  # type: ignore
        self.add_item(TransactionRequestRejectButton(transaction, custom_id=request.reject_custom_id[:end]))  # type: ignore
        if transaction.to is not None and user_id == transaction.to.owner_id:
            self.add_item(  # type: ignore
                TransactionRequestCancelButton(
                    transaction, custom_id=request.cancel_custom_id
                )
            )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if TYPE_CHECKING:
            assert interaction.user is not None
        if self.user_id == 0:
            if self.request.transaction is None:
                await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "No transaction found.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
                return False
            if (
                self.request.transaction.type is TransactionType.WITHDRAW
                or self.request.transaction.type is TransactionType.TRANSFER
            ):
                if self.request.transaction.from_ is None:
                    await interaction.response.send_message(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "No transaction found.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                    return False
                alliance_id = self.request.transaction.from_.alliance_id
                permissions = Alliance.permissions_for_id(alliance_id, interaction.user)
                if permissions.leadership or permissions.manage_bank_accounts:
                    return True
                await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "You do not have permission to use this menu.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
                return False
            elif self.request.transaction.type is TransactionType.GRANT_WITHDRAW:
                if self.request.transaction.from_grant is None:
                    await interaction.response.send_message(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "No grant found.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                    return False
                alliance_id = self.request.transaction.from_grant.alliance_id
                permissions = Alliance.permissions_for_id(alliance_id, interaction.user)
                if (
                    permissions.leadership
                    or permissions.manage_grants
                    or permissions.approve_grants
                ):
                    return True
                await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "You do not have permission to use this menu.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
                return False
        if interaction.user.id == self.user_id:
            return True
        await interaction.response.send_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                "You're not allowed to use this menu!",
                color=discord.Color.red(),
            ),
            ephemeral=True,
        )
        return False


class TransactionRequestAcceptButton(discord.ui.Button[TransactionRequestView]):
    def __init__(self, transaction: Transaction, custom_id: str):
        super().__init__(
            custom_id=custom_id,
            style=discord.ButtonStyle.green,
            label="Accept"
            if transaction.type is not TransactionType.WITHDRAW
            and transaction.type is not TransactionType.GRANT_WITHDRAW
            else "Automatic Transfer",
        )
        self.transaction: Transaction = transaction

    async def callback(self, interaction: discord.Interaction) -> None:
        # sourcery no-metrics
        if TYPE_CHECKING:
            assert interaction.user is not None
        transaction = self.transaction
        try:
            if transaction.status is not TransactionStatus.PENDING:
                await interaction.response.edit_message(view=None)
                return await interaction.followup.send(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        f"Transaction {transaction.id} is no longer pending!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            transaction.status = TransactionStatus.ACCEPTED
            if transaction.type is TransactionType.TRANSFER:
                if transaction.to is None or transaction.from_ is None:
                    transaction.status = TransactionStatus.FAILED
                    return await interaction.response.send_message(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "One account involved in this transaction no longer exists! Please try sending a new transaction again.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                if any(
                    value < transaction.resources[key]
                    for key, value in transaction.resources.to_dict().items()
                ):
                    transaction.status = TransactionStatus.FAILED
                    return await interaction.response.send_message(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "The sending account does not have enough resources to complete this transaction! Please try sending a new transaction again.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                transaction.to.resources += transaction.resources
                transaction.from_.resources -= transaction.resources
                await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        f"Transaction accepted! {transaction.resources} has been added to account #{transaction.to_id:,}.",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
            elif (
                transaction.type is TransactionType.WITHDRAW
                or transaction.type is TransactionType.GRANT_WITHDRAW
            ):
                if (
                    (
                        transaction.from_ is None
                        or transaction.to_nation is None
                        or transaction.from_.alliance is None
                    )
                    if transaction.type is TransactionType.WITHDRAW
                    else (
                        transaction.from_grant is None
                        or transaction.to_nation is None
                        or transaction.from_grant.alliance is None
                    )
                ):
                    transaction.status = TransactionStatus.FAILED
                    return await interaction.response.send_message(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "One party involved in this transaction no longer exists! Please try sending a new transaction again.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                await interaction.response.defer(ephemeral=True)
                if TYPE_CHECKING:
                    assert transaction.from_ is not None
                    assert transaction.from_grant is not None
                    assert transaction.from_.alliance is not None
                    assert transaction.from_grant.alliance is not None
                if (
                    transaction.type is TransactionType.GRANT_WITHDRAW
                    and transaction.from_grant.status is not GrantStatus.PENDING
                ):
                    transaction.status = TransactionStatus.FAILED
                    return await interaction.response.send_message(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "This grant has already been completed!",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                if (
                    any(
                        value < getattr(transaction.resources, key)
                        for key, value in transaction.from_.resources.to_dict().items()
                    )
                    if transaction.type is TransactionType.WITHDRAW
                    else False
                ):
                    transaction.status = TransactionStatus.FAILED
                    await interaction.followup.send(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "The sending account does not have enough resources to complete this transaction! Please try sending a new transaction again.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                    owner = transaction.from_.owner
                    if owner is not None:
                        await owner.send(
                            embed=funcs.get_embed_author_member(
                                interaction.user,
                                f"Your {'grant ' if transaction.type is TransactionType.GRANT_WITHDRAW else ''}withdrawl request has failed. Transaction #{transaction.id}.",
                                color=discord.Color.red(),
                            )
                        )
                    return
                alliance_settings = await AllianceSettings.fetch(
                    transaction.from_.alliance_id
                    if transaction.type is TransactionType.WITHDRAW
                    else transaction.from_grant.alliance_id
                )
                offshore = alliance_settings.offshore
                if offshore is not None and alliance_settings.withdraw_from_offshore:
                    credentials = funcs.credentials.find_highest_alliance_credentials(
                        offshore, "send_alliance_bank"
                    )
                    if credentials is not None:
                        success = await funcs.withdraw(
                            transaction.resources,
                            transaction.to_nation,
                            credentials,
                            note=f"Rift Withdrawal from Account #{transaction.from_.id} and note: {transaction.note}"
                            if transaction.type is TransactionType.WITHDRAW
                            else f"Rift Grant #{transaction.from_grant.id} and note: {transaction.note}",
                        )
                    else:
                        success = False
                else:
                    success = False
                if not success:
                    credentials = funcs.credentials.find_highest_alliance_credentials(
                        transaction.from_.alliance
                        if transaction.type is TransactionType.WITHDRAW
                        else transaction.from_grant.alliance,
                        "send_alliance_bank",
                    )
                    if credentials is None:
                        transaction.status = TransactionStatus.PENDING
                        return await interaction.followup.send(
                            embed=funcs.get_embed_author_member(
                                interaction.user,
                                "I don't have any valid credentials to perform that action!",
                                color=discord.Color.red(),
                            ),
                            ephemeral=True,
                        )
                    success = await funcs.withdraw(
                        transaction.resources,
                        transaction.to_nation,
                        credentials,
                        note=f"Rift Withdrawal from Account #{transaction.from_.id} and note: {transaction.note}"
                        if transaction.type is TransactionType.WITHDRAW
                        else f"Rift Grant #{transaction.from_grant.id} and note: {transaction.note}",
                    )
                if not success:
                    transaction.status = TransactionStatus.PENDING
                    return await interaction.followup.send(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "Automatic transfer failed!",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                transaction.from_.resources -= transaction.resources
                await transaction.from_.save()
                await interaction.edit_original_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        f"Withdrawal of {transaction.resources} from account #{transaction.from_.id:,} approved by {interaction.user.mention}!"
                        if transaction.type is TransactionType.WITHDRAW
                        else f"Grant #{transaction.from_grant.id} of {transaction.resources} approved by {interaction.user.mention}!",
                        color=discord.Color.green(),
                    ),
                    view=None,
                )
                owner = transaction.from_.owner
                if owner is not None:
                    await owner.send(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            f"Your {'grant ' if transaction.type is TransactionType.GRANT_WITHDRAW else ''}withdrawl request has been approved and the resources sent! Transaction #{transaction.id}.",
                            color=discord.Color.green(),
                        )
                    )
                if transaction.type is TransactionType.GRANT_WITHDRAW:
                    grant = transaction.from_grant
                    grant.status = GrantStatus.SENT
                    await grant.save()
            elif transaction.type is TransactionType.GRANT:
                grant = self.transaction.from_grant
                if grant is None:
                    return
                if grant.status is not GrantStatus.PENDING:
                    await interaction.response.edit_message(view=None)
                    return await interaction.followup.send(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "This grant not pending!",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                user = self.transaction.to_user
                if user is None:
                    return
                link = cache.get_user(grant.recipient_id)
                if link is None or (nation := cache.get_nation(link.nation_id)) is None:
                    transaction.status = TransactionStatus.PENDING
                    return await interaction.response.send_message(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            "You're not linked so I can't infer what nation to grant this to! Please link your nation with the `/link` command or use `/grant accept` to accept the grant for a specific nation.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                grant_transaction = await Transaction.create(
                    datetime.datetime.now(tz=datetime.timezone.utc),
                    TransactionStatus.PENDING,
                    TransactionType.GRANT_WITHDRAW,
                    user,
                    nation,
                    grant,
                    self.transaction.resources,
                    self.transaction.note,
                    to_type=AccountType.NATION,
                    from_type=AccountType.GRANT,
                )
                await grant_transaction.send_for_approval()
                await interaction.response.edit_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        f"Grant {grant.id} has been sent for final approval.",
                        color=discord.Color.green(),
                    ),
                    view=None,
                )
        finally:
            await transaction.save()


class TransactionRequestManualAcceptButton(discord.ui.Button[TransactionRequestView]):
    def __init__(self, transaction: Transaction, custom_id: str):
        super().__init__(
            custom_id=custom_id,
            style=discord.ButtonStyle.green,
            label="Manually Transfer",
        )
        self.transaction: Transaction = transaction

    async def callback(self, interaction: discord.Interaction) -> None:
        # sourcery no-metrics
        if TYPE_CHECKING:
            assert interaction.user is not None
        transaction = self.transaction
        try:
            if transaction.status is not TransactionStatus.PENDING:
                await interaction.response.edit_message(view=None)
                return await interaction.followup.send(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        f"Transaction {transaction.id} is no longer pending!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            transaction.status = TransactionStatus.ACCEPTED
            if (
                (
                    transaction.from_ is None
                    or transaction.to_nation is None
                    or transaction.from_.alliance is None
                )
                if transaction.type is TransactionType.WITHDRAW
                else (
                    transaction.from_grant is None
                    or transaction.to_nation is None
                    or transaction.from_grant.alliance is None
                )
            ):
                transaction.status = TransactionStatus.FAILED
                return await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "One party involved in this transaction no longer exists! Please try sending a new transaction again.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            if TYPE_CHECKING:
                assert transaction.from_ is not None
                assert transaction.from_grant is not None
                assert transaction.from_.alliance is not None
                assert transaction.from_grant.alliance is not None
            if (
                transaction.type is TransactionType.GRANT_WITHDRAW
                and transaction.from_grant.status is not GrantStatus.PENDING
            ):
                transaction.status = TransactionStatus.FAILED
                return await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "This grant has already been completed!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            if (
                any(
                    value < getattr(transaction.resources, key)
                    for key, value in transaction.from_.resources.to_dict().items()
                )
                if transaction.type is TransactionType.WITHDRAW
                else False
            ):
                transaction.status = TransactionStatus.FAILED
                await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "The sending account does not have enough resources to complete this transaction! Please try sending a new transaction again.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
                owner = transaction.from_.owner
                if owner is not None:
                    await owner.send(
                        embed=funcs.get_embed_author_member(
                            interaction.user,
                            f"Your withdrawl request has failed. Transaction #{transaction.id}.",
                            color=discord.Color.red(),
                        )
                    )
                return
            alliance_settings = await AllianceSettings.fetch(
                transaction.from_.alliance_id
                if transaction.type is TransactionType.WITHDRAW
                else transaction.from_grant.alliance_id
            )
            offshore = alliance_settings.offshore
            if transaction.type is TransactionType.WITHDRAW:
                transaction.from_.resources -= transaction.resources
            view = discord.ui.View()
            note = urllib.parse.quote(
                f"Rift Withdrawal from Account #{transaction.from_.id} and note: {transaction.note}"
                if transaction.type is TransactionType.WITHDRAW
                else f"Rift Grant #{transaction.from_grant.id} and note: {transaction.note}",
            )
            recipient = urllib.parse.quote_plus(
                transaction.to_nation.name if transaction.to_nation is not None else ""
            )
            view.add_item(  # type: ignore
                discord.ui.Button(
                    label="Main Alliance",
                    url=f"https://politicsandwar.com/alliance/id={transaction.from_.alliance_id if transaction.type is TransactionType.WITHDRAW else transaction.from_grant.alliance_id}&display=bank&{'&'.join(f'w_{key}={value}' for key, value in transaction.resources.to_dict().items() if value > 0)}&w_recipient={recipient}&w_note={note}",
                )
            )
            if offshore is not None and alliance_settings.withdraw_from_offshore:
                view.add_item(  # type: ignore
                    discord.ui.Button(
                        label="Offshore",
                        url=f"https://politicsandwar.com/alliance/id={alliance_settings.offshore_id}&display=bank&{'&'.join(f'w_{key}={value}' for key, value in transaction.resources.to_dict().items() if value > 0)}&w_recipient={recipient}&w_note={note}",
                    )
                )
            await interaction.response.edit_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    f"Withdrawal of {transaction.resources} from account #{transaction.from_.id:,} approved by {interaction.user.mention}!"
                    if transaction.type is TransactionType.WITHDRAW
                    else f"Grant #{transaction.from_grant.id} of {transaction.resources} approved by {interaction.user.mention}!",
                    color=discord.Color.green(),
                ),
                view=None,
            )
            await interaction.followup.send(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    f"Please use one of the links below to send the resources for transaction #{transaction.id}.",
                    color=discord.Color.green(),
                ),
                view=view,
                ephemeral=True,
            )
            owner = (
                transaction.from_.owner
                if transaction.type is TransactionType.WITHDRAW
                else transaction.from_grant.recipient
            )
            if owner is not None:
                await owner.send(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        f"Your {'grant ' if transaction.type is TransactionType.GRANT_WITHDRAW else ''}withdrawl request has been approved! Please wait for the resources to be sent. Transaction #{transaction.id}.",
                        color=discord.Color.green(),
                    )
                )
            if transaction.type is TransactionType.WITHDRAW:
                await transaction.from_.save()
            else:
                grant = transaction.from_grant
                grant.status = GrantStatus.SENT
                await grant.save()
        finally:
            await transaction.save()


class TransactionRequestRejectButton(discord.ui.Button[TransactionRequestView]):
    def __init__(self, transaction: Transaction, custom_id: str):
        super().__init__(
            custom_id=custom_id, style=discord.ButtonStyle.red, label="Reject"
        )
        self.transaction: Transaction = transaction

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert interaction.user is not None
        self.transaction.status = TransactionStatus.REJECTED
        await self.transaction.save()
        await interaction.response.edit_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                f"Transaction #{self.transaction.id:,} rejected by {interaction.user.mention}!",
                color=discord.Color.red(),
            ),
            view=None,
        )
        if (
            self.transaction.type is TransactionType.GRANT_WITHDRAW
            or self.transaction.type is TransactionType.GRANT
        ):
            grant = self.transaction.from_grant
            if grant is not None:
                grant.status = GrantStatus.REJECTED
                await grant.save()
        if (
            self.transaction.type is TransactionType.WITHDRAW
            or self.transaction.type is TransactionType.GRANT_WITHDRAW
        ):
            if (
                self.transaction.from_ is None
                and self.transaction.type is TransactionType.WITHDRAW
            ) or (
                self.transaction.from_grant is None
                and self.transaction.type is TransactionType.GRANT_WITHDRAW
            ):
                return
            if TYPE_CHECKING:
                assert self.transaction.from_ is not None
                assert self.transaction.from_grant is not None
            owner = (
                self.transaction.from_.owner
                if self.transaction.type is TransactionType.WITHDRAW
                else self.transaction.from_grant.recipient
            )
            if owner is not None:
                await owner.send(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        f"Your {'grant ' if self.transaction.type is TransactionType.GRANT_WITHDRAW else ''}withdrawl request has been rejected! Please wait for the resources to be sent. Transaction #{self.transaction.id}.",
                        color=discord.Color.red(),
                    )
                )
            return


class TransactionRequestCancelButton(discord.ui.Button[TransactionRequestView]):
    def __init__(self, transaction: Transaction, custom_id: str):
        super().__init__(
            custom_id=custom_id, style=discord.ButtonStyle.grey, label="Cancel"
        )
        self.transaction: Transaction = transaction

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert interaction.user is not None
        self.transaction.status = TransactionStatus.CANCELLED
        await self.transaction.save()
        await interaction.response.send_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                "Transaction cancelled!",
                color=discord.Color.red(),
            ),
            ephemeral=True,
        )


class DepositConfirm(discord.ui.View):
    def __init__(
        self,
        account: Account,
        resources: Resources,
        credentials: Optional[Credentials],
        note: str,
    ) -> None:
        super().__init__(timeout=300)
        self.account: Account = account
        self.resources: Resources = resources
        self.credentials: Optional[Credentials] = credentials
        self.note: str = note
        if (
            self.credentials is None
            or not self.credentials.permissions.send_nation_bank
        ):
            self.add_item(DepositConfirmCredentialsButton(disabled=True))  # type: ignore
        else:
            self.add_item(DepositConfirmCredentialsButton())  # type: ignore
        self.add_item(DepositConfirmCancelButton())  # type: ignore
        url = f"https://politicsandwar.com/alliance/id={account.alliance_id}&display=bank&{'&'.join(f'd_{key}={value}' for key, value in resources.to_dict().items() if value > 0)}&d_note={self.account.deposit_code}"
        self.add_item(discord.ui.Button(label="Manual Transfer", url=url))  # type: ignore
        self.result: Optional[bool] = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if TYPE_CHECKING:
            assert interaction.user is not None
        return interaction.user.id == self.account.owner_id


class DepositConfirmCredentialsButton(discord.ui.Button[DepositConfirm]):
    def __init__(self, disabled: bool = False) -> None:
        super().__init__(
            style=discord.ButtonStyle.green
            if not disabled
            else discord.ButtonStyle.grey,
            label="Auto Transfer",
            disabled=disabled,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert self.view is not None
            assert interaction.user is not None
            assert self.view.credentials is not None
            assert self.view.account.alliance is not None
            assert self.view.credentials.nation is not None
        await interaction.response.edit_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                f"Depositing {self.view.resources} into account #{self.view.account.id:,}...",
                color=discord.Color.orange(),
            ),
            view=None,
        )
        result = await funcs.deposit(
            self.view.resources,
            self.view.account.alliance,
            self.view.credentials,
            note=f"Automatic Deposit with {f'note {self.view.note}' if self.view.note else 'no note'}",
        )
        if result:
            transaction = await Transaction.create(
                datetime.datetime.now(tz=datetime.timezone.utc),
                TransactionStatus.ACCEPTED,
                TransactionType.DEPOSIT,
                interaction.user,
                self.view.account,
                self.view.credentials.nation,
                self.view.resources,
                self.view.note,
                from_type=AccountType.NATION,
            )
            self.view.account.resources += self.view.resources
            await self.view.account.save()
            await interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    f"Deposited {self.view.resources} into account #{self.view.account.id:,}. The transaction ID is {transaction.id:,}.",
                    color=discord.Color.green(),
                ),
            )
        else:
            await interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    "Deposit failed! Please try again.",
                    color=discord.Color.red(),
                ),
            )
        self.view.stop()


class DepositConfirmCancelButton(discord.ui.Button[DepositConfirm]):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Cancel",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert self.view is not None
            assert interaction.user is not None
        await interaction.response.edit_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                f"Cancelled deposit of {self.view.resources} into account #{self.view.account.id:,}.",
                color=discord.Color.red(),
            ),
            view=None,
        )
        self.view.stop()


class TransactionHistoryView(discord.ui.View):
    def __init__(
        self,
        user: Union[discord.Member, discord.User],
        transactions: List[Transaction],
        description: str,
        page: int,
    ) -> None:
        super().__init__(timeout=300)
        self.user: Union[discord.Member, discord.User] = user
        self.transactions: List[Transaction] = transactions
        self.page: int = page
        self.pages: int = (len(transactions) // 9) + (len(transactions) % 12 > 0)
        self.description: str = description
        if self.pages == 1:
            self.back_button.disabled = True  # type: ignore
            self.forward_button.disabled = True  # type: ignore
        if self.page == 1:
            self.back_button.disabled = True  # type: ignore

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user is not None and interaction.user.id == self.user.id

    def get_embed(self, user: Union[discord.Member, discord.User]) -> discord.Embed:
        fields: List[Field] = [
            i.field for i in self.transactions[(self.page - 1) * 9 : (self.page) * 9]
        ]
        return funcs.get_embed_author_member(
            user,
            self.description.format(page=self.page, pages=self.pages),
            fields=fields,
            color=discord.Color.blue(),
        )

    async def callback(
        self,
        button: discord.ui.Button[TransactionHistoryView],
        interaction: discord.Interaction,
        page: int,
    ):
        if TYPE_CHECKING:
            assert interaction.user is not None
        self.page = page
        if self.page == 1:
            self.back_button.disabled = True  # type: ignore
            self.forward_button.disabled = self.pages <= 1  # type: ignore
        elif self.page == self.pages:
            self.back_button.disabled = False  # type: ignore
            self.forward_button.disabled = True  # type: ignore
        else:
            self.back_button.disabled = False  # type: ignore
            self.forward_button.disabled = False  # type: ignore
        await interaction.response.edit_message(
            embed=self.get_embed(interaction.user), view=self
        )

    @discord.ui.button(  # type: ignore
        label="Back",
        style=discord.ButtonStyle.gray,
        disabled=True,
    )
    async def back_button(
        self,
        button: discord.ui.Button[TransactionHistoryView],
        interaction: discord.Interaction,
    ):
        await self.callback(button, interaction, self.page - 1)

    @discord.ui.button(  # type: ignore
        label="Forward",
        style=discord.ButtonStyle.gray,
    )
    async def forward_button(
        self,
        button: discord.ui.Button[TransactionHistoryView],
        interaction: discord.Interaction,
    ):
        await self.callback(button, interaction, self.page + 1)


class PayConfirm(discord.ui.View):
    def __init__(
        self,
        grant: Grant,
        resources: Resources,
        credentials: Optional[Credentials],
        note: str,
    ) -> None:
        super().__init__(timeout=300)
        self.grant: Grant = grant
        self.resources: Resources = resources
        self.credentials: Optional[Credentials] = credentials
        self.note: str = note
        if (
            self.credentials is None
            or not self.credentials.permissions.send_nation_bank
        ):
            self.add_item(PayConfirmCredentialsButton(disabled=True))  # type: ignore
        else:
            self.add_item(PayConfirmCredentialsButton())  # type: ignore
        self.add_item(DepositConfirmCancelButton())  # type: ignore
        url = f"https://politicsandwar.com/alliance/id={grant.alliance_id}&display=bank&{'&'.join(f'd_{key}={value}' for key, value in resources.to_dict().items() if value > 0)}&d_note={self.grant.code}"
        self.add_item(discord.ui.Button(label="Manual Transfer", url=url))  # type: ignore
        self.result: Optional[bool] = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if TYPE_CHECKING:
            assert interaction.user is not None
        return interaction.user.id == self.grant.recipient_id


class PayConfirmCredentialsButton(discord.ui.Button[PayConfirm]):
    def __init__(self, disabled: bool = False) -> None:
        super().__init__(
            style=discord.ButtonStyle.green
            if not disabled
            else discord.ButtonStyle.grey,
            label="Auto Transfer",
            disabled=disabled,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert self.view is not None
            assert interaction.user is not None
            assert self.view.credentials is not None
            assert self.view.grant.alliance is not None
            assert self.view.credentials.nation is not None
        await interaction.response.edit_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                f"Paying off {self.view.resources} of grant #{self.view.grant.id:,}...",
                color=discord.Color.orange(),
            ),
            view=None,
        )
        result = await funcs.deposit(
            self.view.resources,
            self.view.grant.alliance,
            self.view.credentials,
            note=f"Automatic Grant Payoff with {f'note {self.view.note}' if self.view.note else 'no note'}",
        )
        if result:
            transaction = await Transaction.create(
                datetime.datetime.now(tz=datetime.timezone.utc),
                TransactionStatus.ACCEPTED,
                TransactionType.GRANT_DEPOSIT,
                interaction.user,
                self.view.grant,
                self.view.credentials.nation,
                self.view.resources,
                self.view.note,
                to_type=AccountType.GRANT,
                from_type=AccountType.NATION,
            )
            self.view.grant.paid += self.view.resources
            await self.view.grant.save()
            await interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    f"Payed off {self.view.resources} of grant #{self.view.grant.id:,}. The transaction ID is {transaction.id:,}.",
                    color=discord.Color.green(),
                ),
            )
        else:
            await interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    "Pay off failed! Please try again.",
                    color=discord.Color.red(),
                ),
            )
        self.view.stop()


class PayConfirmCancelButton(discord.ui.Button[PayConfirm]):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Cancel",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert self.view is not None
            assert interaction.user is not None
        await interaction.response.edit_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                f"Cancelled paying of {self.view.resources} towards grant #{self.view.grant.id:,}.",
                color=discord.Color.red(),
            ),
            view=None,
        )
        self.view.stop()
