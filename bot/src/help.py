from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

import discord
from discord.ext import commands

from .env import COLOR, FOOTER

__all__ = ("EmbedHelpCommand",)

if TYPE_CHECKING:
    from _typings import Field, MaybeEmptyEmbed


def add_fields(embed: discord.Embed, fields: List[Field]) -> discord.Embed:
    for field in fields:
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field.get("inline", True),
        )
    return embed


def get_embed_author_member(
    member: Union[discord.Member, discord.User],
    description: MaybeEmptyEmbed[str] = discord.Embed.Empty,
    color: Union[discord.Color, int] = COLOR,
    timestamp: Optional[datetime] = None,
    footer: str = FOOTER,
    title: MaybeEmptyEmbed[str] = discord.Embed.Empty,
    fields: List[Field] = [],
    image_url: MaybeEmptyEmbed[str] = discord.Embed.Empty,
) -> discord.Embed:
    return add_fields(
        discord.Embed(
            color=color,
            description=description,
            timestamp=timestamp or discord.utils.utcnow(),
            title=title,
        )
        .set_footer(text=footer)
        .set_author(
            name=f"{member.name}#{member.discriminator}",
            icon_url=str(member.display_avatar.url),
        )
        .set_image(url=image_url),
        fields,
    )


class EmbedHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command: commands.Command[commands.Cog, Any, Any]):
        return f"{command.qualified_name} {command.signature}"  # type: ignore

    def get_destination(self):  # type: ignore
        return self.context  # type: ignore

    async def filter_commands(self, commands, *, sort=False, key=None):
        """|coro|

        Returns a filtered list of commands and optionally sorts them.

        This takes into account the :attr:`verify_checks` and :attr:`show_hidden`
        attributes.

        Parameters
        ------------
        commands: Iterable[:class:`Command`]
            An iterable of commands that are getting filtered.
        sort: :class:`bool`
            Whether to sort the result.
        key: Optional[Callable[:class:`Command`, Any]]
            An optional key function to pass to :func:`py:sorted` that
            takes a :class:`Command` as its sole parameter. If ``sort`` is
            passed as ``True`` then this will default as the command name.

        Returns
        ---------
        List[:class:`Command`]
            A list of commands that passed the filter.
        """

        if sort and key is None:
            key = lambda c: c.name

        iterator = (
            commands if self.show_hidden else filter(lambda c: not c.hidden, commands)
        )

        if self.verify_checks is False:
            # if we do not need to verify the checks then we can just
            # run it straight through normally without using await.
            return sorted(iterator, key=key) if sort else list(iterator)

        if self.verify_checks is None and not self.context.guild:
            # if verify_checks is None and we're in a DM, don't verify
            return sorted(iterator, key=key) if sort else list(iterator)

        # if we're here then we need to check every command if it can run
        async def predicate(cmd):
            try:
                return await cmd.can_run(self.context)
            except Exception:
                return False

        ret = []
        for cmd in iterator:
            valid = await predicate(cmd)
            if valid:
                ret.append(cmd)

        if sort:
            ret.sort(key=key)
        return ret

    async def send_bot_help(self, mapping):  # type: ignore
        embed = get_embed_author_member(
            self.context.author, "Rift uses slash commands, meaning the prefix is `/`. Try them out by typing `/`!", title="Bot Commands", color=discord.Color.blue()  # type: ignore
        )
        description = self.context.bot.description  # type: ignore
        if description:
            embed.description = description

        for cog, commands in mapping.items():  # type: ignore
            name = "No Category" if cog is None else cog.qualified_name  # type: ignore
            filtered = await self.filter_commands(commands, sort=True)  # type: ignore
            if filtered:
                value = "\u2002".join(c.name for c in commands)  # type: ignore
                if cog and cog.description:  # type: ignore
                    value = "{0}\n{1}".format(cog.description, value)  # type: ignore

                embed.add_field(name=name, value=value)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):  # type: ignore
        embed = get_embed_author_member(
            self.context.author,  # type: ignore
            "Rift uses slash commands, meaning the prefix is `/`. Try them out by typing `/`!",
            title="{0.qualified_name} Commands".format(cog),  # type: ignore
            color=discord.Color.blue(),  # type: ignore
        )
        if cog.description:  # type: ignore
            embed.description = cog.description  # type: ignore

        filtered = await self.filter_commands(cog.get_commands(), sort=True)  # type: ignore
        for command in filtered:  # type: ignore
            embed.add_field(
                name=self.get_command_signature(command),  # type: ignore
                value=command.short_doc or "...",  # type: ignore
                inline=False,
            )

        await self.context.reply(embed=embed)  # type: ignore

    async def send_group_help(self, group):  # type: ignore
        embed = get_embed_author_member(
            self.context.author, "Rift uses slash commands, meaning the prefix is `/`. Try them out by typing `/`!", title=group.qualified_name, color=discord.Color.blue()  # type: ignore
        )
        if group.help:  # type: ignore
            embed.description = group.help  # type: ignore

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)  # type: ignore
            for command in filtered:  # type: ignore
                signature = self.get_command_signature(command)  # type: ignore
                if len(signature) > 256:
                    signature = signature[:253] + "..."
                embed.add_field(
                    name=signature,
                    value=command.short_doc or "...",  # type: ignore
                    inline=False,
                )

        await self.context.reply(embed=embed)  # type: ignore

    send_command_help = send_group_help  # type: ignore