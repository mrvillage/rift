from .base import Menu
from discord.ext import menus


class Confirm(Menu):
    def __init__(self, msg=None, embed=None):
        super().__init__(timeout=30.0)
        self.msg = msg
        self.embed = embed
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await ctx.reply(content=self.msg, embed=self.embed)

    @menus.button("\N{WHITE HEAVY CHECK MARK}")
    async def confirmed(self, payload):
        self.result = True
        self.stop()

    @menus.button("\N{CROSS MARK}")
    async def denied(self, payload):
        self.result = False
        self.stop()

    async def confirm(self, ctx):
        await self.start(ctx, wait=True)
        return self.result


class ConfirmMessage(Menu):
    def __init__(self, msg=None, embed=None):
        super().__init__(timeout=30.0)
        self.msg = msg
        self.embed = embed
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await ctx.reply(content=self.msg, embed=self.embed)

    @menus.button("\N{WHITE HEAVY CHECK MARK}")
    async def confirmed(self, payload):
        self.result = True
        self.stop()

    @menus.button("\N{CROSS MARK}")
    async def denied(self, payload):
        self.result = False
        self.stop()

    async def confirm(self, ctx):
        await self.start(ctx, wait=True)
        return self.result, self.message
