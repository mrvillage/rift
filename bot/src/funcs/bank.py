from __future__ import annotations

from typing import TYPE_CHECKING

import pnwkit
from bs4 import BeautifulSoup

from ..env import PNW_BOT_KEY

if TYPE_CHECKING:
    from typing import Optional, Union

    from ..data.classes import Alliance, Credentials, Nation, Resources

__all__ = (
    "parse_bank_token",
    "withdraw",
    "deposit",
)


def parse_bank_token(content: str) -> str:
    data = BeautifulSoup(content, "html.parser")
    return data.find("input", {"name": "token"}).attrs["value"]  # type: ignore


async def withdraw(
    resources: Resources,
    receiver: Union[Alliance, Nation],
    credentials: Credentials,
    *,
    note: Optional[str] = None,
) -> bool:
    from ..data.classes import Nation

    kit = pnwkit.Kit(credentials.api_key, async_=True)
    kit.set_bot_key(PNW_BOT_KEY)
    try:
        await kit.bank_withdraw_mutation(
            {
                **resources.to_dict(),
                "receiver": receiver.id,
                "receiver_type": 1 if isinstance(receiver, Nation) else 2,
                "note": note,
            }
        )
        return True
    except Exception:
        return False


async def deposit(
    resources: Resources,
    credentials: Credentials,
    *,
    note: Optional[str] = None,
) -> bool:
    kit = pnwkit.Kit(credentials.api_key, async_=True)
    kit.set_bot_key(PNW_BOT_KEY)
    try:
        await kit.bank_deposit_mutation(
            {
                **resources.to_dict(),
                "note": note,
            }
        )
        return True
    except Exception:
        return False


# async def withdraw(
#     resources: Resources,
#     receiver: Union[Alliance, Nation],
#     credentials: Credentials,
#     *,
#     note: Optional[str] = None,
# ) -> bool:
#     async with aiohttp.ClientSession() as session:
#         success = await credentials.login(session)
#         if not success:
#             return False
#         data: Dict[str, Any] = {
#             f"with{key}": value for key, value in resources.to_dict().items()
#         }
#         data["withtype"] = type(receiver).__name__
#         if note is not None:
#             data["withnote"] = note
#         data["withrecipient"] = receiver.name
#         data["withsubmit"] = "Withdraw"
#         success, token = await withdraw_request(credentials, data, session)
#         if not success:
#             data["token"] = token
#             success, token = await withdraw_request(credentials, data, session)
#         return success


# async def withdraw_request(
#     credentials: Credentials,
#     data: Dict[str, Any],
#     session: aiohttp.ClientSession,
# ) -> Tuple[bool, str]:
#     if TYPE_CHECKING:
#         assert credentials.nation is not None
#     content = await actual_withdraw_request(
#         session, credentials.nation.alliance_id, data
#     )
#     token = parse_bank_token(content)
#     return (
#         "Something went wrong" not in content and "successfully transferred" in content
#     ), token


# async def actual_withdraw_request(
#     session: aiohttp.ClientSession,
#     alliance_id: int,
#     data: Dict[str, Any],
# ) -> str:
#     async with session.request(
#         "POST",
#         f"https://politicsandwar.com/alliance/id={alliance_id}&display=bank",
#         data=data,
#     ) as response:
#         return await response.text()


# async def deposit(
#     resources: Resources,
#     receiver: Alliance,
#     credentials: Credentials,
#     *,
#     note: Optional[str] = None,
# ) -> bool:
#     async with aiohttp.ClientSession() as session:
#         success = await credentials.login(session)
#         if not success:
#             return False
#         data: Dict[str, Any] = {
#             f"dep{key}": value for key, value in resources.to_dict().items()
#         }
#         if note is not None:
#             data["depnote"] = note
#         data["deprecipient"] = receiver.name
#         data["depsubmit"] = "Deposit"
#         success, token = await deposit_request(credentials, data, session)
#         if not success:
#             data["token"] = token
#             success, token = await deposit_request(credentials, data, session)
#         return success


# async def deposit_request(
#     credentials: Credentials,
#     data: Dict[str, Any],
#     session: aiohttp.ClientSession,
# ) -> Tuple[bool, str]:
#     if TYPE_CHECKING:
#         assert credentials.nation is not None
#     content = await actual_deposit_request(
#         session, credentials.nation.alliance_id, data
#     )
#     token = parse_bank_token(content)
#     return (
#         "Something went wrong" not in content
#         and "successfully made a deposit" in content
#     ), token


# async def actual_deposit_request(
#     session: aiohttp.ClientSession,
#     alliance_id: int,
#     data: Dict[str, Any],
# ) -> str:
#     async with session.request(
#         "POST",
#         f"https://politicsandwar.com/alliance/id={alliance_id}&display=bank",
#         data=data,
#     ) as response:
#         return await response.text()
