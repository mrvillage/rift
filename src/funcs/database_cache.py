from __future__ import annotations

import asyncio

from src.data.db.sql import execute_read_query

from ..data.db import execute_query, execute_query_many

__all__ = ("fill_database_cache",)

from ..ref import bot


async def fill_database_cache() -> None:

    guilds = [
        {
            "id": i.id,
            "name": i.name,
            "icon_url": i.icon and i.icon.url,
            "owner_id": i.owner_id,
        }
        for i in bot.guilds
    ]
    members = [
        {"id": i.id, "guild": i.guild.id, "permissions": i.guild_permissions.value}
        for i in bot.get_all_members()
    ]
    users = [
        {
            "id": i.id,
            "name": i.name,
            "discriminator": i.discriminator,
            "bot": i.bot,
            "display_avatar_url": i.display_avatar.url,
        }
        for i in bot.users
    ]
    current_guilds = await execute_read_query("SELECT * FROM cache_guilds;")
    current_members = await execute_read_query("SELECT * FROM cache_members;")
    current_users = await execute_read_query("SELECT * FROM cache_users;")
    guild_ids = [i["id"] for i in guilds]
    member_ids = [(i["id"], i["guild"]) for i in members]
    user_ids = [i["id"] for i in users]
    for guild in current_guilds:
        if guild["id"] not in guild_ids:
            await execute_query("DELETE FROM cache_guilds WHERE id = $1;", guild["id"])
            await execute_query(
                "DELETE FROM cache_members WHERE guild = $1;",
                guild["id"],
            )
    for member in current_members:
        if (member["id"], member["guild"]) not in member_ids:
            await execute_query(
                "DELETE FROM cache_members WHERE id = $1 AND guild = $2;",
                member["id"],
                member["guild"],
            )
    for user in current_users:
        if user["id"] not in user_ids:
            await execute_query(
                "DELETE FROM cache_users WHERE id = $1;",
                user["id"],
            )
    queries = [
        "INSERT INTO cache_guilds (id, name, icon_url, owner_id) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO UPDATE SET name = $2, icon_url = $3, owner_id = $4 WHERE cache_guilds.id = $1;",
        "INSERT INTO cache_members (id, guild, permissions) VALUES ($1, $2, $3) ON CONFLICT (id, guild) DO UPDATE SET permissions = $3 WHERE cache_members.id = $1 AND cache_members.guild = $2;",
        "INSERT INTO cache_users (id, name, discriminator, bot, display_avatar_url) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO UPDATE SET name = $2, discriminator = $3, display_avatar_url = $5 WHERE cache_users.id = $1;",
    ]
    await asyncio.gather(
        *[
            execute_query_many(query, data)  # type: ignore
            for query, data in zip(
                queries,
                [
                    [tuple(i.values()) for i in guilds],
                    [tuple(i.values()) for i in members],
                    [tuple(i.values()) for i in users],
                ],
            )
        ]
    )
