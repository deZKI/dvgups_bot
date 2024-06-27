from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_markup_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Выбор по ЕГЭ', callback_data='EGA'),
        InlineKeyboardButton(text='Поступить по СПО', callback_data='SPO')
    ]])
    return markup

MAIN_MENU = get_markup_menu()