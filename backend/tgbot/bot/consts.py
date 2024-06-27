from aiogram import Bot, Dispatcher
from django.conf import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

WELCOME_MESSAGE = "Добро пожаловать на официальный Aбитуриент ДВГУПС Бот"

CACHE_TIMEOUT = 60 * 60  # 1 час

# Ключи для кэширования
CACHE_KEY_EGA_OPTIONS = 'ega_options_exams'
CACHE_KEY_EGA_CHOICE_OPTIONS_TEMPLATE = 'ega_choice_options_{}'
CACHE_KEY_SPECIALITIES_TEMPLATE = 'specialities_{}_{}'
CACHE_KEY_SPECIALITY_INFO_TEMPLATE = 'speciality_info_{}'

# Тексты сообщений
TEXT_BANNED = 'Вы забанены'
TEXT_MENU = 'Меню'
TEXT_SPO_INFO_1 = 'Здесь рассказано про поступление после СПО\nhttps://vk.com/dvgupspriemnayakomissia'
TEXT_SPO_INFO_2 = 'https://t.me/abiturientdvgups'
TEXT_EGA_OPTIONS = 'Выберите основные экзмены'
TEXT_EGA_CHOICE_OPTIONS = 'Выберите Доп экзмены'
TEXT_SPECIALITIES = 'СПЕЦИАЛЬНОСТИ'
TEXT_RUSSIAN_LANGUAGE = 'Рус. язык + '
TEXT_BACK_TO_MENU = 'Вернуться в меню'
TEXT_BACK = 'Вернуться назад'