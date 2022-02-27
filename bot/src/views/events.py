from __future__ import annotations

from typing import TYPE_CHECKING, Union

import discord

from ..cache import cache

__all__ = ("EventExtraInformationView",)


class FakeContext:
    def __init__(
        self, author: Union[discord.User, discord.Member], guild: discord.Guild
    ):
        self.author = author
        self.guild = guild


class EventExtraInformationButton(discord.ui.Button["EventExtraInformationView"]):
    def __init__(self):
        super().__init__(
            label="Extra Information",
            style=discord.ButtonStyle.grey,
            custom_id="WKiLtjZLlX6irkSllEiz5b17UTupd2uIvuxRDUaqd2qQSrs7I2AEPp50VanAPBpNX8rCLOx2TpiCpR6m",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert interaction.message is not None
        desc: str = interaction.message.embeds[0].description  # type: ignore
        short = desc[desc.find("politicsandwar.com/") + 19 :]
        type = short[: short.find("/")]
        id = short[short.find("id=") + 3 : short.find(" ")]
        if type == "nation":
            nation = cache.get_nation(int(id))
            if nation is None:
                return
            embed = nation.get_info_embed(
                FakeContext(interaction.user, interaction.guild)  # type: ignore
            )
        elif type == "alliance":
            alliance = cache.get_alliance(int(id))
            if alliance is None:
                return
            embed = alliance.get_info_embed(
                FakeContext(interaction.user, interaction.guild)  # type: ignore
            )
        else:
            return
        await interaction.response.send_message(embed=embed, ephemeral=True)


class EventExtraInformationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(EventExtraInformationButton())  # type: ignore
