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
        logging.info(f'{ctx.author} asked for edt')
        c = Calendar()
        c.fetch()
        await ctx.send(f'```\n{c.next_course()}\n```')

class Chiffer(commands.Cog):
    regex = re.compile(r'\w*crypt(?!ed\b)(?!ing\b)\w+', re.IGNORECASE)

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        match = self.regex.search(message.content)
        if match:
            logging.info(f'{message.author} a dit "encrypt*"')
            await message.reply(
                f'« {match.group()} » n’est pas français : https://chiffrer.info/',
                mention_author=True
            )

            
bot = commands.Bot(command_prefix=':')

@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')

bot.add_cog(Chiffer(bot))
bot.add_cog(Celcat(bot))
bot.run(cfg['discord']['token'])
