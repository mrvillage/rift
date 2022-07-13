from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import checks, consts, embeds, flags, models
from .common import CommonGrid, CommonSelectMenu

__all__ = ("TargetFindGrid", "TargetsGrid")

if TYPE_CHECKING:
    import lang
    from quarrel import Missing


class TargetFindGrid(CommonGrid, checks=[checks.grid_owner_only]):
    __slots__ = (
        "owner_id",
        "rater",
        "attack",
        "expression",
        "nation",
    )

    def __init__(
        self,
        owner_id: int,
        rater: models.TargetRater,
        attack: bool,
        expression: Missing[lang.Expression],
        nation: models.Nation,
    ) -> None:
        super().__init__(timeout=consts.TARGET_FIND_TIMEOUT)
        self.owner_id: int = owner_id
        self.rater: models.TargetRater = rater
        self.attack: bool = attack
        self.expression: Missing[lang.Expression] = expression
        self.nation: models.Nation = nation
        self.add_component(
            TargetFindSelectMenu(owner_id, rater, attack, expression, nation)
        )


class TargetFindSelectMenu(CommonSelectMenu):
    __slots__ = (
        "owner_id",
        "rater",
        "attack",
        "expression",
        "nation",
    )

    def __init__(
        self,
        owner_id: int,
        rater: models.TargetRater,
        attack: bool,
        expression: Missing[lang.Expression],
        nation: models.Nation,
    ) -> None:
        super().__init__(
            placeholder="Attributes to include in rating (you have 5 minutes).",
            min_values=1,
            max_values=21,
            options=[
                quarrel.SelectOption(label="Cities", value="cities"),
                quarrel.SelectOption(label="Infrastructure", value="infrastructure"),
                quarrel.SelectOption(label="Activity", value="activity"),
                quarrel.SelectOption(label="Soldiers", value="soldiers"),
                quarrel.SelectOption(label="Tanks", value="tanks"),
                quarrel.SelectOption(label="Aircraft", value="aircraft"),
                quarrel.SelectOption(label="Ships", value="ships"),
                quarrel.SelectOption(label="Missiles", value="missiles"),
                quarrel.SelectOption(label="Nukes", value="nukes"),
                quarrel.SelectOption(label="Money", value="money"),
                quarrel.SelectOption(label="Coal", value="coal"),
                quarrel.SelectOption(label="Oil", value="oil"),
                quarrel.SelectOption(label="Uranium", value="uranium"),
                quarrel.SelectOption(label="Iron", value="iron"),
                quarrel.SelectOption(label="Bauxite", value="bauxite"),
                quarrel.SelectOption(label="Lead", value="lead"),
                quarrel.SelectOption(label="Gasoline", value="gasoline"),
                quarrel.SelectOption(label="Munitions", value="munitions"),
                quarrel.SelectOption(label="Steel", value="steel"),
                quarrel.SelectOption(label="Aluminum", value="aluminum"),
                quarrel.SelectOption(label="Food", value="food"),
            ],
        )
        self.owner_id: int = owner_id
        self.rater: models.TargetRater = rater
        self.attack: bool = attack
        self.expression: Missing[lang.Expression] = expression
        self.nation: models.Nation = nation

    async def callback(
        self,
        interaction: quarrel.Interaction,
        groups: dict[str, str],
        values: tuple[str],
    ) -> None:
        await interaction.respond_with_edit(
            embed=embeds.target_find_processing(interaction),
            grid=quarrel.Grid(timeout=0),
        )
        targets = models.TargetConfig.find_targets(
            flags.TargetFindCounting.from_values(values),
            self.rater,
            self.attack,
            self.expression,
            self.nation,
        )
        await interaction.edit_original_response(
            embed=embeds.targets(interaction, targets, 1, self.nation),
            grid=TargetsGrid(self.owner_id, targets, 1),
        )


class TargetsGrid(CommonGrid, checks=[checks.grid_owner_only]):
    __slots__ = (
        "owner_id",
        "targets",
        "page",
    )

    def __init__(
        self,
        owner_id: int,
        targets: list[models.Target],
        page: int,
    ) -> None:
        super().__init__(timeout=300)
        self.owner_id: int = owner_id
        self.targets: list[models.Target] = targets
        self.page: int = page
