import django.db.models
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.management.base import BaseCommand
from django.conf import settings

from tgbot.models import TelegramUser
from abiturient.models import Speciality, Exams
from telebot import TeleBot, types
from pathlib import Path
from django.db.models.functions import Concat
from django.db.models import F, Value
from django.db.models import Q

bot = TeleBot(token=settings.TELEGRAM_BOT_TOKEN)

MENU = 'MENU'
EGA = 'EGA'
SPO = 'SPO'

EGA_MAIN_EXAM = 'M'
EGA_CHOICE_EXAM = 'C'

SPECIALITY = 'S'

markup_menu = types.InlineKeyboardMarkup()
# markup_Menu.add(types.InlineKeyboardButton(text='Узнать про направления👋', callback_data='direction_info'),
#                 types.InlineKeyboardButton(text='Узнать про специальности', callback_data='speciality_info'))
markup_menu.add(types.InlineKeyboardButton(text='Выбор по ЕГЭ', callback_data=EGA))
markup_menu.add(types.InlineKeyboardButton(text='Поступить по СПО', callback_data=SPO))

markup_back = types.InlineKeyboardMarkup()
markup_back.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))







def telegram_user_validation(function):
    def validation(message):
        tg_user = message.from_user
        user, created = TelegramUser.objects.get_or_create(telegram_id=tg_user.id, name=tg_user.first_name)
        if user.is_banned:
            if isinstance(message, types.CallbackQuery):
                bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.id,
                                      text='Вы забанены')
            else:
                bot.send_message(message.chat.id, 'Вы забанены')
        else:
            function(message)
    return validation


@bot.message_handler(commands=['start'])
@telegram_user_validation
def command_start(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать на официальный Aбитуриент ДВГУПС Бот !', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.from_user.id, 'Меню', reply_markup=markup_menu)

@bot.message_handler(commands=['menu'])
@telegram_user_validation
def command_menu(message):
    bot.send_message(message.from_user.id, 'Меню', reply_markup=markup_menu)

@bot.callback_query_handler(func=lambda callback: callback.data)
@telegram_user_validation
def menu(callback):

    # выход в главное меню
    if callback.data == MENU:
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Меню',
                              reply_markup=markup_menu)

    elif callback.data == SPO:
        bot.send_message(chat_id=callback.message.chat.id, text='Здесь рассказано про поступление после СПО\nhttps://vk.com/dvgupspriemnayakomissia')
        bot.send_message(chat_id=callback.message.chat.id, text='https://t.me/abiturientdvgups')


    # по егэ
    elif callback.data == EGA:
        markup = types.InlineKeyboardMarkup()
        exams = Speciality.objects.filter(degree__in=['1', '2']).annotate(
            exam_names=ArrayAgg('main_subjects__name'), exam_slugs=ArrayAgg('main_subjects__slug')
        ).values_list('exam_names', 'exam_slugs').distinct()

        for exam in exams:
            btn = types.InlineKeyboardButton(text='Рус. язык + '+ ' + '.join(exam[0]), callback_data=' + '.join(exam[1]) + EGA_MAIN_EXAM)
            markup.add(btn)

        markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Выберите основные экзмены',
                              reply_markup=markup)




    #по егэ экз на выбор
    elif callback.data[-1] == EGA_MAIN_EXAM:
        markup = types.InlineKeyboardMarkup()
        main_exams_slugs = callback.data[:-1].split(' + ')

        exams = Speciality.objects.annotate(
             main_subjects_list=ArrayAgg('main_subjects__slug')
        ).filter(main_subjects_list__contains=main_exams_slugs).\
            distinct().values_list('choice_subjects__name', 'choice_subjects__slug')

        main_exams_names = list(Speciality.objects.filter(main_subjects__slug__in=main_exams_slugs).distinct().values_list(
            'main_subjects__name', flat=True))

        for exam in exams:
            btn = types.InlineKeyboardButton(text='Рус. язык + ' + ' + '.join(main_exams_names) + ' + ' + exam[0], callback_data='+'.join(main_exams_slugs) + '+' + exam[1] + EGA_CHOICE_EXAM)
            markup.add(btn)

        markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Выберите Доп экзмены',
                              reply_markup=markup)

    #выбор специальностей
    elif callback.data[-1] == EGA_CHOICE_EXAM:
        markup = types.InlineKeyboardMarkup()
        main_exams, choice_exam = callback.data[:-1].split('+')

        specialities = Speciality.objects.filter(main_subjects__slug=main_exams, choice_subjects__slug=choice_exam). \
            distinct().values_list('name', 'code')

        for speciality in specialities:
            btn = types.InlineKeyboardButton(text=speciality[0],
                                             callback_data=speciality[1] + SPECIALITY)
            markup.add(btn)

        markup.add(types.InlineKeyboardButton(text='Вернуться назад', callback_data=main_exams + EGA_MAIN_EXAM))
        markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data=MENU))
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='СПЕЦИАЛЬНОСТИ',
                              reply_markup=markup)

    elif callback.data[-1] == SPECIALITY:
        speciality = Speciality.objects.get(code=callback.data[:-1])
        bot.send_message(chat_id=callback.message.chat.id, text=speciality.name)

        bot.send_message(chat_id=callback.message.chat.id, text=speciality.description)

    else:
        print(callback.data[-1] == EGA_MAIN_EXAM)
        pass


@bot.message_handler(content_types=['text'])
def send_text(message:types.Message):
    speciality = Speciality.objects.get(name=message.text)
    if not speciality == None:
        bot.send_message(chat_id=message.chat.id, text=speciality.name)

        bot.send_message(chat_id=message.chat.id, text=speciality.description)
    elif message.text == 'Вернуться в меню':
        bot.send_message(message.from_user.id, 'Меню', reply_markup=markup_menu)
    else:
        bot.send_message(message.from_user.id, 'не знаю такую команду')


class Command(BaseCommand):
    help = 'Абитуриент ДВГУПС'
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as exception:
            print('bolt', exception)