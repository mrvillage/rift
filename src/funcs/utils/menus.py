from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Optional, Sequence

import discord

if TYPE_CHECKING:
    from ...data.classes import MenuItem


async def get_row(
    message: discord.Message,
    type_: str,
    flags: Mapping[str, Any],
    items: Sequence[Sequence[MenuItem]],
) -> Optional[
    int
]:  # sourcery skip: merge-duplicate-blocks, merge-nested-ifs, remove-redundant-if
    from .. import get_embed_author_member

    try:
        if "row" in flags:
            row_num = int(flags["row"][0]) - 1
        else:
            for index, row in enumerate(items):
                if len(row) == 5:
                    continue
                elif not row:
                    return index
                elif row[0].type == "select":
                    continue
                else:
                    return index
            await message.reply(
                embed=get_embed_author_member(
                    message.author, "There's no space for that item in the menu!"
                )
            )
            return None
        if 0 < row_num < 6:
            row = items[row_num]
            if row:
                if (
                    row[0].type == "select"
                    or len(row) == 5
                    or (type_ == "select" and len(row) != 0)
                ):
                    await message.reply(
                        embed=get_embed_author_member(
                            message.author,
                            f"Row {row_num} doesn't have space for your item!",
                        )
                    )
                    return
            return row_num
        raise ValueError
    except ValueError:
        await message.reply(
            embed=get_embed_author_member(
                message.author, f"`{flags['row'][0]}` is not a valid row!"
            )
        )
        return
