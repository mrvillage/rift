from __future__ import annotations

from typing import TYPE_CHECKING, List

import discord
from discord.ext import commands

from ... import funcs
from ...cache import cache
from ...data.classes import Alliance, ForumPost, Nation, Treaty, War
from ...ref import Rift, bot
from ...views import Info


class EventMessages(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.Cog.listener()
    async def on_alliance_create(self, alliance: Alliance):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "ALLIANCE" and i.type == "CREATE"
        ]
        for sub in subscriptions:
            if sub.condition is None:
                pass
            elif sum(await sub.condition.evaluate(alliance)) == 0:
                continue
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f"**Alliance created!**\n[{repr(alliance)}](https://politicsandwar.com/alliance/id={alliance.id})",
                    color=discord.Color.blue(),
                ),
                view=Info().add_button(
                    "Extra Information", f"info-alliance-{alliance.id}"
                ),
            )

    @commands.Cog.listener()
    async def on_alliance_delete(self, alliance: Alliance):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "ALLIANCE" and i.type == "DELETE"
        ]
        for sub in subscriptions:
            if sub.condition is None:
                pass
            elif sum(await sub.condition.evaluate(alliance)) == 0:
                continue
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f"**Alliance deleted!**\n[{repr(alliance)}](https://politicsandwar.com/alliance/id={alliance.id})",
                    color=discord.Color.blue(),
                ),
            )

    @commands.Cog.listener()
    async def on_forum_post_create(self, post: ForumPost, title: str):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "FORUM_POST" and i.type == "CREATE"
        ]
        for sub in subscriptions:
            if post.forum.name.upper().replace(" ", "_") not in sub.sub_types:
                continue
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f'**Forum Post Created!**\nForum: {post.forum.name}\n[{title}]({post.link} "{post.link}")',
                    color=discord.Color.blue(),
                ),
            )

    @commands.Cog.listener()
    async def on_nation_create(self, nation: Nation):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "NATION" and i.type == "CREATE"
        ]
        for sub in subscriptions:
            if sub.condition is None:
                pass
            elif sum(await sub.condition.evaluate(nation)) == 0:
                continue
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f"**Nation created!**\n[{repr(nation)}](https://politicsandwar.com/nation/id={nation.id})",
                    color=discord.Color.blue(),
                ),
                view=Info().add_button("Extra Information", f"info-nation-{nation.id}"),
            )

    @commands.Cog.listener()
    async def on_nation_update(self, before: Nation, after: Nation):
        # sourcery no-metrics
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "NATION" and i.type == "UPDATE"
        ]
        for sub in subscriptions:
            if sub.condition is None:
                pass
            elif sum(await sub.condition.evaluate(before, after)) == 0:
                continue
            changes: List[str] = []
            if (
                "ALLIANCE" in sub.sub_types
                or "ALLIANCE_POSITION" in sub.sub_types
                or "ALLIANCE_POSITION_ALL" in sub.sub_types
            ) and before.alliance != after.alliance:
                changes.append(
                    f"- Alliance changed from [{repr(before.alliance)}](https://politicsandwar.com/alliance/id={(before.alliance and before.alliance.id) or 0}) to [{repr(after.alliance)}](https://politicsandwar.com/alliance/id={(after.alliance and after.alliance.id) or 0})."
                )
            if (
                (
                    "ALLIANCE_POSITION" in sub.sub_types
                    or "ALLIANCE_POSITION_ALL" in sub.sub_types
                )
                and before.alliance_position != after.alliance_position
                and (
                    before.alliance_position >= 3
                    or after.alliance_position >= 3
                    or "ALLIANCE_POSITION_ALL" in sub.sub_types
                )
            ):
                changes.append(
                    f"- Alliance position changed from {funcs.utils.get_alliance_position(before.alliance_position)} to {funcs.utils.get_alliance_position(after.alliance_position)}."
                )
            if ("VACATION_MODE" in sub.sub_types) and before.v_mode != after.v_mode:
                if after.v_mode:
                    changes.append("Entered Vacation Mode.")
                else:
                    changes.append("Exited Vacation Mode.")
            if changes:
                str_changes = "\n".join(changes)
                await sub.send(
                    funcs.get_embed_author_member(
                        bot.user,
                        f"**Nation updated!**\n[{repr(after)}](https://politicsandwar.com/nation/id={after.id})\n\n**Changes**\n{str_changes}",
                        color=discord.Color.blue(),
                    ),
                    view=Info().add_button(
                        "Extra Information", f"info-nation-{after.id}"
                    ),
                )

    @commands.Cog.listener()
    async def on_nation_delete(self, nation: Nation):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "NATION" and i.type == "DELETE"
        ]
        for sub in subscriptions:
            if sub.condition is None:
                pass
            elif sum(await sub.condition.evaluate(nation)) == 0:
                continue
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f"**Nation deleted!**\n[{repr(nation)}](https://politicsandwar.com/nation/id={nation.id})",
                    color=discord.Color.blue(),
                ),
            )

    @commands.Cog.listener()
    async def on_treaty_create(self, treaty: Treaty):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "TREATY" and i.type == "CREATE"
        ]
        for sub in subscriptions:
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f"**Treaty created!**\n{treaty.treaty_type} from [{repr(treaty.from_)}](https://politicsandwar.com/alliance/id={treaty.from_.id if treaty.from_ else 0}) to [{repr(treaty.to_)}](https://politicsandwar.com/alliance/id={treaty.to_.id if treaty.to_ else 0}).",
                    color=discord.Color.blue(),
                ),
            )

    @commands.Cog.listener()
    async def on_treaty_delete(self, treaty: Treaty):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i
            for i in cache.subscriptions
            if i.category == "TREATY" and i.type == "DELETE"
        ]
        for sub in subscriptions:
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f"**Treaty deleted!**\n{treaty.treaty_type} from [{repr(treaty.from_)}](https://politicsandwar.com/alliance/id={treaty.from_.id if treaty.from_ else 0}) to [{repr(treaty.to_)}](https://politicsandwar.com/alliance/id={treaty.to_.id if treaty.to_ else 0}).",
                    color=discord.Color.blue(),
                ),
            )

    @commands.Cog.listener()
    async def on_war_create(self, war: War):
        if TYPE_CHECKING:
            assert isinstance(bot.user, discord.User)
        subscriptions = [
            i for i in cache.subscriptions if i.category == "WAR" and i.type == "CREATE"
        ]
        for sub in subscriptions:
            if sub.condition is None:
                pass
            elif sum(await sub.condition.evaluate(war.attacker, war.defender)) == 0:
                continue
            await sub.send(
                funcs.get_embed_author_member(
                    bot.user,
                    f"**War created!**\n[{war.attacker}](https://politicsandwar.com/nation/id={(war.attacker and war.attacker.id) or 0}) of {f'alliance [{war.attacker.alliance}](https://politicsandwar.com/alliance/id={war.attacker.alliance_id})' if war.attacker is not None else 'no alliance'} declared war on [{repr(war.defender)}](https://politicsandwar.com/nation/id={(war.defender and war.defender.id) or 0}) of {f'alliance [{war.defender.alliance}](https://politicsandwar.com/alliance/id={war.defender.alliance_id})' if war.defender is not None else 'no alliance'}.",
                    color=discord.Color.blue(),
                ),
                view=Info()
                .add_url(
                    "War Page",
                    f"https://politicsandwar.com/nation/war/timeline/war={war.id}",
                )
                .add_button("Attacker Information", f"info-nation-{war.attacker_id}")
                .add_button("Defender Information", f"info-nation-{war.defender_id}"),
            )


def setup(bot: Rift):
    bot.add_cog(EventMessages(bot))