from __future__ import annotations

import asyncio

import discord

from .. import funcs
from ..data.get import get_alliances_offset, get_max_alliances_page

__all__ = ("AlliancesPaginator",)


class AlliancesPaginator(discord.ui.View):
    def __init__(self, max_page: int, page: int) -> None:
        super().__init__(timeout=None)
        max_page = max_page
        if page >= max_page:
            self.right.disabled = True
        elif page == 1:
            self.left.disabled = True

    @discord.ui.button(
        custom_id="XMP7cqDL99UKz5UHNoPv3zuds64epgX2mD07hV6cfd3ZF9P2JWiPsFhIHYUG1yWW1AQsh1venmDXoF6k",
        emoji="⬅",
        style=discord.ButtonStyle.blurple,
    )
    async def left(self, button: discord.ui.Button, interaction: discord.Interaction):
        desc = interaction.message.embeds[0].description[7:]  # type: ignore
        page = int(desc[: desc.index("**")].strip("*")) - 1
        max_page = await get_max_alliances_page()
        if page == 1:
            button.disabled = True
        for i in self.children:
            if i is not button:
                i.disabled = False  # type: ignore
        offset = (page - 1) * 50
        alliances = await get_alliances_offset(offset=offset)
        await asyncio.gather(*(i._make_members() for i in alliances))
        await asyncio.gather(*(i._make_calculated_score() for i in alliances))
        await asyncio.gather(*(i._make_member_count() for i in alliances))
        embed = funcs.get_embed_author_member(
            interaction.user,  # type: ignore
            f"Page **{page}** of **{max_page}**\n"
            + "Rank: ID, Name, Score, Members\n"
            + "\n".join(
                f"**#{i.rank}**: {i.id}, {i.name}, {i.score:,.2f}, {i.member_count}"
                for i in alliances
            ),
            color=discord.Color.blue(),
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        custom_id="Sti8atDJZR3yCa53mOwN87AaTiV9SrRI0CDV4fd6xtvud6Etx6uYKgUhgqZZ1DZ94fexUhQQYcGdu7pJ",
        emoji="🔃",
        style=discord.ButtonStyle.blurple,
    )
    async def refresh(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        desc = interaction.message.embeds[0].description[7:]  # type: ignore
        page = int(desc[: desc.index("**")].strip("*"))
        max_page = await get_max_alliances_page()
        if page == max_page:
            self.right.disabled = False  # type: ignore
        elif page > max_page:
            page = max_page
            self.right.disabled = False  # type: ignore
        offset = (page - 1) * 50
        alliances = await get_alliances_offset(offset=offset)
        await asyncio.gather(*(i._make_members() for i in alliances))
        await asyncio.gather(*(i._make_calculated_score() for i in alliances))
        await asyncio.gather(*(i._make_member_count() for i in alliances))
        embed = funcs.get_embed_author_member(
            interaction.user,  # type: ignore
            f"Page **{page}** of **{max_page}**\n"
            + "Rank: ID, Name, Score, Members\n"
            + "\n".join(
                f"**#{i.rank}**: {i.id}, {i.name}, {i.score:,.2f}, {i.member_count}"
                for i in alliances
            ),
            color=discord.Color.blue(),
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        custom_id="NixTSNYXBclJfdBbY8mDzTTGziFovBC3f1pTSl7CDoVAxDUlJ7io6Wc4IISyoyXQ6BqQrTsW3XlupLpV",
        emoji="➡",
        style=discord.ButtonStyle.blurple,
    )
    async def right(self, button: discord.ui.Button, interaction: discord.Interaction):
        desc = interaction.message.embeds[0].description[7:]  # type: ignore
        page = int(desc[: desc.index("**")].strip("*")) + 1
        max_page = await get_max_alliances_page()
        if page == max_page:
            button.disabled = True
        elif page > max_page:
            page = max_page
            button.disabled = True
            await interaction.response.send_message(
                embed=funcs.get_embed_author_member(
                    interaction.user,  # type: ignore
                    "Sorry! But the next page doesn't exist!",
                    color=discord.Color.red(),
                )
            )
            return await interaction.edit_original_message(view=self)
        for i in self.children:
            if i is not button:
                i.disabled = False  # type: ignore
        offset = (page - 1) * 50
        alliances = await get_alliances_offset(offset=offset)
        await asyncio.gather(*(i._make_members() for i in alliances))
        await asyncio.gather(*(i._make_calculated_score() for i in alliances))
        await asyncio.gather(*(i._make_member_count() for i in alliances))
        embed = funcs.get_embed_author_member(
            interaction.user,  # type: ignore
            f"Page **{page}** of **{max_page}**\n"
            + "Rank: ID, Name, Score, Members\n"
            + "\n".join(
                f"**#{i.rank}**: {i.id}, {i.name}, {i.score:,.2f}, {i.member_count}"
                for i in alliances
            ),
            color=discord.Color.blue(),
        )
        await interaction.response.edit_message(embed=embed, view=self)
