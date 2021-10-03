from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from ..ref import bot

if TYPE_CHECKING:
    from ..data.classes import Alliance, Nation, Transaction

__all__ = ("withdraw",)


async def withdraw(
    *,
    transaction: Transaction,
    receiver: Union[Alliance, Nation],
    note: Optional[str] = None
):
    transaction_data = transaction.get_data_withdraw()
    transaction_data["withtype"] = type(receiver).__name__
    if note is not None:
        transaction_data["withnote"] = note
    transaction_data["withrecipient"] = receiver.name
    if bot.auth_token is not None:
        transaction_data["token"] = bot.auth_token
    async with bot.pnw_session.request(
        "POST",
        "https://politicsandwar.com/alliance/id=3683&display=bank",
        data=transaction_data,
    ) as response:
        content = await response.text()
    await bot.parse_token(content)
    return (
        "Something went wrong" not in content and "successfully transferred" in content
    )
