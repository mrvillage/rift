import discord
from discord.ext import commands, menus
from ..funcs.embeds import get_embed_author_member
from ..ref import bot


class Menu(menus.Menu):
    async def update(self, payload):
        try:
            await bot.get_channel(payload.channel_id).get_partial_message(payload.message_id).remove_reaction(payload.emoji, payload.member)
        except discord.Forbidden:
            pass
        await super().update(payload)

    def reaction_check(self, payload):
        if payload.message_id != self.message.id:
            return False
        if payload.user_id not in {self.bot.owner_id, self._author_id, *self.bot.owner_ids}:
            return False
        if payload.event_type == "REACTION_REMOVE":
            return False
        return payload.emoji in self.buttons

    async def finalize(self, timed_out):
        try:
            await self.message.clear_reactions()
        except discord.Forbidden:
            pass


class EmbedPageSource(menus.ListPageSource):
    def __init__(self, data, per_page):
        super().__init__(data, per_page=per_page)

    async def format_page(self, menu, item):
        return item


class MenuPages(menus.MenuPages):
    async def update(self, payload):
        try:
            await bot.get_channel(payload.channel_id).get_partial_message(payload.message_id).remove_reaction(payload.emoji, payload.member)
        except discord.Forbidden:
            pass
        await super().update(payload)

    async def send_initial_message(self, ctx, channel):
        """|coro|

        The default implementation of :meth:`Menu.send_initial_message`
        for the interactive pagination session.

        This implementation shows the first page of the source.
        """
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        return await ctx.reply(**kwargs)

    def reaction_check(self, payload):
        if payload.message_id != self.message.id:
            return False
        if payload.user_id not in {self.bot.owner_id, self._author_id, *self.bot.owner_ids}:
            return False
        if payload.event_type == "REACTION_REMOVE":
            return False
        return payload.emoji in self.buttons

    async def finalize(self, timed_out):
        await self.message.clear_reactions()
