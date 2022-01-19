from __future__ import annotations

from typing import Union

from discord.ext import commands

from ..cache import cache
from ..data.classes import Alliance, Nation
from ..errors import (
    AllianceNotFoundError,
    LinkError,
    NationNotFoundError,
    NationOrAllianceNotFoundError,
)
from ..funcs.utils import convert_link
from ..ref import RiftContext

__all__ = ("convert_nation_or_alliance", "convert_alliance", "convert_nation")


async def convert_nation_or_alliance(
    ctx: RiftContext, search: str
) -> Union[Nation, Alliance]:
    try:
        return await Nation.convert(ctx, search, False)
    except NationNotFoundError:
        try:
            return await Alliance.convert(ctx, search, False)
        except AllianceNotFoundError:
            try:
                return await Nation.convert(ctx, search, True)
            except NationNotFoundError:
                try:
                    return await Alliance.convert(ctx, search, True)
                except AllianceNotFoundError:
                    raise NationOrAllianceNotFoundError(search)

async def convert_alliance(
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
        n = await convert_nation(ctx, search)
        if n.alliance is None:
            raise AllianceNotFoundError(search)
        return n.alliance
    except (NationNotFoundError, AttributeError):
        raise AllianceNotFoundError(search)
    raise AllianceNotFoundError(search)

async def convert_nation(ctx: RiftContext, search: str, advanced: bool = True) -> Nation:
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
            if nation is not None:
                return nation
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
