from discord import Embed
from datetime import datetime
from ..env import COLOR, FOOTER


def add_fields(embed, fields):
    for field in fields:
        embed.add_field(name=field["name"], value=field["value"],
                        inline=True if "inline" not in field else field["inline"])
    return embed


def get_embed(title: str):
    return Embed(title=title, COLOR=COLOR).set_footer(text=FOOTER)


def get_embed_author(author_name, author_icon_url, description, color=COLOR, timestamp=None, footer=FOOTER):
    return Embed(color=color, description=description, timestamp=datetime.utcnow() if timestamp is None else timestamp).set_footer(text=footer).set_author(name=author_name, icon_url=author_icon_url)


def get_embed_author_member(member, description=Embed.Empty, color=COLOR, timestamp=None, footer=FOOTER, title=Embed.Empty, fields=[], image_url=Embed.Empty):
    return add_fields(Embed(color=color, description=description, timestamp=datetime.utcnow() if timestamp is None else timestamp, title=title).set_footer(text=footer).set_author(name=f"{member.name}#{member.discriminator}", icon_url=str(member.avatar_url)).set_image(url=image_url), fields)


def get_embed_author_guild(guild, description=Embed.Empty, color=COLOR, timestamp=datetime.utcnow(), footer=FOOTER, title=Embed.Empty, fields=[]):
    return add_fields(Embed(color=color, description=description, timestamp=timestamp).set_footer(text=footer).set_author(name=guild.name, icon_url=str(guild.icon_url)), fields)


def get_embed_no_title():
    return Embed(COLOR=COLOR).set_footer(text=FOOTER)


def get_embed_check_dm_page_author_member(author):
    return get_embed_author_member(author, f"Please check your Direct Messages!")


def get_embed_send_dm_error_page_author_member(author):
    return get_embed_author_member(author, f"I couldn't send you a Direct Message!")


def add_timed_out_page(message):
    return message.embeds[0].add_field(name="Timed Out", value="The command timed out.", inline=False)
