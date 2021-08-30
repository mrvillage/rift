from __future__ import annotations

from typing import Optional

from ..data.db import execute_query


async def insert_log(
    time: str,
    message_id: int,
    channel_id: int,
    guild_id: Optional[int],
    author_id: int,
    message_content: str,
    qualified_name: Optional[str],
    args: str,
    kwargs: str,
    success: bool = None,
    error_message: str = None,
) -> None:
    await execute_query(
        """
        INSERT INTO command_logs (datetime, message_id, channel_id, guild_id, author_id, message_content, qualified_name, args, kwargs, success, error_message)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);
        """,
        time,
        message_id,
        channel_id,
        guild_id,
        author_id,
        message_content,
        qualified_name,
        args,
        kwargs,
        success,
        error_message,
    )
