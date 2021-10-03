from __future__ import annotations

from typing import Optional

from ..data.db import execute_query

__all__ = ("edit_log",)


async def edit_log(
    datetime: str,
    message_id: int,
    channel_id: int,
    guild_id: Optional[int],
    author_id: int,
    message_content: str,
    qualified_name: Optional[str],
    success: Optional[bool] = None,
    error_message: Optional[str] = None,
) -> None:
    await execute_query(
        """
        UPDATE command_logs
        SET
            success = $8,
            error_message =  $9
        WHERE
            datetime = $1 AND
            message_id = $2 AND
            channel_id = $3 AND
            guild_id = $4 AND
            author_id = $5 AND
            message_content = $6 AND
            qualified_name = $7;
        """,
        datetime,
        message_id,
        channel_id,
        guild_id,
        author_id,
        message_content,
        qualified_name,
        success,
        error_message,
    )
