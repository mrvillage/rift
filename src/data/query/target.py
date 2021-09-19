from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.data.db.sql import execute_read_query

from ..db import execute_query

__all__ = ("add_target", "edit_target", "remove_target")

if TYPE_CHECKING:
    from typings import TargetData


async def add_target(
    target_id: int,
    owner_id: int,
    channel_ids: List[int],
    role_ids: List[int],
    user_ids: List[int],
    direct_message: bool,
    /,
) -> TargetData:
    target = dict(
        (
            await execute_read_query(
                "INSERT INTO targets (target_id, owner_id, channel_ids, role_ids, user_ids, direct_message) VALUES ($1, $2, $3, $4, $5, $6) RETURNING (id, target_id, owner_id, channel_ids, role_ids, user_ids, direct_message);",
                target_id,
                owner_id,
                channel_ids,
                role_ids,
                user_ids,
                direct_message,
            )
        )[0]
    )["row"]
    return {
        "id": target[0],
        "target_id": target[1],
        "owner_id": target[2],
        "channel_ids": target[3],
        "role_ids": target[4],
        "user_ids": target[5],
        "direct_message": target[6],
    }


async def edit_target(target_id: int, /) -> None:
    ...


async def remove_target(target_id: int, /) -> None:
    await execute_query("DELETE FROM targets WHERE target_id = $1;", target_id)
