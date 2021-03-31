from config import cfg
import discord
from discord.ext import commands
import asyncio
import logging
import re

from celcat import Calendar

logging.basicConfig(level=logging.INFO)

class Celcat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def edt(self, ctx):
        c = Calendar()
        c.fetch()
        await ctx.send(c.next_course())

class Chiffer(commands.Cog):
    regex = re.compile(r'\w*crypt(é|e|age)\w*', re.IGNORECASE)

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        match = self.regex.search(message.content)
        if match:
            await message.reply(
                '« {} » n’est pas français : https://chiffrer.info/'.format(match.group()),
                mention_author=True
            )

            
bot = commands.Bot(command_prefix=':')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.add_cog(Chiffer(bot))
bot.add_cog(Celcat(bot))
bot.run(cfg['discord']['token'])
