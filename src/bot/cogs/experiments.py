import asyncio
from src.flags.base import BooleanFlagConverter
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands.flags import FlagConverter

from ...data.classes import FullCity, Nation
from ...data.query import get_mmr
from ... import funcs


class Flags(
    BooleanFlagConverter,
    case_insensitive=True,
    delimiter="=",
    prefix="-",
):
    hi: Optional[str]
    hello: Optional[str]


class Vie(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()


class Experiments(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="flags")
    async def flags(self, ctx, *, flags: Flags):
        # flags = Flags.parse_flags(flags)
        await ctx.send(str(flags))

    @commands.command(name="view")
    async def view(self, ctx):
        class Viewer(discord.ui.View):
            def __init__(self) -> None:
                print("HI")
                super().__init__()
                print("HI")

            @discord.ui.button(label="Hello")
            async def oogabooga(
                self, btn: discord.ui.Button, interaction: discord.Interaction
            ):
                followup = interaction.followup
                await interaction.response.defer()
                await asyncio.sleep(15)
                await followup.send(f"Hello", ephemeral=True)

        view = Viewer()
        vie = Vie()
        await ctx.send("View", view=view)

    @commands.command(name="provider")
    async def provider(self, ctx: commands.Context):
        embed = discord.Embed(description="This is a provider")
        print(embed.provider)
        embed._provider = {
            "name": "Ash Development",
            "url": "https://rift.mrvillage.dev",
        }
        print(embed.provider)
        print(embed._provider)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Experiments(bot))
