from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel
from src.bot import bot

from .interaction import MockInteraction

__all__ = ("mock", "build_mock", "build_application_command_mock")

if TYPE_CHECKING:
    from typing import Any

    from quarrel import Missing
    from quarrel.types.interactions import (
        Interaction,
        InteractionData,
        InteractionDataApplicationCommandOption,
    )
    from quarrel.types.member import MemberWithUser
    from quarrel.types.message import Message
    from quarrel.types.snowflake import Snowflake
    from quarrel.types.user import User


def mock(data: Interaction) -> MockInteraction:
    return MockInteraction(data, bot.state)


def build_mock(
    type: quarrel.InteractionType,
    *,
    data: InteractionData,
    guild_id: Missing[Snowflake] = quarrel.MISSING,
    channel_id: Missing[Snowflake] = quarrel.MISSING,
    member: Missing[MemberWithUser] = quarrel.MISSING,
    user: Missing[User] = quarrel.MISSING,
    message: Missing[Message] = quarrel.MISSING,
) -> MockInteraction:
    payload: Interaction = {
        "id": "0",
        "application_id": "1",
        "type": type.value,
        "token": "token123",
        "version": 1,
        "guild_id": guild_id if guild_id is not quarrel.MISSING else DEFAULT_GUILD_ID,
        "channel_id": channel_id
        if channel_id is not quarrel.MISSING
        else DEFAULT_CHANNEL_ID,
        "member": member
        if member is not quarrel.MISSING
        else DEFAULT_INTERACTION_MEMBER,
    }
    if user is not quarrel.MISSING:
        payload["user"] = user
    if message is not quarrel.MISSING:
        payload["message"] = message
    payload["data"] = data
    return mock(payload)


def build_application_command_mock(
    *,
    guild_id: Missing[Snowflake] = quarrel.MISSING,
    channel_id: Missing[Snowflake] = quarrel.MISSING,
    member: Missing[MemberWithUser] = quarrel.MISSING,
    user: Missing[User] = quarrel.MISSING,
    message: Missing[Message] = quarrel.MISSING,
) -> MockInteraction:
    return build_mock(
        quarrel.InteractionType.APPLICATION_COMMAND,
        data={},  # type: ignore
        guild_id=guild_id,
        channel_id=channel_id,
        member=member,
        user=user,
        message=message,
    )


def command_to_options(
    command: quarrel.SlashCommand[Any], **options: Any
) -> list[InteractionDataApplicationCommandOption]:
    payload = command.to_payload().get("options", [])
    for i in payload:
        i["value"] = options[i["name"]]  # type: ignore
    return payload  # type: ignore


DEFAULT_GUILD_ID = "1234"
DEFAULT_CHANNEL_ID = "5678"
DEFAULT_INTERACTION_MEMBER: MemberWithUser = {
    "roles": [],
    "joined_at": "2020-01-01T00:00:00.000Z",
    "deaf": False,
    "mute": False,
    "nick": None,
    "avatar": None,
    "user": {
        "id": "1234",
        "username": "user",
        "discriminator": "1234",
        "avatar": None,
        "bot": False,
        "system": False,
    },
}
