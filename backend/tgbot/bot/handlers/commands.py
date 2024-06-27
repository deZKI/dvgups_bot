from aiogram import Dispatcher, Router, types
from aiogram.filters import Command

from tgbot.bot.consts import WELCOME_MESSAGE
from tgbot.bot.messages import send_main_menu
from tgbot.bot.utils.decorators import telegram_user_validation


async def command_start(message: types.Message) -> None:
    await message.answer(WELCOME_MESSAGE,
                         reply_markup=types.ReplyKeyboardRemove())
    await send_main_menu(message.from_user.id)


async def command_menu(message: types.Message) -> None:
    await send_main_menu(message.from_user.id)


def register_handlers(dp: Dispatcher) -> None:
    router = Router()
    router.message.register(telegram_user_validation(command_start), Command(commands=['start']))
    router.message.register(telegram_user_validation(command_menu), Command(commands=['menu']))
    dp.include_router(router)
