import datetime
import sys
from discord import Intents, AllowedMentions, Game
import aiohttp
from .env import EMAIL, PASSWORD, __version__
from .errors import LoginError
from discord.ext.commands import Bot, when_mentioned_or
from .data.db.connect import connection
from .data.db import execute_read_query
from .help import EmbedHelpCommand


class Rift(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.alliances_update = datetime.datetime.utcnow()
        self.nations_update = datetime.datetime.utcnow()
        print(f"Starting up!")
        self.pnw_session = None

    async def update_pnw_session(self):
        self.new_pnw_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30.0))
        login_data = {
            "email": EMAIL,
            "password": PASSWORD,
            "loginform": "Login"
        }
        async with self.new_pnw_session.request("POST", "https://politicsandwar.com/login/", data=login_data) as response:
            if "login failure" in (await response.text()).lower():
                raise LoginError
        try:
            await self.pnw_session.close()
            self.pnw_session = self.new_pnw_session
            del self.new_pnw_session
        except AttributeError:
            self.pnw_session = self.new_pnw_session
            del self.new_pnw_session

    async def get_staff(self):
        self.staff = [i[0] for i in await execute_read_query("SELECT * FROM staff;")]
        return self.staff

    async def close(self):
        await self.pnw_session.close()
        await super().close()


intents = Intents.all()
bot = Rift(command_prefix=when_mentioned_or("?"), intents=intents, case_insensitive=True,
           allowed_mentions=AllowedMentions(replied_user=False), activity=Game(name=__version__), strip_after_prefix=True, help_command=EmbedHelpCommand())
