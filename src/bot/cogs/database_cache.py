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
        await execute_query("DELETE FROM cache_guilds WHERE id = $1;", guild.id)
        await execute_query("DELETE FROM cache_members WHERE guild_id = $1;", guild.id)

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
        await execute_query(
            "INSERT INTO cache_members (id, guild_id, permissions) VALUES ($1, $2, $3) ON CONFLICT (id, guild_id) DO UPDATE SET permissions = $3 WHERE members.id = $1 AND cache_members.guild_id = $2;",
            member.id,
            member.guild.id,
            member.guild_permissions.value,
        )
        user = member._user  # type: ignore
        await execute_query(
            "INSERT INTO cache_users (id, name, discriminator, bot, display_avatar) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO UPDATE SET name = $2, discriminator = $3, display_avatar = $5 WHERE cache_users.id = $1;",
            user.id,
            user.name,
            int(user.discriminator),
            user.bot,
            user.display_avatar.url,
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await execute_query(
            "DELETE FROM cache_members WHERE id = $1 AND guild_id = $2;",
            member.id,
            member.guild.id,
        )

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.guild_permissions.value != after.guild_permissions.value:
            await execute_query(
                "INSERT INTO cache_members (id, guild_id, permissions) VALUES ($1, $2, $3) ON CONFLICT (id, guild_id) DO UPDATE SET permissions = $3 WHERE members.id = $1 AND cache_members.guild_id = $2;",
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
                "INSERT INTO cache_users (id, name, discriminator, display_avatar) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO UPDATE SET name = $2, discriminator = $3, display_avatar = $4 WHERE cache_users.id = $1;",
                after.id,
                after.name,
                int(after.discriminator),
                after.display_avatar.url,
            )


def setup(bot: Rift):
    bot.add_cog(DatabaseCache(bot))
