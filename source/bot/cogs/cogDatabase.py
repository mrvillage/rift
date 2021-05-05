import discord
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level
from ...errors import DocumentNotFoundError, ConvertError  # pylint: disable=relative-beyond-top-level
from ...menus import Confirm  # pylint: disable=relative-beyond-top-level
from ... import checks  # pylint: disable=relative-beyond-top-level
from ... import cache  # pylint: disable=relative-beyond-top-level


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="database", aliases=["archive", "db", "document", "documents"], invoke_without_command=True)
    async def database(self, ctx, *args):
        if not args:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You didn't give any arguments!"))
            return
        try:
            docs = await rift.search_documents(*args)
        except DocumentNotFoundError:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"I couldn't find any documents matching your arguments `{'`, `'.join(args)}`"))
            return
        embed = await rift.get_document_embeds(ctx.author, docs)
        if isinstance(embed, discord.Embed):
            await ctx.reply(embed=embed)
        else:
            await embed.start(ctx)

    @database.command(name="submit", aliases=["sub"])
    async def database_add(self, ctx, *args):
        docs = '\n'.join(args)
        if await Confirm(embed=rift.get_embed_author_member(ctx.author, f"Are you sure you want to submit the following documents?\n{docs}")).confirm(ctx):
            for arg in args:
                await rift.submit_document(url=arg, userid=ctx.author.id)
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"The following documents have been submitted:\n{docs}"))
        else:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"No documents have been submitted."))

    @database.command(name="submissions")
    @checks.is_staff()
    async def database_submissions(self, ctx):
        submissions = await rift.get_document_submissions()
        try:
            subs = '\n'.join([f"{i[0]} - {i[1]}" for i in submissions])
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"There are {len(submissions)} pending submissions:\n{subs}"))
        except IndexError:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "There are no pending submissions."))

    @database.command(name="review")
    @checks.is_staff()
    async def database_review(self, ctx, sub_id: int, status, *, name=None):
        try:
            status = await rift.convert_bool(status)
        except ZeroDivisionError:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{status}` is not a valid status."))
            return
        submission = await rift.get_document_submission(sub_id=sub_id)
        if len(submission) == 0:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{sub_id}` is not a valid submission ID."))
            return
        submission = submission[0]
        if submission[2] is not None:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Submission #{sub_id} is not a pending submission."))
            return
        await rift.edit_document_submission(sub_id=sub_id, status=status)
        if status:
            doc_id = await rift.add_document(name=name, url=submission[1])
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Submission #{sub_id} has been approved."))
            await self.bot.get_user(self.bot.owner_id).send(embed=rift.get_embed_author_member(ctx.author, f"Submission #{sub_id} has been approved and is now document #{doc_id}. Please update with a URL to a copied document immediately.\n{submission[1]}"))
        else:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Submission #{sub_id} has been denied."))

    @database.group(name="edit", invoke_without_command=True)
    @checks.is_staff()
    async def database_edit(self, ctx):
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to say what to edit!"))

    @database_edit.command(name="name")
    @checks.is_staff()
    async def database_edit_name(self, ctx, document_id: int, *, name):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        await rift.edit_document(document_id=document_id, name=name)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s name has been changed to `{name}`."))

    @database_edit.command(name="url")
    @checks.is_owner()
    async def database_edit_url(self, ctx, document_id: int, *, url):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        await rift.edit_document(document_id=document_id, url=url)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s url has been changed to {url}."))

    @database_edit.command(name="description")
    @checks.is_staff()
    async def database_edit_description(self, ctx, document_id: int, *, description):
        description = description.strip("\n")
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        await rift.edit_document(document_id=document_id, description=description)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s description has been changed to:\n`{description}`."))

    @database_edit.group(name="categories", invoke_without_command=True)
    @checks.is_staff()
    async def database_edit_categories(self, ctx):
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to say what to do!"))

    @database_edit_categories.command(name="add")
    @checks.is_staff()
    async def database_edit_categories_add(self, ctx, document_id: int, *args):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        if len(args) == 0:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give any categories!"))
            return
        categories = cache.documents[document_id].categories
        for arg in args:
            categories.append(arg)
        await rift.edit_document(document_id=document_id, categories=categories)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s categories have been changed to `{', '.join(categories) if not len(categories) == 0 else None}`."))

    @database_edit_categories.command(name="remove")
    @checks.is_staff()
    async def database_edit_categories_remove(self, ctx, document_id: int, *args):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        if len(args) == 0:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give any categories!"))
            return
        categories = cache.documents[document_id].categories
        for arg in args:
            if arg in categories:
                categories.remove(arg)
        await rift.edit_document(document_id=document_id, categories=categories)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s categories have been changed to `{', '.join(categories) if not len(categories) == 0 else None}`."))

    @database_edit_categories.command(name="set")
    @checks.is_staff()
    async def database_edit_categories_set(self, ctx, document_id: int, *args):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        if len(args) == 0:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give any categories!"))
            return
        await rift.edit_document(document_id=document_id, categories=args)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s categories have been changed to `{', '.join(args)}`."))

    @database_edit.group(name="keywords", invoke_without_command=True)
    @checks.is_staff()
    async def database_edit_keywords(self, ctx):
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to say what to do!"))

    @database_edit_keywords.command(name="add")
    @checks.is_staff()
    async def database_edit_keywords_add(self, ctx, document_id: int, *args):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        if len(args) == 0:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give any categories!"))
            return
        keywords = cache.documents[document_id].keywords
        for arg in args:
            keywords.append(arg)
        await rift.edit_document(document_id=document_id, keywords=keywords)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s keywords have been changed to `{', '.join(keywords) if not len(keywords) == 0 else None}`."))

    @database_edit_keywords.command(name="remove")
    @checks.is_staff()
    async def database_edit_keywords_remove(self, ctx, document_id: int, *args):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        if len(args) == 0:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give any keywords!"))
            return
        keywords = cache.documents[document_id].keywords
        for arg in args:
            if arg in keywords:
                keywords.remove(arg)
        await rift.edit_document(document_id=document_id, keywords=keywords)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s keywords have been changed to `{', '.join(keywords) if not len(keywords) == 0 else None}`."))

    @database_edit_keywords.command(name="set")
    @checks.is_staff()
    async def database_edit_keywords_set(self, ctx, document_id: int, *args):
        if document_id not in cache.documents:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"`{document_id}` is not a valid document ID."))
            return
        if len(args) == 0:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give any keywords!"))
            return
        await rift.edit_document(document_id=document_id, keywords=args)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Document #{document_id}'s keywords have been changed to `{', '.join(args)}`."))


def setup(bot):
    bot.add_cog(Database(bot))
