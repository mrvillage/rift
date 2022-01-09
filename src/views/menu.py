from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

import discord

from ..cache import cache
from ..ref import Rift

if TYPE_CHECKING:
    from ..data.classes import Embassy, Ticket


class MenuView(discord.ui.View):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.menu_id: int = kwargs.pop("menu_id")
        self.bot: Rift = kwargs.pop("bot")
        super().__init__(*args, **kwargs)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if TYPE_CHECKING:
            assert isinstance(interaction.message, discord.Message)
        return bool(
            [
                i
                for i in cache.menu_interfaces
                if i.menu_id == self.menu_id and i.message_id == interaction.message.id
            ]
        )


class MenuButton(discord.ui.Button):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.action: str = kwargs.pop("action")
        self.options: List[int] = kwargs.pop("options")
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: discord.Interaction) -> None:
        # sourcery no-metrics
        from ..data.classes import EmbassyConfig, TicketConfig
        from ..funcs import get_embed_author_member

        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)
            assert isinstance(interaction.guild, discord.Guild)
        bot_member = interaction.guild.get_member(interaction.application_id)
        if TYPE_CHECKING:
            assert isinstance(bot_member, discord.Member)
        highest_role = bot_member.top_role
        if self.action is None:
            return await interaction.response.defer()
        if self.action in {"ADD_ROLE", "ADD_ROLES"}:
            roles: List[discord.Role] = []
            for role in self.options:
                role = interaction.guild.get_role(role)
                if role is None:
                    continue
                if role < highest_role and role not in interaction.user.roles:
                    roles.append(role)
            if roles:
                await interaction.user.add_roles(*roles)
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Added the following roles: {', '.join(role.mention for role in roles)}",
                        color=discord.Color.green(),
                    ),
                )
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No roles were added since you have them all already.",
                        color=discord.Color.green(),
                    ),
                )
        elif self.action in {"REMOVE_ROLE", "REMOVE_ROLES"}:
            roles = []
            for role in self.options:
                role = interaction.guild.get_role(role)
                if role is None:
                    continue
                if role < highest_role and role not in interaction.user.roles:
                    roles.append(role)
            if roles:
                await interaction.user.remove_roles(*roles)
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Removed the following roles from you: {', '.join(role.mention for role in roles)}",
                        color=discord.Color.green(),
                    ),
                )
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No roles were removed since you you don't have any of them.",
                        color=discord.Color.green(),
                    ),
                )
        elif self.action in {"TOGGLE_ROLE", "TOGGLE_ROLES"}:
            add_roles: List[discord.Role] = []
            remove_roles: List[discord.Role] = []
            for role in self.options:
                role = interaction.guild.get_role(role)
                if role is None:
                    continue
                if role < highest_role and role not in interaction.user.roles:
                    add_roles.append(role)
                elif role < highest_role:
                    remove_roles.append(role)
            if add_roles:
                await interaction.user.add_roles(*add_roles)
            if remove_roles:
                await interaction.user.remove_roles(*remove_roles)
            if add_roles or remove_roles:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Toggled the following roles: {', '.join(role.mention for role in add_roles + remove_roles)}",
                        color=discord.Color.green(),
                    ),
                )
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No roles were toggled since you have them all already.",
                        color=discord.Color.green(),
                    ),
                )
        elif self.action in {"CREATE_TICKET", "CREATE_TICKETS"}:
            await interaction.response.defer()
            configs = [await TicketConfig.fetch(opt) for opt in self.options]
            tickets: List[Ticket] = []
            for config in configs:
                if config.guild_id != interaction.guild.id:
                    continue
                ticket = await config.create(interaction.user)
                await ticket.start(interaction.user, config)
                tickets.append(ticket)
            if len(tickets) > 1:
                tickets_str = "\n".join(f"<#{ticket.id}" for ticket in tickets)
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Tickets Created!\n{tickets_str}",
                        color=discord.Color.green(),
                    ),
                )
            else:
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Ticket Created!\n<#{tickets[0].id}>",
                        color=discord.Color.green(),
                    ),
                )
        elif self.action in {"CLOSE_TICKET", "CREATE_TICKETS"}:
            ...
        elif self.action in {"CREATE_EMBASSY", "CREATE_EMBASSIES"}:
            await interaction.response.defer()
            configs = [await EmbassyConfig.fetch(opt) for opt in self.options]
            embassies: List[Embassy] = []
            link = cache.get_user(interaction.user.id)
            if link is None:
                return await interaction.followup.send(
                    embed=get_embed_author_member(
                        interaction.user,
                        "You must be linked to create an embassy.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            nation = cache.get_nation(link.nation_id)
            if nation is None:
                return await interaction.followup.send(
                    embed=get_embed_author_member(
                        interaction.user,
                        "You must be linked to create an embassy.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            alliance = nation.alliance
            if alliance is None:
                return await interaction.followup.send(
                    embed=get_embed_author_member(
                        interaction.user,
                        "You must be in an alliance to create an embassy.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            if nation.alliance_position < 3:
                return await interaction.followup.send(
                    embed=get_embed_author_member(
                        interaction.user,
                        "You must be an Officer or higher to create an embassy.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            for config in configs:
                if config.guild_id != interaction.guild.id:
                    continue
                embassy, start = await config.create_embassy(interaction.user, alliance)
                if start:
                    await embassy.start(interaction.user, config)
                embassies.append(embassy)
            if len(embassies) > 1:
                embassies_str = "\n".join(f"<#{embassy.id}" for embassy in embassies)
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Embassies:\n{embassies_str}",
                        color=discord.Color.green(),
                    ),
                )
            elif len(embassies) == 0:
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No embassies were created.",
                        color=discord.Color.green(),
                    ),
                )
            else:
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Embassy:\n<#{embassies[0].id}>",
                        color=discord.Color.green(),
                    ),
                )
        elif self.action in {"CLOSE_EMBASSY", "CLOSE_EMBASSIES"}:
            ...


class MenuSelect(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction) -> None:
        values = self.values.copy()  # type: ignore


class MenuSelectOption(discord.SelectOption):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.action: str = kwargs.pop("action")
        self.options: List[int] = kwargs.pop("options")
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"Label: {self.label} - Description: {self.description} - Emoji: {self.emoji} - Default: {self.default} - Action: {self.action}"  # type: ignore
