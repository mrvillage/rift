from __future__ import annotations

from discord.ext import commands

from ..cache import cache
from ..data.classes import Alliance
from ..errors import AllianceNotFoundError, LinkError, NationNotFoundError
from ..funcs.utils import convert_link
from ..ref import RiftContext
from .nation import search_nation

__all__ = ("search_alliance",)


async def search_alliance(
    ctx: RiftContext, search: str, advanced: bool = False
) -> Alliance:
    search = search or str(ctx.author.id)
    try:
        search = convert_link(search)
    except LinkError:
        pass
    try:
        user = await commands.MemberConverter().convert(ctx, search)  # type: ignore
    except commands.MemberNotFound:
        try:
            user = await commands.UserConverter().convert(ctx, search)  # type: ignore
        except commands.UserNotFound:
            user = None
    if user is not None:
        link = cache.get_user(user.id)
        if link is not None:
            nation = cache.get_nation(link.nation_id)
            if nation is not None and nation.alliance is not None:
                return nation.alliance
    if search.isdigit():
        try:
            return await Alliance.fetch(int(search))
        except AllianceNotFoundError:
            pass
    alliances = cache.alliances
    # full name search, case insensitive
    if len(l := [i for i in alliances if i.name.lower() == search.lower()]) == 1:
        return l[0]
    # provided acronym search, case insensitive
    if len(l := [i for i in alliances if i.acronym.lower() == search.lower()]) == 1:
        return l[0]
    if not advanced:
        raise AllianceNotFoundError(search)
    # calculated acronym search, case insensitive
    if (
        len(
            l := [
                i
                for i in alliances
                if "".join(j[0] for j in i.name.lower().split(" ")) == search.lower()
            ]
        )
        == 1
    ):
        return l[0]
    # calculated acronym search, case insensitive, no "the"
    if (
        len(
            l := [
                i
                for i in alliances
                if "".join(j[0] for j in i.name.lower().split(" ") if j != "the")
                == search.lower()
            ]
        )
        == 1
    ):
        return l[0]
    # full name search, case insensitive, no "the"
    if (
        len(
            l := [
                i
                for i in alliances
                if i.name.lower().replace("the ", "")
                == search.lower().replace("the ", "")
            ]
        )
        == 1
    ):
        return l[0]
    # startswith and endswith search, case insensitive
    if (
        len(
            l := [
                i
                for i in alliances
                if i.name.lower().startswith(search.lower())
                or i.name.lower().endswith(search.lower())
            ]
        )
        == 1
    ):
        return l[0]
    # startswith and endswith search, case insensitive, no "the"
    if (
        len(
            l := [
                i
                for i in alliances
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
    # partial name search
    if len(l := [i for i in alliances if search.lower() in i.name.lower()]) == 1:
        return l[0]
    try:
        n = await search_nation(ctx, search)
        if n.alliance is None:
            raise AllianceNotFoundError(search)
        return n.alliance
    except (NationNotFoundError, AttributeError):
        raise AllianceNotFoundError(search)
    raise AllianceNotFoundError(search)
