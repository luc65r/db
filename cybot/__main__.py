from .config import cfg
import discord
from discord.ext import typed_commands as commands
import asyncio
import logging
import arrow
import re
from typing import Optional

from cybot.celcat import Calendar
from cybot.svg_calendar import SvgCalendar, CalendarTheme

logging.basicConfig(level=logging.INFO)


class Celcat(commands.Cog[commands.Context]):
    def __init__(self, bot: commands.Bot[commands.Context]) -> None:
        self.bot = bot

    @commands.command()
    async def edt(
        self, ctx: commands.Context, group: int = 1, date: Optional[str] = None
    ) -> None:
        logging.info(f"{ctx.author} asked for edt")
        if date is None:
            c = SvgCalendar(None, group, 23, 30, 45, 235, 1, CalendarTheme())
        else:
            try:
                d = arrow.get(date, locale="fr", tzinfo="Europe/Paris")
            except arrow.parser.ParserError:
                await ctx.send(f"La date est invalide")
                return

            c = SvgCalendar(d, group, 23, 30, 45, 235, 1, CalendarTheme())

        await ctx.send(file=discord.File("edt.png"))


class Chiffer(commands.Cog[commands.Context]):
    regex = re.compile(r"\b(\w*en)?crypt(?!ed\b)(?!ing\b)\w+", re.IGNORECASE)

    def __init__(self, bot: commands.Bot[commands.Context]) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return

        match = self.regex.search(message.content)
        if match:
            logging.info(f'{message.author} a dit "crypt*"')
            await message.reply(
                f"« {match.group()} » n’est pas français : https://chiffrer.info/",
                mention_author=True,
            )


class Amimir(commands.Cog[commands.Context]):
    def __init__(self, bot: commands.Bot[commands.Context]) -> None:
        self.bot = bot

    @commands.command()
    async def amimir(self, ctx: commands.Context) -> None:
        logging.info(f"{ctx.author} amimir")
        await ctx.send("https://tenor.com/view/a-mimir-gif-18858209")


bot = commands.Bot(command_prefix=":")


@bot.event
async def on_ready() -> None:
    logging.info(f"We have logged in as {bot.user}")


bot.add_cog(Chiffer(bot))
bot.add_cog(Celcat(bot))
bot.add_cog(Amimir(bot))
bot.run(cfg["discord"]["token"])
