from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.contrib.postgres.aggregates import ArrayAgg
from abiturient.models import Speciality
from tgbot.bot.keyboards import MAIN_MENU
from tgbot.bot.consts import bot
from asgiref.sync import sync_to_async
from django.core.cache import cache
from .consts import (
    CACHE_TIMEOUT,
    CACHE_KEY_EGA_OPTIONS,
    CACHE_KEY_EGA_CHOICE_OPTIONS_TEMPLATE,
    CACHE_KEY_SPECIALITIES_TEMPLATE,
    CACHE_KEY_SPECIALITY_INFO_TEMPLATE,
    TEXT_BANNED,
    TEXT_MENU,
    TEXT_SPO_INFO_1,
    TEXT_SPO_INFO_2,
    TEXT_EGA_OPTIONS,
    TEXT_EGA_CHOICE_OPTIONS,
    TEXT_SPECIALITIES,
    TEXT_RUSSIAN_LANGUAGE,
    TEXT_BACK_TO_MENU,
    TEXT_BACK,
)


async def send_ban_message(event: types.Message | types.CallbackQuery) -> None:
    if isinstance(event, types.CallbackQuery):
        await bot.edit_message_text(chat_id=event.message.chat.id, message_id=event.message.message_id,
                                    text=TEXT_BANNED)
    else:
        await bot.send_message(event.chat.id, TEXT_BANNED)


async def send_main_menu(chat_id: int) -> None:
    await bot.send_message(chat_id, TEXT_MENU, reply_markup=MAIN_MENU)


async def send_go_main_menu(callback: types.CallbackQuery) -> None:
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=TEXT_EGA_OPTIONS, reply_markup=MAIN_MENU)


async def send_spo_info(chat_id: int) -> None:
    await bot.send_message(chat_id, text=TEXT_SPO_INFO_1)
    await bot.send_message(chat_id, text=TEXT_SPO_INFO_2)


async def send_ega_options(callback: types.CallbackQuery) -> None:
    buttons = []
    exams = await sync_to_async(cache.get)(CACHE_KEY_EGA_OPTIONS)

    if not exams:
        exams = await sync_to_async(
            lambda: list(Speciality.objects.filter(degree__in=['1', '2']).annotate(
                exam_names=ArrayAgg('main_subjects__name'), exam_slugs=ArrayAgg('main_subjects__slug')
            ).values_list('exam_names', 'exam_slugs').distinct())
        )()
        await sync_to_async(cache.set)(CACHE_KEY_EGA_OPTIONS, exams, CACHE_TIMEOUT)

    for exam in exams:
        btn = InlineKeyboardButton(text=TEXT_RUSSIAN_LANGUAGE + ' + '.join(exam[0]),
                                   callback_data=' + '.join(exam[1]) + 'M')
        buttons.append([btn])

    buttons.append([InlineKeyboardButton(text=TEXT_BACK_TO_MENU, callback_data='MENU')])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=TEXT_EGA_OPTIONS, reply_markup=markup)


async def send_ega_choice_options(callback: types.CallbackQuery) -> None:
    buttons = []
    main_exams_slugs = callback.data[:-1].split(' + ')
    cache_key = CACHE_KEY_EGA_CHOICE_OPTIONS_TEMPLATE.format(callback.data[:-1])
    exams = await sync_to_async(cache.get)(cache_key)

    if not exams:
        exams = await sync_to_async(
            lambda: list(Speciality.objects.annotate(
                main_subjects_list=ArrayAgg('main_subjects__slug')
            ).filter(main_subjects_list__contains=main_exams_slugs).distinct().values_list('choice_subjects__name',
                                                                                           'choice_subjects__slug'))
        )()
        await sync_to_async(cache.set)(cache_key, exams, CACHE_TIMEOUT)

    main_exams_names = await sync_to_async(
        lambda: list(Speciality.objects.filter(main_subjects__slug__in=main_exams_slugs).distinct().values_list(
            'main_subjects__name', flat=True))
    )()

    for exam in exams:
        btn = InlineKeyboardButton(text=TEXT_RUSSIAN_LANGUAGE + ' + '.join(main_exams_names) + ' + ' + exam[0],
                                   callback_data='+'.join(main_exams_slugs) + '+' + exam[1] + 'C')
        buttons.append([btn])

    buttons.append([InlineKeyboardButton(text=TEXT_BACK_TO_MENU, callback_data='MENU')])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=TEXT_EGA_CHOICE_OPTIONS, reply_markup=markup)


async def send_specialities(callback: types.CallbackQuery) -> None:
    buttons = []
    main_exams, choice_exam = callback.data[:-1].split('+')
    cache_key = CACHE_KEY_SPECIALITIES_TEMPLATE.format(main_exams, choice_exam)
    specialities = await sync_to_async(cache.get)(cache_key)

    if not specialities:
        specialities = await sync_to_async(
            lambda: list(Speciality.objects.filter(main_subjects__slug=main_exams,
                                                   choice_subjects__slug=choice_exam).distinct().values_list('name',
                                                                                                             'code'))
        )()
        await sync_to_async(cache.set)(cache_key, specialities, CACHE_TIMEOUT)

    for speciality in specialities:
        btn = InlineKeyboardButton(text=speciality[0], callback_data=speciality[1] + 'S')
        buttons.append([btn])

    buttons.append([InlineKeyboardButton(text=TEXT_BACK, callback_data=main_exams + 'M')])
    buttons.append([InlineKeyboardButton(text=TEXT_BACK_TO_MENU, callback_data='MENU')])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=TEXT_SPECIALITIES, reply_markup=markup)


async def send_speciality_info(callback: types.CallbackQuery) -> None:
    cache_key = CACHE_KEY_SPECIALITY_INFO_TEMPLATE.format(callback.data[:-1])
    speciality = await sync_to_async(cache.get)(cache_key)

    if not speciality:
        speciality = await sync_to_async(Speciality.objects.get)(code=callback.data[:-1])
        await sync_to_async(cache.set)(cache_key, speciality, CACHE_TIMEOUT)

    await bot.send_message(chat_id=callback.message.chat.id, text=speciality.name)
    await bot.send_message(chat_id=callback.message.chat.id, text=speciality.description)
