import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import Throttled
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models.functions import Concat
from django.db.models import F, Value, Q
from django.db.models import ArrayAgg

from backend.tgbot.models import TelegramUser
from backend.abiturient.models import Speciality, Exams

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

MENU = 'MENU'
EGA = 'EGA'
SPO = 'SPO'
EGA_MAIN_EXAM = 'M'
EGA_CHOICE_EXAM = 'C'
SPECIALITY = 'S'

markup_menu = InlineKeyboardMarkup()
markup_menu.add(InlineKeyboardButton(text='Выбор по ЕГЭ', callback_data=EGA))
markup_menu.add(InlineKeyboardButton(text='Поступить по СПО', callback_data=SPO))

markup_back = InlineKeyboardMarkup()
markup_back.add(InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))


async def telegram_user_validation(handler):
    async def wrapper(event: types.Message):
        tg_user = event.from_user
        user, created = await TelegramUser.objects.aget_or_create(telegram_id=tg_user.id, name=tg_user.first_name)
        if user.is_banned:
            if isinstance(event, types.CallbackQuery):
                await bot.edit_message_text(chat_id=event.message.chat.id, message_id=event.message.message_id, text='Вы забанены')
            else:
                await bot.send_message(event.chat.id, 'Вы забанены')
        else:
            await handler(event)
    return wrapper


@dp.message_handler(commands=['start'])
@telegram_user_validation
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать на официальный Aбитуриент ДВГУПС Бот!', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, 'Меню', reply_markup=markup_menu)


@dp.message_handler(commands=['menu'])
@telegram_user_validation
async def command_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Меню', reply_markup=markup_menu)


@dp.callback_query_handler(lambda callback: callback.data)
@telegram_user_validation
async def menu(callback: types.CallbackQuery):
    # выход в главное меню
    if callback.data == MENU:
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Меню', reply_markup=markup_menu)
    elif callback.data == SPO:
        await bot.send_message(chat_id=callback.message.chat.id, text='Здесь рассказано про поступление после СПО\nhttps://vk.com/dvgupspriemnayakomissia')
        await bot.send_message(chat_id=callback.message.chat.id, text='https://t.me/abiturientdvgups')
    elif callback.data == EGA:
        markup = InlineKeyboardMarkup()
        exams = Speciality.objects.filter(degree__in=['1', '2']).annotate(
            exam_names=ArrayAgg('main_subjects__name'), exam_slugs=ArrayAgg('main_subjects__slug')
        ).values_list('exam_names', 'exam_slugs').distinct()

        for exam in exams:
            btn = InlineKeyboardButton(text='Рус. язык + ' + ' + '.join(exam[0]), callback_data=' + '.join(exam[1]) + EGA_MAIN_EXAM)
            markup.add(btn)

        markup.add(InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Выберите основные экзмены', reply_markup=markup)
    elif callback.data[-1] == EGA_MAIN_EXAM:
        markup = InlineKeyboardMarkup()
        main_exams_slugs = callback.data[:-1].split(' + ')

        exams = Speciality.objects.annotate(
             main_subjects_list=ArrayAgg('main_subjects__slug')
        ).filter(main_subjects_list__contains=main_exams_slugs).distinct().values_list('choice_subjects__name', 'choice_subjects__slug')

        main_exams_names = list(Speciality.objects.filter(main_subjects__slug__in=main_exams_slugs).distinct().values_list('main_subjects__name', flat=True))

        for exam in exams:
            btn = InlineKeyboardButton(text='Рус. язык + ' + ' + '.join(main_exams_names) + ' + ' + exam[0], callback_data='+'.join(main_exams_slugs) + '+' + exam[1] + EGA_CHOICE_EXAM)
            markup.add(btn)

        markup.add(InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Выберите Доп экзмены', reply_markup=markup)
    elif callback.data[-1] == EGA_CHOICE_EXAM:
        markup = InlineKeyboardMarkup()
        main_exams, choice_exam = callback.data[:-1].split('+')

        specialities = Speciality.objects.filter(main_subjects__slug=main_exams, choice_subjects__slug=choice_exam).distinct().values_list('name', 'code')

        for speciality in specialities:
            btn = InlineKeyboardButton(text=speciality[0], callback_data=speciality[1] + SPECIALITY)
            markup.add(btn)

        markup.add(InlineKeyboardButton(text='Вернуться назад', callback_data=main_exams + EGA_MAIN_EXAM))
        markup.add(InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='СПЕЦИАЛЬНОСТИ', reply_markup=markup)
    elif callback.data[-1] == SPECIALITY:
        speciality = Speciality.objects.get(code=callback.data[:-1])
        await bot.send_message(chat_id=callback.message.chat.id, text=speciality.name)
        await bot.send_message(chat_id=callback.message.chat.id, text=speciality.description)
    else:
        print(callback.data[-1] == EGA_MAIN_EXAM)
        pass


@dp.message_handler(content_types=['text'])
async def send_text(message: types.Message):
    speciality = Speciality.objects.filter(name=message.text).first()
    if speciality:
        await bot.send_message(chat_id=message.chat.id, text=speciality.name)
        await bot.send_message(chat_id=message.chat.id, text=speciality.description)
    elif message.text == 'Вернуться в меню':
        await bot.send_message(message.from_user.id, 'Меню', reply_markup=markup_menu)
    else:
        await bot.send_message(message.from_user.id, 'не знаю такую команду')


class Command(BaseCommand):
    help = 'Абитуриент ДВГУПС'

    def handle(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(dp.start_polling())
