import discord
from discord.ext import commands, menus


class MenuManager:
    def __init__(self, channel, content=None, embed=None):
        self.channel = channel
        self.content = content
        self.embed = embed

    async def start(self):
        self.message = await self.channel.send(self.content, embed=self.embed)
