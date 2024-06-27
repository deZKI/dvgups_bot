from aiogram import Router, types, Dispatcher

from tgbot.bot.utils.decorators import telegram_user_validation
from tgbot.bot.messages import (
    send_go_main_menu,
    send_spo_info,
    send_ega_options,
    send_ega_choice_options,
    send_specialities,
    send_speciality_info
)


async def menu(callback: types.CallbackQuery) -> None:
    if callback.data == 'MENU':
        await send_go_main_menu(callback)
    elif callback.data == 'SPO':
        await send_spo_info(callback.message.chat.id)
    elif callback.data == 'EGA':
        await send_ega_options(callback)
    elif callback.data.endswith('M'):
        await send_ega_choice_options(callback)
    elif callback.data.endswith('C'):
        await send_specialities(callback)
    elif callback.data.endswith('S'):
        await send_speciality_info(callback)
    else:
        print(callback.data.endswith('M'))


def register_handlers(dp: Dispatcher) -> None:
    router = Router()
    router.callback_query.register(telegram_user_validation(menu))
    dp.include_router(router)
