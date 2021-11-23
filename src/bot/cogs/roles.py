from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, List, Optional, Tuple, Union

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...checks import can_manage_alliance_roles
from ...data.classes import Alliance, Nation, Role
from ...flags import Flags
from ...ref import Rift, RiftContext
from ...views import PermissionsSelector

if TYPE_CHECKING:
    from _typings import Permission

ROLE_PERMISSIONS: List[Permission] = [
    {
        "name": "Manage Roles",
        "description": "Allows the role to manage roles.",
        "value": "manage_roles",
        "flag": 1 << 0,
    },
    {
        "name": "Leadership",
        "description": "Grants the role all permissions and designates it as part of alliance leadership.",
        "value": "leadership",
        "flag": 1 << 1,
    },
    {
        "name": "View Alliance Bank",
        "description": "Allows the role to view the alliance bank.",
        "value": "view_alliance_bank",
        "flag": 1 << 2,
    },
    {
        "name": "Send Alliance Bank",
        "description": "Allows the role to send money from the alliance bank.",
        "value": "send_alliance_bank",
        "flag": 1 << 3,
    },
    {
        "name": "View Nation Banks",
        "description": "Allows the role to view alliance member banks.",
        "value": "view_nation_banks",
        "flag": 1 << 4,
    },
    {
        "name": "View Nation Spies",
        "description": "Allows the role to view nation spies.",
        "value": "view_nation_spies",
        "flag": 1 << 5,
    },
    {
        "name": "View Offshores",
        "description": "Allows the role to view offshore information.",
        "value": "view_offshores",
        "flag": 1 << 6,
    },
    {
        "name": "Send Offshore Banks",
        "description": "Allows the role to send money from the offshore banks.",
        "value": "send_offshore_banks",
        "flag": 1 << 7,
    },
    {
        "name": "Manage Offshores",
        "description": "Allows the role to manage offshore information and settings.",
        "value": "manage_offshores",
        "flag": 1 << 8,
    },
    {
        "name": "View Nation Safekeeping",
        "description": "Allows the role to view nation safekeeping.",
        "value": "view_nation_safekeeping",
        "flag": 1 << 9,
    },
    {
        "name": "Send Nation Safekeeping",
        "description": "Allows the role to send nation safekeeping in response to withdrawal requests.",
        "value": "send_nation_safekeeping",
        "flag": 1 << 10,
    },
    {
        "name": "Manage Nation Safekeeping",
        "description": "Allows the role to manage nation safekeeping (arbitrary add/remove).",
        "value": "manage_nation_safekeeping",
        "flag": 1 << 11,
    },
    {
        "name": "Approve Grants",
        "description": "Allows the role to approve nation grants.",
        "value": "approve_grants",
        "flag": 1 << 12,
    },
    {
        "name": "Manage Grants",
        "description": "Allows the role to manage nation grant information and settings.",
        "value": "manage_grants",
        "flag": 1 << 13,
    },
    {
        "name": "Manage Alliance Taxes",
        "description": "Allows the role to manage alliance taxes.",
        "value": "manage_alliance_taxes",
        "flag": 1 << 14,
    },
    {
        "name": "Manage Alliance Positions",
        "description": "Allows the role to manage in-game alliance positions.",
        "value": "manage_alliance_positions",
        "flag": 1 << 15,
    },
    {
        "name": "Manage Treaties",
        "description": "Allows the role to manage alliance treaties.",
        "value": "manage_treaties",
        "flag": 1 << 16,
    },
    {
        "name": "Create Alliance Announcements",
        "description": "Allows the role to create alliance announcements.",
        "value": "create_alliance_announcements",
        "flag": 1 << 17,
    },
    {
        "name": "Delete Alliance Announcements",
        "description": "Allows the role to delete alliance announcements.",
        "value": "delete_alliance_announcements",
        "flag": 1 << 18,
    },
]


def save_role_permissions(role: Role) -> Callable[[Flags], Coroutine[Any, Any, None]]:
    async def save(flags: Flags) -> None:
        await role.save()

    return save


async def manage_roles_command_check(
    ctx: RiftContext, alliance: Optional[Alliance] = None
) -> Tuple[Nation, Optional[Alliance], bool]:
    nation = await Nation.convert(ctx, None)
    if alliance is None:
        alliance = nation.alliance
    if alliance is None:
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "You're not in an alliance and didn't specify one so I don't know where to manage! Please try again with an alliance.",
                color=discord.Color.red(),
            ),
            ephemeral=True,
        )
        return nation, alliance, False
    if not await can_manage_alliance_roles(nation, alliance):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"You don't have permission to manage roles for {repr(alliance)}!",
                color=discord.Color.red(),
            ),
            ephemeral=True,
        )
        return nation, alliance, False
    return nation, alliance, True


class Roles(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="roles",
        brief="Manage alliance roles.",
        type=commands.CommandType.chat_input,
    )
    async def roles(self, ctx: RiftContext):
        ...

    @roles.command(  # type: ignore
        name="create",
        brief="Create an alliance role.",
        type=commands.CommandType.chat_input,
    )
    async def roles_create(
        self,
        ctx: RiftContext,
        name: str,
        rank: int,
        starting_members: List[discord.Member] = [],
        description: Optional[str] = None,
        alliance: Optional[Alliance] = None,
    ):
        _, alliance, can = await manage_roles_command_check(ctx, alliance)
        if not can or alliance is None:
            return
        role = Role.create(name, description, alliance, rank, starting_members)
        view = PermissionsSelector(
            ctx.author.id,
            save_role_permissions(role),
            role.permissions,
            ROLE_PERMISSIONS,
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "Please select the permissions you want for the new role.",
                color=discord.Color.blue(),
            ),
            view=view,
            ephemeral=True,
        )
        if await view.wait():
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author, "Role creation timed out."
                ),
                view=None,
            )
        enabled_permissions = ", ".join(
            f"`{i['name']}`"
            for i in ROLE_PERMISSIONS
            if getattr(role.permissions, i["value"])
        )
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Role created!\n\nID: {role.id}\nName: {role.name}\nRank: {role.rank:,}\nAlliance: {repr(role.alliance)}\nMembers: {' '.join(i.mention for i in starting_members) or 'None'}\nDescription: {role.description}\nPermissions: {enabled_permissions}",
                color=discord.Color.green(),
            ),
            view=None,
        )

    @roles.command(  # type: ignore
        name="delete",
        brief="Delete an alliance role.",
        type=commands.CommandType.chat_input,
    )
    async def roles_delete(self, ctx: RiftContext, role: Role):
        if role.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This role doesn't belong to an alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        _, alliance, can = await manage_roles_command_check(ctx, role.alliance)
        if not can or alliance is None:
            return
        await role.delete()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Role `{role.name}` of alliance {repr(alliance)} deleted.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @roles.command(  # type: ignore
        name="list",
        brief="List alliance roles.",
        type=commands.CommandType.chat_input,
    )
    async def roles_list(self, ctx: RiftContext, alliance: Optional[Alliance] = None):
        _, alliance, can = await manage_roles_command_check(ctx, alliance)
        if not can or alliance is None:
            return
        roles = [i for i in cache.roles if i.alliance_id == alliance.id]
        if roles:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "\n".join(f"#{i.rank} - {i.id} - {i.name}" for i in roles),
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "There are no roles for that alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

    @roles.command(  # type: ignore
        name="info",
        brief="Get information about an alliance role.",
        type=commands.CommandType.chat_input,
    )
    async def roles_info(self, ctx: RiftContext, role: Role):
        if role.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This role doesn't belong to an alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        _, alliance, can = await manage_roles_command_check(ctx, role.alliance)
        if not can or alliance is None:
            return
        enabled_permissions = ", ".join(
            f"`{i['name']}`"
            for i in ROLE_PERMISSIONS
            if getattr(role.permissions, i["value"])
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"ID: {role.id}\nName: {role.name}\nRank: {role.rank:,}\nAlliance: {repr(role.alliance)}\nMembers: {' '.join(f'<@{i}>' for i in role.member_ids) or 'None'}\nDescription: {role.description}\nPermissions: {enabled_permissions}",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @roles.command(  # type: ignore
        name="edit",
        brief="Edit an alliance role.",
        type=commands.CommandType.chat_input,
    )
    async def roles_edit(
        self,
        ctx: RiftContext,
        role: Role,
        name: str = MISSING,
        rank: int = MISSING,
        description: str = MISSING,
    ):
        if role.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This role doesn't belong to an alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        _, alliance, can = await manage_roles_command_check(ctx, role.alliance)
        if not can or alliance is None:
            return
        if name is not MISSING:
            role.name = name
        if rank is not MISSING:
            role.rank = rank
        if description is not MISSING:
            role.description = description
        view = PermissionsSelector(
            ctx.author.id,
            save_role_permissions(role),
            role.permissions,
            ROLE_PERMISSIONS,
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "Please select the permissions you want for the role.",
                color=discord.Color.blue(),
            ),
            view=view,
            ephemeral=True,
        )
        if await view.wait():
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author, "Role editing timed out."
                ),
                view=None,
            )
        enabled_permissions = ", ".join(
            f"`{i['name']}`"
            for i in ROLE_PERMISSIONS
            if getattr(role.permissions, i["value"])
        )
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Role edited!\n\nID: {role.id}\nName: {role.name}\nRank: {role.rank:,}\nAlliance: {repr(role.alliance)}\nMembers: {' '.join(i.mention for i in role.members) or 'None'}\nDescription: {role.description}\nPermissions: {enabled_permissions}",
                color=discord.Color.green(),
            ),
            view=None,
        )

    @roles.command(  # type: ignore
        name="add-member",
        brief="Add a new member to an alliance role.",
        type=commands.CommandType.chat_input,
    )
    async def roles_add_member(
        self, ctx: RiftContext, role: Role, member: Union[discord.Member, discord.User]
    ):
        if role.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This role doesn't belong to an alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        _, alliance, can = await manage_roles_command_check(ctx, role.alliance)
        if not can or alliance is None:
            return
        if member.id in role.member_ids:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{member.mention} is already a member of this role!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        role.member_ids.append(member.id)
        await role.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{member.mention} has been added to this role!",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @roles.command(  # type: ignore
        name="remove-member",
        brief="Removes a member from an alliance role.",
        type=commands.CommandType.chat_input,
    )
    async def roles_remove_member(
        self, ctx: RiftContext, role: Role, member: Union[discord.Member, discord.User]
    ):
        if role.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This role doesn't belong to an alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        _, alliance, can = await manage_roles_command_check(ctx, role.alliance)
        if not can or alliance is None:
            return
        if member.id not in role.member_ids:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{member.mention} is not a member of this role!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        role.member_ids.remove(member.id)
        await role.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{member.mention} has been removed from this role!",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )


def setup(bot: Rift):
    bot.add_cog(Roles(bot))
