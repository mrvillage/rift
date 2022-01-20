from __future__ import annotations

from typing import Optional, Union

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
    for i in range(3):
        try:
            return await convert_nation(ctx, search, i)
        except NationNotFoundError:
            pass
        try:
            return await convert_alliance(ctx, search, i)
        except AllianceNotFoundError:
            pass
    raise NationOrAllianceNotFoundError(search)


async def convert_alliance(
    ctx: RiftContext, search: Optional[str], stage: int = 0
) -> Alliance:
    search = search or str(ctx.author.id)
    alliances = cache.alliances
    if stage in {0, 1}:
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
        # full name search, case insensitive
        if len(l := [i for i in alliances if i.name.lower() == search.lower()]) == 1:
            return l[0]
        # provided acronym search, case insensitive
        if len(l := [i for i in alliances if i.acronym.lower() == search.lower()]) == 1:
            return l[0]
        if stage == 1:
            raise AllianceNotFoundError(search)
    if stage in {0, 2}:
        # calculated acronym search, case insensitive
        if (
            len(
                l := [
                    i
                    for i in alliances
                    if "".join(j[0] for j in i.name.lower().split(" "))
                    == search.lower()
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
        if stage == 2:
            raise AllianceNotFoundError(search)
    if stage in {0, 3}:
        # partial name search
        if len(l := [i for i in alliances if search.lower() in i.name.lower()]) == 1:
            return l[0]
        if stage == 3:
            raise AllianceNotFoundError(search)
    if stage in {0, 4}:
        try:
            n = await convert_nation(ctx, search)
            if n.alliance is None:
                raise AllianceNotFoundError(search)
            return n.alliance
        except (NationNotFoundError, AttributeError):
            raise AllianceNotFoundError(search)
    raise AllianceNotFoundError(search)


async def convert_nation(ctx: RiftContext, search: str, stage: int = 0) -> Nation:
    search = search or str(ctx.author.id)
    nations = cache.nations
    if stage in {0, 1}:
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
        # full name search, case insensitive
        if len(l := [i for i in nations if i.name.lower() == search.lower()]) == 1:
            return l[0]
        # leader name search, case insensitive
        if len(l := [i for i in nations if i.leader.lower() == search.lower()]) == 1:
            return l[0]
        if stage == 1:
            raise NationNotFoundError(search)
    if stage in {0, 2}:
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
        if stage == 2:
            raise NationNotFoundError(search)
    if stage in {0, 3}:
        # partial name search
        if len(l := [i for i in nations if search.lower() in i.name.lower()]) == 1:
            return l[0]
        # partial leader search
        if len(l := [i for i in nations if search.lower() in i.leader.lower()]) == 1:
            return l[0]
    raise NationNotFoundError(search)
