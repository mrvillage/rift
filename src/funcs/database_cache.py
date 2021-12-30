from __future__ import annotations

import asyncio

from src.data.db.sql import execute_read_query

from ..data.db import execute_query, execute_query_many

__all__ = ("fill_database_cache",)

from ..ref import bot


async def fill_database_cache() -> None:  # sourcery no-metrics

    guilds = [
        {
            "id": i.id,
            "name": i.name,
            "icon_url": i.icon.url if i.icon is not None else None,
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
    roles = [
        {
            "id": j.id,
            "name": j.name,
            "guild": j.guild.id,
            "color": j.color.value,
            "members": [k.id for k in j.members],
            "permissions": j.permissions.value,
            "position": j.position,
            "tags": {
                "is_bot_managed": j.tags.is_bot_managed() if j.tags else False,
                "is_premium_subscriber": j.tags.is_premium_subscriber()
                if j.tags
                else False,
                "is_integration": j.tags.is_integration() if j.tags else False,
            },
        }
        for i in bot.guilds
        for j in i.roles
    ]
    channels = [
        {
            "id": j.id,
            "category": j.category_id,
            "guild": j.guild.id,
            "name": j.name,
            "overwrites": {
                key.id: value._values  # type: ignore
                for key, value in j.overwrites.items()
                if not value.is_empty()
            },
            "permissions_synced": j.permissions_synced,
            "position": j.position,
            "type": j.type.value,
        }
        for i in bot.guilds
        for j in i.channels
    ]
    channels.sort(key=lambda x: 0 if x["type"] == 4 else 1)
    current_guilds = await execute_read_query("SELECT * FROM cache_guilds;")
    current_members = await execute_read_query("SELECT * FROM cache_members;")
    current_users = await execute_read_query("SELECT * FROM cache_users;")
    current_roles = await execute_read_query("SELECT * FROM cache_roles;")
    current_channels = await execute_read_query("SELECT * FROM cache_channels;")
    guild_ids = [i["id"] for i in guilds]
    member_ids = [(i["id"], i["guild"]) for i in members]
    role_ids = [i["id"] for i in roles]
    channel_ids = [i["id"] for i in channels]
    for guild in current_guilds:
        if guild["id"] not in guild_ids:
            await execute_query(
                "DELETE FROM cache_members WHERE guild = $1;",
                guild["id"],
            )
            await execute_query(
                "DELETE FROM cache_roles WHERE guild = $1;",
                guild["id"],
            )
            await execute_query(
                "DELETE FROM cache_channels WHERE guild = $1;",
                guild["id"],
            )
            await execute_query("DELETE FROM cache_guilds WHERE id = $1;", guild["id"])
    for member in current_members:
        if (member["id"], member["guild"]) not in member_ids:
            await execute_query(
                "DELETE FROM cache_members WHERE id = $1 AND guild = $2;",
                member["id"],
                member["guild"],
            )
    for role in current_roles:
        if role["id"] not in role_ids:
            await execute_query(
                "DELETE FROM cache_roles WHERE id = $1;",
                role["id"],
            )
    for channel in current_channels:
        if channel["id"] not in channel_ids:
            await execute_query(
                "UPDATE cache_channels SET category = NULL WHERE category = $1;",
                channel["id"],
            )
            await execute_query(
                "DELETE FROM cache_channels WHERE id = $1;",
                channel["id"],
            )
    queries = [
        "INSERT INTO cache_guilds (id, name, icon_url, owner_id) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO UPDATE SET name = $2, icon_url = $3, owner_id = $4 WHERE cache_guilds.id = $1;",
        "INSERT INTO cache_members (id, guild, permissions) VALUES ($1, $2, $3) ON CONFLICT (id, guild) DO UPDATE SET permissions = $3 WHERE cache_members.id = $1 AND cache_members.guild = $2;",
        "INSERT INTO cache_users (id, name, discriminator, bot, display_avatar_url) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO UPDATE SET name = $2, discriminator = $3, display_avatar_url = $5 WHERE cache_users.id = $1;",
        "INSERT INTO cache_roles (id, name, guild, color, members, permissions, position, tags) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (id) DO UPDATE SET name = $2, guild = $3, color = $4, members = $5, permissions = $6, position = $7, tags = $8 WHERE cache_roles.id = $1;",
        "INSERT INTO cache_channels (id, category, guild, name, overwrites, permissions_synced, position, type) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (id) DO UPDATE SET category = $2, guild = $3, name = $4, overwrites = $5, permissions_synced = $6, position = $7, type = $8 WHERE cache_channels.id = $1;",
    ]
    current_guilds_dict = {i["id"]: dict(i) for i in current_guilds}
    current_members_dict = {(i["id"], i["guild"]): dict(i) for i in current_members}
    current_users_dict = {i["id"]: dict(i) for i in current_users}
    current_roles_dict = {i["id"]: dict(i) for i in current_roles}
    current_channels_dict = {i["id"]: dict(i) for i in current_channels}
    guilds_purged = [i for i in guilds if i != current_guilds_dict.get(i["id"])]
    members_purged = [
        i for i in members if i != current_members_dict.get((i["id"], i["guild"]))
    ]
    users_purged = [i for i in users if i != current_users_dict.get(i["id"])]
    roles_purged = [i for i in roles if i != current_roles_dict.get(i["id"])]
    channels_purged = [i for i in channels if i != current_channels_dict.get(i["id"])]
    await asyncio.gather(
        *[
            execute_query_many(query, data)  # type: ignore
            for query, data in zip(
                queries,
                [
                    [tuple(i.values()) for i in guilds_purged],
                    [tuple(i.values()) for i in members_purged],
                    [tuple(i.values()) for i in users_purged],
                    [tuple(i.values()) for i in roles_purged],
                    [tuple(i.values()) for i in channels_purged],
                ],
            )
        ]
    )
