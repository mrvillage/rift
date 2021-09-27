from __future__ import annotations

from discord.ext import commands

from ..cache import cache
from ..data.classes import Nation
from ..errors import LinkError, NationNotFoundError
from ..funcs.utils import convert_link
from .link import get_link_user

__all__ = ("search_nation",)


async def search_nation(
    ctx: commands.Context, search: str, advanced: bool = True
) -> Nation:
    try:
        search = await convert_link(search)
    except LinkError:
        pass
    try:
        user = await commands.MemberConverter().convert(ctx, search)
    except commands.MemberNotFound:
        try:
            user = await commands.UserConverter().convert(ctx, search)
        except commands.UserNotFound:
            user = None
    if user is not None:
        try:
            return await Nation.fetch((await get_link_user(user.id))["nation_id"])
        except IndexError:
            pass
    if search.isdigit():
        try:
            return await Nation.fetch(int(search))
        except KeyError:
            pass
    nations = cache.nations
    # full name search, case insensitive
    if len(l := [i for i in nations if i.name.lower() == search.lower()]) == 1:
        return l[0]
    # leader name search, case insensitive
    if len(l := [i for i in nations if i.leader.lower() == search.lower()]) == 1:
        return l[0]
    if not advanced:
        raise NationNotFoundError(search)
    # full name search, case insensitive, no "the"
    if (
        len(
            l := [
                i
                for i in nations
                if i.name.lower().replace("the ", "")
                == search.lower().replace("the ", "")
            ]
        )
        == 1
    ):
        return l[0]
    # startswith and endswith name search, case insensitive
    if (
        len(
            l := [
                i
                for i in nations
                if i.name.lower().startswith(search.lower())
                or i.name.lower().endswith(search.lower())
            ]
        )
        == 1
    ):
        return l[0]
    # startswith and endswith name search, case insensitive, no "the"
    if (
        len(
            l := [
                i
                for i in nations
                if i.name.lower()
                .replace("the ", "")
                .startswith(search.lower().replace("the ", ""))
                or i.name.lower()
                .replace("the ", "")
                .endswith(search.lower().replace("the ", ""))
            ]
        )
        == 1
    ):
        return l[0]
    # startswith and endswith leader search, case insensitive
    if (
        len(
            l := [
                i
                for i in nations
                if i.leader.lower().startswith(search.lower())
                or i.leader.lower().endswith(search.lower())
            ]
        )
        == 1
    ):
        return l[0]
    # partial name search
    if len(l := [i for i in nations if search.lower() in i.name.lower()]) == 1:
        return l[0]
    # partial leader search
    if len(l := [i for i in nations if search.lower() in i.leader.lower()]) == 1:
        return l[0]
    raise NationNotFoundError(search)
