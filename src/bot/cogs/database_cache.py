from __future__ import annotations

import discord
from discord.ext import commands

from ... import funcs
from ...data.db import execute_query
from ...ref import Rift


class DatabaseCache(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await funcs.fill_database_cache()
        print("Database cache filled!", flush=True)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await execute_query(
            "INSERT INTO cache_guilds (id, name, icon_url, owner_id) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO UPDATE SET name = $2, icon_url = $3, owner_id = $4 WHERE cache_guilds.id = $1;",
            guild.id,
            guild.name,
            guild.icon and guild.icon.url,
            guild.owner_id,
        )
        if not guild.chunked:
            await guild.chunk()
        for member in guild.members:
            await self.on_member_join(member)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await execute_query("DELETE FROM cache_roles WHERE guild = $1;", guild.id)
        await execute_query("DELETE FROM cache_channels WHERE guild = $1;", guild.id)
        await execute_query("DELETE FROM cache_members WHERE guild = $1;", guild.id)
        await execute_query("DELETE FROM cache_guilds WHERE id = $1;", guild.id)

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if (
            before.name != after.name
            or before.icon != after.icon
            or before.owner_id != after.owner_id
        ):
            await execute_query(
                "INSERT INTO cache_guilds (id, name, icon_url, owner_id) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO UPDATE SET name = $2, icon_url = $3, owner_id = $4 WHERE cache_guilds.id = $1;",
                after.id,
                after.name,
                after.icon and after.icon.url,
                after.owner_id,
            )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        user = member._user  # type: ignore
        await execute_query(
            "INSERT INTO cache_users (id, name, discriminator, bot, display_avatar_url) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO UPDATE SET name = $2, discriminator = $3, display_avatar_url = $5 WHERE cache_users.id = $1;",
            user.id,
            user.name,
            user.discriminator,
            user.bot,
            user.display_avatar.url,
        )
        await execute_query(
            "INSERT INTO cache_members (id, guild, permissions) VALUES ($1, $2, $3) ON CONFLICT (id, guild) DO UPDATE SET permissions = $3 WHERE cache_members.id = $1 AND cache_members.guild = $2;",
            member.id,
            member.guild.id,
            member.guild_permissions.value,
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await execute_query(
            "DELETE FROM cache_members WHERE id = $1 AND guild = $2;",
            member.id,
            member.guild.id,
        )

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.guild_permissions.value != after.guild_permissions.value:
            await execute_query(
                "INSERT INTO cache_members (id, guild, permissions) VALUES ($1, $2, $3) ON CONFLICT (id, guild) DO UPDATE SET permissions = $3 WHERE cache_members.id = $1 AND cache_members.guild = $2;",
                after.id,
                after.guild.id,
                after.guild_permissions.value,
            )

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if (
            before.name != after.name
            or before.discriminator != after.discriminator
            or before.bot != after.bot
            or before.display_avatar != after.display_avatar
        ):
            await execute_query(
                "INSERT INTO cache_users (id, name, discriminator, display_avatar_url) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO UPDATE SET name = $2, discriminator = $3, display_avatar_url = $4 WHERE cache_users.id = $1;",
                after.id,
                after.name,
                after.discriminator,
                after.display_avatar.url,
            )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        await execute_query(
            "INSERT INTO cache_channels (id, category, guild, name, overwrites, permissions_synced, position, type) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (id) DO UPDATE SET category = $2, guild = $3, name = $4, overwrites = $5, permissions_synced = $6, position = $7, type = $8 WHERE cache_channels.id = $1;",
            channel.id,
            channel.category_id,
            channel.guild.id,
            channel.name,
            {
                key.id: value._values  # type: ignore
                for key, value in channel.overwrites.items()
                if not value.is_empty()
            },
            channel.permissions_synced,
            channel.position,
            channel.type.value,
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        await execute_query("DELETE FROM cache_channels WHERE id = $1;", channel.id)

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel
    ):
        before_overwrites = {
            key.id: value._values  # type: ignore
            for key, value in before.overwrites.items()
            if not value.is_empty()
        }
        after_overwrites = {
            key.id: value._values  # type: ignore
            for key, value in after.overwrites.items()
            if not value.is_empty()
        }
        if (
            before.category_id != after.category_id
            or before.name != after.name
            or before_overwrites != after_overwrites
            or before.permissions_synced != after.permissions_synced
            or before.position != after.position
            or before.type != after.type
        ):
            await execute_query(
                "INSERT INTO cache_channels (id, category, guild, name, overwrites, permissions_synced, position, type) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (id) DO UPDATE SET category = $2, guild = $3, name = $4, overwrites = $5, permissions_synced = $6, position = $7, type = $8 WHERE cache_channels.id = $1;",
                after.id,
                after.category_id,
                after.guild.id,
                after.name,
                after_overwrites,
                after.permissions_synced,
                after.position,
                after.type.value,
            )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        await execute_query(
            "INSERT INTO cache_roles (id, name, guild, color, members, permissions, position, tags) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (id) DO UPDATE SET name = $2, guild = $3, color = $4, members = $5, permissions = $6, position = $7, tags = $8 WHERE cache_roles.id = $1;",
            role.id,
            role.name,
            role.guild.id,
            role.color.value,
            [i.id for i in role.members],
            role.permissions.value,
            role.position,
            {
                "is_bot_managed": role.tags.is_bot_managed() if role.tags else False,
                "is_premium_subscriber": role.tags.is_premium_subscriber()
                if role.tags
                else False,
                "is_integration": role.tags.is_integration() if role.tags else False,
            },
        )

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        await execute_query("DELETE FROM cache_roles WHERE id = $1;", role.id)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        before_tags = {
            "is_bot_managed": before.tags.is_bot_managed() if before.tags else False,
            "is_premium_subscriber": before.tags.is_premium_subscriber()
            if before.tags
            else False,
            "is_integration": before.tags.is_integration() if before.tags else False,
        }
        after_tags = {
            "is_bot_managed": after.tags.is_bot_managed() if after.tags else False,
            "is_premium_subscriber": after.tags.is_premium_subscriber()
            if after.tags
            else False,
            "is_integration": after.tags.is_integration() if after.tags else False,
        }
        if (
            before.name != after.name
            or before.color.value != after.color.value
            or {i.id for i in before.members} != {i.id for i in after.members}
            or before.permissions.value != after.permissions.value
            or before.position != after.position
            or before_tags != after_tags
        ):
            await execute_query(
                "INSERT INTO cache_roles (id, name, guild, color, members, permissions, position, tags) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (id) DO UPDATE SET name = $2, guild = $3, color = $4, members = $5, permissions = $6, position = $7, tags = $8 WHERE cache_roles.id = $1;",
                after.id,
                after.name,
                after.guild.id,
                after.color.value,
                [i.id for i in after.members],
                after.permissions.value,
                after.position,
                {
                    "is_bot_managed": after.tags.is_bot_managed()
                    if after.tags
                    else False,
                    "is_premium_subscriber": after.tags.is_premium_subscriber()
                    if after.tags
                    else False,
                    "is_integration": after.tags.is_integration()
                    if after.tags
                    else False,
                },
            )


def setup(bot: Rift):
    bot.add_cog(DatabaseCache(bot))
