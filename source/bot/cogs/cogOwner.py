import discord
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level
from ...data.db import execute_query, execute_read_query  # pylint: disable=relative-beyond-top-level


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        if not isinstance(error, commands.CheckFailure):
            await rift.handler(ctx, error)

    @commands.command(name="unlink", aliases=["unverify", "remove-link", "removelink"])
    async def unlink(self, ctx, arg):
        try:
            user = await commands.MemberConverter().convert(ctx, arg)
            user_id = user.id
            try:
                nation_id = (await rift.get_link_user(self.bot.connection, user_id))[1]
            except:
                await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"<@{user_id}> is not linked."))
                return
        except:
            try:
                if "politicsandwar" in arg:
                    if "http" in arg:
                        arg = arg.replace("https://", "")
                    nation_id = int(
                        arg.strip("/\\").replace("politicsandwar.com/nation/id=", ""))
                else:
                    nation_id = int(arg)
                try:
                    link = await rift.get_link_nation(self.bot.connection, nation_id)
                    user_id = link[1]
                except:
                    await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"`{nation_id}` is not linked!"))
            except ValueError:
                await ctx.send(embed=rift.get_embed_author_member(ctx.author, f"`{arg}` is not a valid argument!"))
                return
        await rift.remove_link_nation(self.bot.connection, nation_id)
        await ctx.send(embed=rift.get_embed_author_member(user, f"<@{user_id}> has been unlinked from nation `{nation_id}`."))

    @commands.group(name="extension", invoke_without_command=True)
    async def extension(self, ctx):
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give a subcommand!"))

    @extension.command(name="reload")
    async def extension_reload(self, ctx, *, extension):
        try:
            self.bot.reload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` has been reloaded."))
        except commands.ExtensionNotLoaded:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` is not loaded."))
        except commands.ExtensionNotFound:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` does not exist."))

    @extension.command(name="load")
    async def extension_load(self, ctx, *, extension):
        try:
            self.bot.load_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` has been loaded."))
        except commands.ExtensionAlreadyLoaded:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` is already loaded."))
        except commands.ExtensionNotFound:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` does not exist."))

    @extension.command(name="unload")
    async def extension_unload(self, ctx, *, extension):
        try:
            self.bot.unload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` has been unloaded."))
        except commands.ExtensionNotLoaded:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` is not loaded."))
        except commands.ExtensionNotFound:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"Extension `{extension}` does not exist."))

    @commands.group(name="staff")
    async def staff(self, ctx):
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, "You forgot to give a subcommand!"))

    @staff.command(name="add")
    async def staff_add(self, ctx, member: discord.Member):
        staff = self.bot.get_staff()
        if member.id in staff:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"{member.mention} is already Staff."))
            return
        await execute_query("INSERT INTO staff VALUES ($1);", member.id)
        self.bot.staff.append(member.id)
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"{member.menton} is now Staff."))


def setup(bot):
    bot.add_cog(Owner(bot))
