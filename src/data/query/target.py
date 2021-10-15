from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.data.db.sql import execute_read_query

from ..db import execute_query

__all__ = ("add_target_reminder", "edit_target_reminder", "remove_target_reminder")

if TYPE_CHECKING:
    from _typings import TargetReminderData


async def add_target_reminder(
    target_id: int,
    owner_id: int,
    channel_ids: List[int],
    role_ids: List[int],
    user_ids: List[int],
    direct_message: bool,
    /,
) -> TargetReminderData:
    target = await execute_read_query(
        "INSERT INTO target_reminders (target_id, owner_id, channel_ids, role_ids, user_ids, direct_message) VALUES ($1, $2, $3, $4, $5, $6) RETURNING (id);",
        target_id,
        owner_id,
        channel_ids,
        role_ids,
        user_ids,
        direct_message,
    )
    return {
        "id": target[0]["id"],
        "target_id": target_id,
        "owner_id": owner_id,
        "channel_ids": channel_ids,
        "role_ids": role_ids,
        "user_ids": user_ids,
        "direct_message": direct_message,
    }


async def edit_target_reminder(id: int, /) -> None:
    ...


async def remove_target_reminder(id: int, /) -> None:
    await execute_query("DELETE FROM target_reminders WHERE id = $1;", id)
