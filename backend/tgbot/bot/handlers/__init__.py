from aiogram import Dispatcher

from .callbacks import register_handlers as register_callbacks_handlers
from .commands import register_handlers as register_commands_handlers


def register_handlers(dp: Dispatcher) -> None:
    register_commands_handlers(dp)
    register_callbacks_handlers(dp)
