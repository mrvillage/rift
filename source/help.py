from datetime import datetime
import discord
from discord import Embed
from discord.ext import commands
from .env import COLOR, FOOTER


def add_fields(embed, fields):
    for field in fields:
        embed.add_field(name=field["name"], value=field["value"],
                        inline=True if "inline" not in field else field["inline"])
    return embed


def get_embed_author_member(member, description=Embed.Empty, color=COLOR, timestamp=None, footer=FOOTER, title=Embed.Empty, fields=[], image_url=Embed.Empty):
    return add_fields(Embed(color=color, description=description, timestamp=datetime.utcnow() if timestamp == None else timestamp, title=title).set_footer(text=footer).set_author(name=f"{member.name}#{member.discriminator}", icon_url=str(member.avatar_url)).set_image(url=image_url), fields)


class EmbedHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        embed = get_embed_author_member(
            self.context.author, title='Bot Commands')
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            name = 'No Category' if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                value = '\u2002'.join(c.name for c in commands)
                if cog and cog.description:
                    value = '{0}\n{1}'.format(cog.description, value)

                embed.add_field(name=name, value=value)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = get_embed_author_member(
            self.context.author, title='{0.qualified_name} Commands'.format(cog))
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(
                command), value=command.short_doc or '...', inline=False)

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = get_embed_author_member(
            self.context.author, title=group.qualified_name)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(
                    command), value=command.short_doc or '...', inline=False)

        await self.get_destination().send(embed=embed)

    send_command_help = send_group_help
