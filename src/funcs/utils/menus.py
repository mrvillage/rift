from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Sequence

import discord

if TYPE_CHECKING:
    from ...data.classes import MenuItem


async def get_row(
    message: discord.Message,
    type_: str,
    flags: Mapping[str, Any],
    items: Sequence[Sequence[MenuItem]],
) -> int:  # sourcery skip: merge-nested-ifs
    from .. import get_embed_author_member

    try:
        if "row" in flags:
            row_num = int(flags["row"][0]) - 1
        else:
            return None
        if 0 < row_num < 6:
            row = items[row_num - 1]
            if row:
                if row[0].type == "select" and len(row) == 5:
                    await message.reply(
                        embed=get_embed_author_member(
                            message.author,
                            f"Row {row_num} and all the ones after don't have space for your item!",
                        )
                    )
                    return -1
            return row_num
        raise ValueError
    except ValueError:
        await message.reply(
            embed=get_embed_author_member(
                message.author, f"`{flags['row'][0]}` is not a valid row!"
            )
        )
        return -1
