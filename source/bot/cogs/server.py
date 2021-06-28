import discord
from discord.ext import commands
from ... import funcs as rift
from ...errors import ServerNotFoundError, BoolError
from ...menus import Confirm
from ... import checks
from ... import cache


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="server",
        aliases=["servers", "invite", "invites"],
        invoke_without_command=True,
    )
    async def server(self, ctx, *args):
        if not args:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You didn't give any arguments!"
                )
            )
            return
        try:
            servers = await rift.search_servers(*args)
        except ServerNotFoundError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author,
                    f"I couldn't find any servers matching your arguments `{'`, `'.join(args)}`",
                )
            )
            return
        embed, invalid = await rift.get_server_embeds(ctx, servers)
        invalid = invalid
        if isinstance(embed, discord.Embed):
            await ctx.reply(embed=embed)
        else:
            await embed.start(ctx)

    @server.command(name="submit", aliases=["sub"])
    async def server_add(self, ctx, *args):
        invites = []
        good = []
        for arg in args:
            try:
                invite = await commands.InviteConverter().convert(ctx, arg)
                invites.append(invite)
                good.append(str(invite))
            except commands.BadInviteArgument:
                pass
        good = "\n".join(good)
        if not invites:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You didn't submit any valid invites!"
                )
            )
            return
        if await Confirm(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Are you sure you want to submit the following servers?\n{good}",
            )
        ).confirm(ctx):
            for arg in args:
                await rift.submit_server(invite=arg, userid=ctx.author.id)
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"The following servers have been submitted:\n{good}"
                )
            )
        else:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"No servers have been submitted."
                )
            )

    @server.command(name="submissions")
    @checks.is_staff()
    async def server_submissions(self, ctx):
        submissions = await rift.get_server_submissions()
        try:
            subs = "\n".join([f"{i[0]} - {i[1]}" for i in submissions])
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author,
                    f"There are {len(submissions)} pending submissions:\n{subs}",
                )
            )
        except IndexError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "There are no pending submissions."
                )
            )

    @server.command(name="review")
    @checks.is_staff()
    async def server_review(self, ctx, sub_id: int, status, *, name=None):
        try:
            status = await rift.convert_bool(status)
        except BoolError:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{status}` is not a valid status."
                )
            )
            return
        submission = await rift.get_server_submission(sub_id=sub_id)
        if len(submission) == 0:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{sub_id}` is not a valid submission ID."
                )
            )
            return
        submission = submission[0]
        if submission[2] is not None:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Submission #{sub_id} is not a pending submission."
                )
            )
            return
        await rift.edit_server_submission(sub_id=sub_id, status=status)
        if status:
            await rift.add_server(name=name, invite=submission[1])
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Submission #{sub_id} has been approved."
                )
            )
        else:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"Submission #{sub_id} has been denied."
                )
            )

    @server.group(name="edit", invoke_without_command=True)
    @checks.is_staff()
    async def server_edit(self, ctx):
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, "You forgot to say what to edit!"
            )
        )

    @server_edit.command(name="name")
    @checks.is_staff()
    async def server_edit_name(self, ctx, server_id: int, *, name):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        await rift.edit_server(server_id=server_id, name=name)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, f"Server #{server_id}'s name has been changed to `{name}`."
            )
        )

    @server_edit.command(name="invite")
    @checks.is_owner()
    async def server_edit_invite(self, ctx, server_id: int, *, invite):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        await rift.edit_server(server_id=server_id, invite=invite)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s invite has been changed to {invite}.",
            )
        )

    @server_edit.command(name="description")
    @checks.is_staff()
    async def server_edit_description(self, ctx, server_id: int, *, description):
        description = description.strip("\n")
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        await rift.edit_server(server_id=server_id, description=description)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s description has been changed to:\n`{description}`.",
            )
        )

    @server_edit.group(name="categories", invoke_without_command=True)
    @checks.is_staff()
    async def server_edit_categories(self, ctx):
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, "You forgot to say what to do!"
            )
        )

    @server_edit_categories.command(name="add")
    @checks.is_staff()
    async def server_edit_categories_add(self, ctx, server_id: int, *args):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        if len(args) == 0:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You forgot to give any categories!"
                )
            )
            return
        categories = cache.servers[server_id].categories
        for arg in args:
            categories.append(arg)
        await rift.edit_server(server_id=server_id, categories=categories)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s categories have been changed to `{', '.join(categories) if not len(categories) == 0 else None}`.",
            )
        )

    @server_edit_categories.command(name="remove")
    @checks.is_staff()
    async def server_edit_categories_remove(self, ctx, server_id: int, *args):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        if len(args) == 0:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You forgot to give any categories!"
                )
            )
            return
        categories = cache.servers[server_id].categories
        for arg in args:
            if arg in categories:
                categories.remove(arg)
        await rift.edit_server(server_id=server_id, categories=categories)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s categories have been changed to `{', '.join(categories) if not len(categories) == 0 else None}`.",
            )
        )

    @server_edit_categories.command(name="set")
    @checks.is_staff()
    async def server_edit_categories_set(self, ctx, server_id: int, *args):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        if len(args) == 0:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You forgot to give any categories!"
                )
            )
            return
        await rift.edit_server(server_id=server_id, categories=args)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s categories have been changed to `{', '.join(args)}`.",
            )
        )

    @server_edit.group(name="keywords", invoke_without_command=True)
    @checks.is_staff()
    async def server_edit_keywords(self, ctx):
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author, "You forgot to say what to do!"
            )
        )

    @server_edit_keywords.command(name="add")
    @checks.is_staff()
    async def server_edit_keywords_add(self, ctx, server_id: int, *args):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        if len(args) == 0:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You forgot to give any categories!"
                )
            )
            return
        keywords = cache.servers[server_id].keywords
        for arg in args:
            keywords.append(arg)
        await rift.edit_server(server_id=server_id, keywords=keywords)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s keywords have been changed to `{', '.join(keywords) if not len(keywords) == 0 else None}`.",
            )
        )

    @server_edit_keywords.command(name="remove")
    @checks.is_staff()
    async def server_edit_keywords_remove(self, ctx, server_id: int, *args):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        if len(args) == 0:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You forgot to give any keywords!"
                )
            )
            return
        keywords = cache.servers[server_id].keywords
        for arg in args:
            if arg in keywords:
                keywords.remove(arg)
        await rift.edit_server(server_id=server_id, keywords=keywords)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s keywords have been changed to `{', '.join(keywords) if not len(keywords) == 0 else None}`.",
            )
        )

    @server_edit_keywords.command(name="set")
    @checks.is_staff()
    async def server_edit_keywords_set(self, ctx, server_id: int, *args):
        if server_id not in cache.servers:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, f"`{server_id}` is not a valid server ID."
                )
            )
            return
        if len(args) == 0:
            await ctx.reply(
                embed=rift.get_embed_author_member(
                    ctx.author, "You forgot to give any keywords!"
                )
            )
            return
        await rift.edit_server(server_id=server_id, keywords=args)
        await ctx.reply(
            embed=rift.get_embed_author_member(
                ctx.author,
                f"Server #{server_id}'s keywords have been changed to `{', '.join(args)}`.",
            )
        )


def setup(bot):
    bot.add_cog(Server(bot))
