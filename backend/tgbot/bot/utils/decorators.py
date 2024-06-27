from typing import Callable, Any
from aiogram import types

from tgbot.models import TelegramUser
from tgbot.bot.messages import send_ban_message


def telegram_user_validation(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(event: types.Message) -> None:
        tg_user = event.from_user
        user, created = await TelegramUser.objects.aget_or_create(telegram_id=tg_user.id, name=tg_user.first_name)
        if user.is_banned:
            await send_ban_message(event)
        else:
            await handler(event)

    return wrapper
