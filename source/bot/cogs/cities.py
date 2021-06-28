import discord
from discord.ext import commands


class Cities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Cities(bot))


# Will accept every parameter but will ignore imp_total
# If nothing is set then it will not check anything for that improvement
# Integers will say it needs to be exactly at this point, <, <=, =, ==, >=, > will all also work
# * will be ignore
# & is for necessary (will only work for power plants)

# Set dynamic requirements with $, max or none
# # will default it to the MMR that the build would fall under based upon city count and infrastructure

# %(number) will be mutually exclusive, you have one of that set with the number

# Will have suggested builds you can assign to members
