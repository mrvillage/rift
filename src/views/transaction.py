from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import discord

from .. import funcs
from ..cache import cache
from ..data.classes import Transaction
from ..enums import AccountType, TransactionStatus, TransactionType
from ..errors import NoCredentialsError

__all__ = ("TransactionRequestView", "DepositConfirm")

if TYPE_CHECKING:
    from typing import Optional

    from ..data.classes import (
        Account,
        Credentials,
        Resources,
        Transaction,
        TransactionRequest,
    )


class TransactionRequestView(discord.ui.View):
    def __init__(
        self,
        request: TransactionRequest,
        user_id: int,
    ) -> None:
        super().__init__(timeout=None)
        self.request: TransactionRequest = request
        transaction = self.request.transaction
        if transaction is None:
            return
        self.user_id: int = user_id
        self.add_item(TransactionRequestAcceptButton(transaction, custom_id=request.accept_custom_id))  # type: ignore
        self.add_item(TransactionRequestRejectButton(transaction, custom_id=request.reject_custom_id))  # type: ignore
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
            if (
                self.request.transaction is None
                or self.request.transaction.from_ is None
            ):
                return False
            alliance_id = self.request.transaction.from_.alliance_id
            user_id = interaction.user.id
            roles = [
                i
                for i in cache.roles
                if alliance_id == i.alliance_id
                and user_id in i.member_ids
                and (
                    i.permissions.send_nation_safekeeping
                    or i.permissions.leadership
                    or i.permissions.manage_bank_accounts
                )
            ]
            return bool(roles)
        if interaction.user.id == self.user_id:
            return True
        await interaction.response.send_message(
            embed=funcs.get_embed_author_member(
                interaction.user, "You're not allowed to use this menu!"
            ),
            ephemeral=True,
        )
        return False


class TransactionRequestAcceptButton(discord.ui.Button[TransactionRequestView]):
    def __init__(self, transaction: Transaction, custom_id: str):
        super().__init__(
            custom_id=custom_id, style=discord.ButtonStyle.green, label="Accept"
        )
        self.transaction: Transaction = transaction

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert interaction.user is not None
        transaction = self.transaction
        if transaction.status is not TransactionStatus.PENDING:
            await interaction.edit_original_message(view=None)
            return await interaction.followup.send(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    f"Transaction {transaction.id} is no longer pending!",
                ),
                ephemeral=True,
            )
        transaction.status = TransactionStatus.ACCEPTED
        if transaction.type is TransactionType.TRANSFER:
            if transaction.to is None or transaction.from_ is None:
                return await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "One account involved in this transaction no longer exists! Please try sending a new transaction again.",
                    ),
                    ephemeral=True,
                )
            if any(
                value < transaction.resources[key]
                for key, value in transaction.resources.to_dict().items()
            ):
                return await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "The sending account does not have enough resources to complete this transaction! Please try sending a new transaction again.",
                    ),
                    ephemeral=True,
                )
            transaction.to.resources += transaction.resources
            transaction.from_.resources -= transaction.resources
            await transaction.save()
            await interaction.response.send_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    f"Transaction accepted! {transaction.resources} has been added to account #{transaction.to_id:,}.",
                ),
                ephemeral=True,
            )
        elif transaction.type is TransactionType.WITHDRAW:
            if (
                transaction.from_ is None
                or transaction.to_nation is None
                or transaction.from_.alliance is None
            ):
                return await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "One party involved in this transaction no longer exists! Please try sending a new transaction again.",
                    ),
                    ephemeral=True,
                )
            await interaction.response.defer(ephemeral=True)
            resources = await transaction.from_.alliance.fetch_bank()
            if any(
                value < getattr(transaction.resources, key)
                for key, value in resources.to_dict().items()
            ):
                return await interaction.response.send_message(
                    embed=funcs.get_embed_author_member(
                        interaction.user,
                        "The sending alliance does not have enough resources to complete this transaction! Please try sending a new transaction again.",
                    ),
                    ephemeral=True,
                )
            credentials = funcs.credentials.find_highest_alliance_credentials(
                transaction.from_.alliance, "send_alliance_bank"
            )
            if credentials is None:
                raise NoCredentialsError(transaction.from_.alliance)
            await funcs.withdraw(
                transaction.resources,
                transaction.to_nation,
                credentials,
                note=f"Rift Withdrawal from Account #{transaction.from_.id} and note: {transaction.note}",
            )
            transaction.from_.resources -= resources
            await transaction.from_.save()
            await interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,
                    f"Withdrawal of {transaction.resources} from account #{transaction.from_.id:,} approved by {interaction.user.mention}!",
                    color=discord.Color.green(),
                ),
                view=None,
            )


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
        )


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
                interaction.user, "Transaction cancelled!"
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
                datetime.datetime.utcnow(),
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