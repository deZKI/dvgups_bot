import logging
import sys
import asyncio

from django.core.management.base import BaseCommand

from tgbot.bot.consts import dp, bot
from tgbot.bot.handlers import register_handlers


def main():
    register_handlers(dp)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))


class Command(BaseCommand):
    help = 'Абитуриент ДВГУПС'

    def handle(self, *args, **kwargs) -> None:
        main()
