from ...ref import bot


async def withdraw(*, transaction, receiver, note: str = None):
    transaction_data = transaction.get_data_withdraw()
    transaction_data["withtype"] = type(receiver).__name__
    if note is not None:
        transaction_data["withnote"] = note
    transaction_data["withrecipient"] = receiver.name
    if bot.auth_token is not None:
        transaction_data["token"] = bot.auth_token
    async with bot.pnw_session.request(
        "POST",
        "https://politicsandwar.com/alliance/id=3683&display=bank",
        data=transaction_data,
    ) as response:
        content = await response.text()
    await bot.parse_token(content)
    if "Something went wrong" in content:
        return False
    elif "successfully transferred" in content:
        return True
    else:
        return False
