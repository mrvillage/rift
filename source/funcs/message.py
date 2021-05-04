import aiohttp
from .. import APIKEY, EMAIL, PASSWORD # pylint: disable=relative-beyond-top-level
from ..errors.message import * # pylint: disable=unused-wildcard-import

async def send_message(*, receiver=None, subject=None, content=None):
    async with aiohttp.ClientSession(timeout=30) as session:
        message_data = {
            "newconversation": "true",
            "receiver": receiver,
            "subject": subject,
            "body": content,
            "sndmsg": "Send Message"
        }
        async with session.post("https://politicsandwar.com/inbox/message", data=message_data) as response:
            if "successfully" in (await response.text()).lower():
                return True
            else:
                return SentError

async def send_message_many(*, email=None, password=None, key=None, receivers=None, subject=None, content=None):
    async with aiohttp.ClientSession(timeout=30) as session:
        login_data = {
            "email": email,
            "password": password,
            "loginform": "Login"
        }
        async with session.post("https://politicsandwar.com/login/", data=login_data) as response:
            if "login failure" in (await response.text()).lower():
                raise LoginError("Login Failure. Incorrect email or password.")
        errors = []
        for receiver in receivers:
            try:
                message_data = {
                    "newconversation": "true",
                    "receiver": receiver,
                    "subject": subject,
                    "body": content,
                    "sndmsg": "Send Message"
                }
                async with session.post("https://politicsandwar.com/inbox/message", data=message_data) as response:
                    if "successfully" in (await response.text()).lower():
                        return True
                    else:
                        return SentError(f"'{receiver}'")
            except SentError as error:
                errors.append(error.__str__())
        if len(errors) > 0:
            raise SentError(errors)