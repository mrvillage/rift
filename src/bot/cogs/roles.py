from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
)

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...checks import can_manage_alliance_roles
from ...data.classes import Alliance, Nation, Role
from ...enums import PrivacyLevel
from ...errors import RoleNotFoundError
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
        "name": "Create Bank Accounts",
        "description": "Allows the role to create bank accounts.",
        "value": "create_bank_accounts",
        "flag": 1 << 9,
    },
    {
        "name": "View Bank Accounts",
        "description": "Allows the role to view bank accounts.",
        "value": "view_bank_accounts",
        "flag": 1 << 10,
    },
    {
        "name": "Manage Bank Accounts",
        "description": "Allows the role to manage bank accounts.",
        "value": "manage_bank_accounts",
        "flag": 1 << 11,
    },
    {
        "name": "View Grants",
        "description": "Allows the role to view grants.",
        "value": "view_grants",
        "flag": 1 << 12,
    },
    {
        "name": "Request Grants",
        "description": "Allows the role to request grants.",
        "value": "request_grants",
        "flag": 1 << 13,
    },
    {
        "name": "Approve Grants",
        "description": "Allows the role to approve nation grants.",
        "value": "approve_grants",
        "flag": 1 << 14,
    },
    {
        "name": "Manage Grants",
        "description": "Allows the role to manage nation grant information and settings.",
        "value": "manage_grants",
        "flag": 1 << 15,
    },
    {
        "name": "Manage Alliance Taxes",
        "description": "Allows the role to manage alliance taxes.",
        "value": "manage_alliance_taxes",
        "flag": 1 << 16,
    },
    # {
    #     "name": "Manage Alliance Positions",
    #     "description": "Allows the role to manage in-game alliance positions.",
    #     "value": "manage_alliance_positions",
    #     "flag": 1 << 17,
    # },
    # {
    #     "name": "Manage Treaties",
    #     "description": "Allows the role to manage alliance treaties.",
    #     "value": "manage_treaties",
    #     "flag": 1 << 18,
    # },
    # {
    #     "name": "Create Alliance Announcements",
    #     "description": "Allows the role to create alliance announcements.",
    #     "value": "create_alliance_announcements",
    #     "flag": 1 << 19,
    # },
    # {
    #     "name": "Delete Alliance Announcements",
    #     "description": "Allows the role to delete alliance announcements.",
    #     "value": "delete_alliance_announcements",
    #     "flag": 1 << 20,
    # },
]


def save_role_permissions(role: Role) -> Callable[[Flags], Coroutine[Any, Any, None]]:
    async def save(flags: Flags) -> None:
        await role.save()

    return save


async def manage_roles_command_check_with_message(
    ctx: RiftContext, alliance: Optional[Alliance] = None
) -> Tuple[Nation, Optional[Alliance], bool]:
    nation, alliance, can = await manage_roles_command_check(ctx, alliance)
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
    if not can:
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


async def manage_roles_command_check(
    ctx: RiftContext, alliance: Optional[Alliance] = None, suppress: bool = False
) -> Tuple[Nation, Optional[Alliance], bool]:
    nation = await Nation.convert(ctx, None)
    if alliance is None:
        alliance = nation.alliance
    if alliance is None:
        return nation, alliance, False
    if not await can_manage_alliance_roles(nation, alliance, suppress):
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
        descriptions={
            "name": "The name of the role.",
            "rank": "The rank of the role.",
            "starting_members": "A space separated list of members to initially give the role.",
            "description": "The description of the role.",
            "alliance": "The alliance to create the role in.",
            "privacy_level": "The privacy level of the role.",
        },
    )
    async def roles_create(
        self,
        ctx: RiftContext,
        name: str,
        rank: int,
        starting_members: List[discord.Member] = [],
        description: Optional[str] = None,
        alliance: Optional[Alliance] = None,
        privacy_level: Literal["PUBLIC", "PRIVATE", "PROTECTED"] = "PUBLIC",
    ):
        nation, alliance, can = await manage_roles_command_check_with_message(
            ctx, alliance
        )
        if not can or alliance is None:
            return
        role = Role.create(
            name,
            description,
            alliance,
            rank,
            starting_members,
            getattr(PrivacyLevel, privacy_level),
        )
        roles = [
            i
            for i in cache.roles
            if i.alliance_id == alliance.id and ctx.author.id in i.member_ids
        ]
        max_rank = max(i.rank for i in roles) if roles else 0
        leadership = any(i.permissions.leadership for i in roles) or (
            nation.alliance_id == alliance.id
            and nation.alliance_position in {"Heir", "Leader"}
        )
        if rank >= max_rank and not leadership:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You can't create a role with a rank higher than the highest rank you have!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        view = PermissionsSelector(
            ctx.author.id,
            save_role_permissions(role),
            role.permissions,
            [
                i
                for i in ROLE_PERMISSIONS
                if leadership or any(getattr(r.permissions, i["value"]) for r in roles)
            ],
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Please select the permissions you want for the new role for alliance {repr(alliance)}.",
                color=discord.Color.blue(),
            ),
            view=view,
            ephemeral=True,
        )
        if await view.wait():
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Role creation timed out.",
                    color=discord.Color.red(),
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
                f"Role created!\n\nID: {role.id}\nName: {role.name}\nRank: {role.rank:,}\nAlliance: {repr(role.alliance)}\nMembers: {' '.join(i.mention for i in starting_members) or 'None'}\nDescription: {role.description}\nPermissions: {enabled_permissions}\nPrivacy Level: `{role.privacy_level.name}`",
                color=discord.Color.green(),
            ),
            view=None,
        )

    @roles.command(  # type: ignore
        name="delete",
        brief="Delete an alliance role.",
        type=commands.CommandType.chat_input,
        descriptions={
            "role": "The role to delete.",
        },
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
        _, alliance, can = await manage_roles_command_check_with_message(
            ctx, role.alliance
        )
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
        descriptions={
            "alliance": "The alliance to list roles for.",
        },
    )
    async def roles_list(self, ctx: RiftContext, alliance: Optional[Alliance] = None):
        nation, alliance, can = await manage_roles_command_check(ctx, alliance, True)
        if alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance and didn't specify one so I don't know where to look! Please try again with an alliance.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if can:
            privacy_levels = {
                PrivacyLevel.PUBLIC,
                PrivacyLevel.PRIVATE,
                PrivacyLevel.PROTECTED,
            }
        elif nation.alliance_id == alliance.id:
            privacy_levels = {PrivacyLevel.PUBLIC, PrivacyLevel.PRIVATE}
        else:
            privacy_levels = {PrivacyLevel.PUBLIC}
        roles = [
            i
            for i in cache.roles
            if i.alliance_id == alliance.id and i.privacy_level in privacy_levels
        ]
        if roles:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Privacy Level: `{max(privacy_levels, key=lambda x: x.value).name}`\n\n"
                    + "\n".join(f"#{i.rank} - {i.id} - {i.name}" for i in roles),
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You can't view any roles for that alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

    @roles.command(  # type: ignore
        name="info",
        brief="Get information about an alliance role.",
        type=commands.CommandType.chat_input,
        descriptions={
            "role": "The role to get information about.",
        },
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
        nation, alliance, can = await manage_roles_command_check(
            ctx, role.alliance, True
        )
        if alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance and didn't specify one so I don't know where to look! Please try again with an alliance.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if can:
            privacy_levels = {
                PrivacyLevel.PUBLIC,
                PrivacyLevel.PRIVATE,
                PrivacyLevel.PROTECTED,
            }
        elif nation.alliance_id == alliance.id:
            privacy_levels = {PrivacyLevel.PUBLIC, PrivacyLevel.PRIVATE}
        else:
            privacy_levels = {PrivacyLevel.PUBLIC}
        if role.privacy_level not in privacy_levels:
            raise RoleNotFoundError(
                [i for i in ctx.options if i["name"] == "role"][0]["value"]  # type: ignore
            )
        enabled_permissions = ", ".join(
            f"`{i['name']}`"
            for i in ROLE_PERMISSIONS
            if getattr(role.permissions, i["value"])
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"ID: {role.id}\nName: {role.name}\nRank: {role.rank:,}\nAlliance: {repr(role.alliance)}\nMembers: {' '.join(f'<@{i}>' for i in role.member_ids) or 'None'}\nDescription: {role.description}\nPermissions: {enabled_permissions}\nPrivacy Level: `{role.privacy_level.name}`",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @roles.command(  # type: ignore
        name="edit",
        brief="Edit an alliance role.",
        type=commands.CommandType.chat_input,
        descriptions={
            "role": "The role to edit.",
            "name": "The new name of the role.",
            "rank": "The new rank of the role.",
            "description": "The new description of the role.",
            "privacy_level": "The new privacy level of the role.",
        },
    )
    async def roles_edit(
        self,
        ctx: RiftContext,
        role: Role,
        name: str = MISSING,
        rank: int = MISSING,
        description: str = MISSING,
        privacy_level: Literal["PUBLIC", "PRIVATE", "PROTECTED"] = MISSING,
    ):  # sourcery no-metrics
        if (
            name is MISSING
            and rank is MISSING
            and description is MISSING
            and privacy_level is MISSING
        ):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You must specify at least one field to edit!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if role.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This role doesn't belong to an alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        nation, alliance, can = await manage_roles_command_check_with_message(
            ctx, role.alliance
        )
        if not can or alliance is None:
            return
        roles = [
            i
            for i in cache.roles
            if i.alliance_id == alliance.id and ctx.author.id in i.member_ids
        ]
        leadership = any(i.permissions.leadership for i in roles) or (
            nation.alliance_id == alliance.id
            and nation.alliance_position in {"Heir", "Leader"}
        )
        max_rank = max(i.rank for i in roles)
        if rank >= max_rank and not leadership:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You can't edit a role to have a rank higher than the highest rank you have!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if role.rank >= max_rank and not leadership:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You can't edit a role with a higher rank than the highest rank you have!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if name is not MISSING:
            role.name = name
        if rank is not MISSING:
            role.rank = rank
        if description is not MISSING:
            role.description = description
        if privacy_level is not MISSING:
            role.privacy_level = getattr(PrivacyLevel, privacy_level)
        view = PermissionsSelector(
            ctx.author.id,
            save_role_permissions(role),
            role.permissions,
            [
                i
                for i in ROLE_PERMISSIONS
                if leadership or any(getattr(r.permissions, i["value"]) for r in roles)
            ],
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
                f"Role edited!\n\nID: {role.id}\nName: {role.name}\nRank: {role.rank:,}\nAlliance: {repr(role.alliance)}\nMembers: {' '.join(i.mention for i in role.members) or 'None'}\nDescription: {role.description}\nPermissions: {enabled_permissions}\nPrivacy Level: `{role.privacy_level.name}`",
                color=discord.Color.green(),
            ),
            view=None,
        )

    @roles.command(  # type: ignore
        name="add-member",
        brief="Add a new member to an alliance role.",
        type=commands.CommandType.chat_input,
        descriptions={
            "role": "The role to add.",
            "member": "The member to add to the role.",
        },
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
        nation, alliance, can = await manage_roles_command_check_with_message(
            ctx, role.alliance
        )
        if not can or alliance is None:
            return
        if (
            nation.alliance_position in {"Heir", "Leader"}
            and nation.alliance_id != alliance.id
        ) or nation.alliance_position not in {"Heir", "Leader"}:
            roles = [
                i
                for i in cache.roles
                if i.alliance_id == alliance.id
                and (i.permissions.manage_roles or i.permissions.leadership)
                and ctx.author.id in i.member_ids
            ]
            if not roles:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "You don't have permission to add members to this role!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            max_rank = max(i.rank for i in roles)
            leadership = any(i.permissions.leadership for i in roles) or (
                nation.alliance_id == alliance.id
                and nation.alliance_position in {"Heir", "Leader"}
            )
            if role.rank >= max_rank and not leadership:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "You don't have permission to add members to this role!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
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
        descriptions={
            "role": "The role to remove.",
            "member": "The member to remove from the role.",
        },
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
        nation, alliance, can = await manage_roles_command_check_with_message(
            ctx, role.alliance
        )
        if not can or alliance is None:
            return
        if (
            nation.alliance_position in {"Heir", "Leader"}
            and nation.alliance_id != alliance.id
        ) or nation.alliance_position not in {"Heir", "Leader"}:
            roles = [
                i
                for i in cache.roles
                if i.alliance_id == alliance.id
                and (i.permissions.manage_roles or i.permissions.leadership)
                and ctx.author.id in i.member_ids
            ]
            if not roles:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "You don't have permission to add members to this role!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            max_rank = max(i.rank for i in roles)
            leadership = any(i.permissions.leadership for i in roles) or (
                nation.alliance_id == alliance.id
                and nation.alliance_position in {"Heir", "Leader"}
            )
            if role.rank >= max_rank and not leadership:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "You don't have permission to add members to this role!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
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

    @roles.command(  # type: ignore
        name="summary",
        brief="Shows a summary of a users roles in an alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "member": "The member to show the roles of.",
            "alliance": "The alliance to show the member's roles in.",
        },
    )
    async def roles_summary(
        self,
        ctx: RiftContext,
        member: Union[discord.Member, discord.User] = MISSING,
        alliance: Optional[Alliance] = None,
    ):
        member = member or ctx.author
        nation, alliance, can = await manage_roles_command_check(ctx, alliance, True)
        if alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance and didn't specify one so I don't know where to look! Please try again with an alliance.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if can:
            privacy_levels = {
                PrivacyLevel.PUBLIC,
                PrivacyLevel.PRIVATE,
                PrivacyLevel.PROTECTED,
            }
        elif nation.alliance_id == alliance.id:
            privacy_levels = {PrivacyLevel.PUBLIC, PrivacyLevel.PRIVATE}
        else:
            privacy_levels = {PrivacyLevel.PUBLIC}
        roles = {
            i
            for i in cache.roles
            if i.alliance_id == alliance.id
            and i.privacy_level in privacy_levels
            and member.id in i.member_ids
        }
        if not roles:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{member.mention} doesn't have any roles in this alliance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        enabled_permissions = ", ".join(
            f"`{i['name']}`"
            for i in ROLE_PERMISSIONS
            if any(getattr(role.permissions, i["value"]) for role in roles)
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Privacy Level: `{max(privacy_levels, key=lambda x: x.value).name}`\n\nRank: {max(roles, key=lambda x: x.rank).rank:,}\nAlliance: {repr(alliance)}\nRoles: {', '.join(f'{i.id} - {i.name}' for i in roles) or 'None'}\nPermissions: {enabled_permissions}",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )


def setup(bot: Rift):
    bot.add_cog(Roles(bot))
