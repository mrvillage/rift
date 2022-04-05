from __future__ import annotations

from typing import TYPE_CHECKING

from .. import models, options
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ("MilitarizationCommand",)


if TYPE_CHECKING:

    class MilitarizationCommandOptions:
        ...


@bot.command
class MilitarizationCommand(
    CommonSlashCommand["MilitarizationCommandOptions"],
    name="militarization",
    description="Get militarization information.",
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MilitarizationNationCommandOptions:
        nation: models.Nation


class MilitarizationNationCommand(
    CommonSlashCommand["MilitarizationNationCommandOptions"],
    name="nation",
    description="Get the militarization of a nation.",
    parent=MilitarizationCommand,
    options=[options.NATION_DEFAULT_SELF],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MilitarizationAllianceCommandOptions:
        alliance: models.Alliance


class MilitarizationAllianceCommand(
    CommonSlashCommand["MilitarizationAllianceCommandOptions"],
    name="alliance",
    description="Get the militarization of an alliance.",
    parent=MilitarizationCommand,
    options=[options.ALLIANCE_DEFAULT_SELF],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MilitarizationBlocCommandOptions:
        ...


class MilitarizationBlocCommand(
    CommonSlashCommand["MilitarizationBlocCommandOptions"],
    name="bloc",
    description="Get the militarization of a bloc.",
    parent=MilitarizationCommand,
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MilitarizationNationsCommandOptions:
        condition: models.Condition


class MilitarizationNationsCommand(
    CommonSlashCommand["MilitarizationNationsCommandOptions"],
    name="nations",
    description="Get the militarization of a group of nations.",
    parent=MilitarizationCommand,
    options=[options.CONDITION],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MilitarizationAlliancesCommandOptions:
        condition: models.Condition


class MilitarizationAlliancesCommand(
    CommonSlashCommand["MilitarizationAlliancesCommandOptions"],
    name="alliances",
    description="Get the militarization of a group of alliances.",
    parent=MilitarizationCommand,
    options=[options.CONDITION],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...
