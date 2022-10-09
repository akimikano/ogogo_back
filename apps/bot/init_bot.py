import logging
import telebot
from telebot import StateMemoryStorage
import os
from telebot import BaseMiddleware
from telebot.types import (
    Message, CallbackQuery
)
from telebot.util import update_types
from typing import Union
from loguru import logger
from apps.bot.models import UserBot
from apps.hospital.models import Hospital, HospitalUnit, WorkerQueue
from apps.users.models import User
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5746692689:AAEkQ05e-MtNq1H0mGlXVljsi6cPGswgpJU'
# API_TOKEN = '5659812696:AAFEnwIgJ2jq4b2wriorTEAGWmaI55QDNOc'
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(API_TOKEN, use_class_middlewares=True, parse_mode='HTML', state_storage=state_storage)
telebot.logger.setLevel(logging.DEBUG)
telebot.apihelper.ENABLE_MIDDLEWARE = True


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        super(AuthMiddleware, self).__init__()
        self.update_sensitive = False
        self.update_types = ['message']

    def pre_process(self, message: Union[Message, CallbackQuery], data):
        # user_data = message.from_user.to_dict()
        # message.u, message.is_created = UserBot.get_user_and_created(user_data)
        # if isinstance(message, Message):
        if '/start' in message.text:
            id_profile = message.text.split()
            user_id = None
            logger.debug(id_profile)
            if len(id_profile) < 2:
                bot.reply_to(message, 'Подключитесь к боту через ссылку')
                bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            else:
                try:
                    user_id = int(id_profile[1])
                except:
                    bot.reply_to(message, 'Подключитесь к боту через ссылку')
                    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            logger.debug('AAAAAAA')
            logger.debug(user_id)
            if not user_id:
                bot.reply_to(message, 'Подключитесь к боту через ссылку')
                bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            else:
                try:
                    user = User.objects.get(id=user_id)
                    user_data = message.from_user.to_dict()
                    message.u, message.is_created = UserBot.get_user_and_created(user_data)
                    message.u.id = message.from_user.id
                    message.u.django_user = user
                    message.u.save()
                except:
                    pass

            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Список больниц', callback_data='hospitals'))
            bot.send_message(message.chat.id,
                             'Добро пожаловать в электронную очередь Ogogo. Выберите больницу:',
                             reply_markup=keyboard)


                # parent = message.text.split()
                # if len(parent) == 2:
                #     parent_id = parent[1]
                #     if parent_id.isdigit() and message.is_created:
                #         message.u.parent = UserBot.objects.get_or_none(id=parent_id)
                #         message.u.save()
                #         data['parent'] = message.u.parent

    def post_process(self, message: Message, data, exception):
        pass


bot.setup_middleware(AuthMiddleware())


def get_hospital_markup():
    hospitals_markup = InlineKeyboardMarkup()
    hospitals = Hospital.objects.all()
    for h in hospitals:
        hospitals_markup.add(InlineKeyboardButton(h.name, callback_data=f'hospital_{h.id}'))
    return hospitals_markup


def get_units_markup(id):
    hospitals_markup = InlineKeyboardMarkup()
    hospitals = Hospital.objects.prefetch_related('hospitalunit_set').get(id=id)
    for h in hospitals.hospitalunit_set.all():
        hospitals_markup.add(InlineKeyboardButton(h.name, callback_data=f'unit_{h.id}'))
    return hospitals_markup


def get_doctors_markup(id):
    hospitals_markup = InlineKeyboardMarkup()
    hospitals = HospitalUnit.objects.prefetch_related('workers').get(id=id)
    for h in hospitals.workers.all():
        hospitals_markup.add(InlineKeyboardButton(f'{h.last_name} {h.first_name}', callback_data=f'worker_{h.id}'))
    return hospitals_markup


def queue_keyboard(id):
    hospitals_markup = InlineKeyboardMarkup()
    hospitals_markup.add(InlineKeyboardButton(f'Встать в очередь', callback_data=f'queue_{id}'))
    return hospitals_markup


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.callback_query_handler(func=lambda callback: callback.data == 'hospitals')
def echo_message(callback: CallbackQuery):
    bot.answer_callback_query(callback.id)
    logger.debug(callback.data)
    bot.send_message(callback.message.chat.id, 'Больницы:', reply_markup=get_hospital_markup())


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('hospital_'))
def echo_message(callback: CallbackQuery):
    bot.answer_callback_query(callback.id)
    logger.debug(callback.data)

    id = int(callback.data.split('_')[1])
    keyboard = get_units_markup(id)

    bot.send_message(callback.message.chat.id, 'Отделы:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('unit_'))
def echo_message(callback: CallbackQuery):
    bot.answer_callback_query(callback.id)
    logger.debug(callback.data)

    id = int(callback.data.split('_')[1])
    keyboard = get_doctors_markup(id)

    bot.send_message(callback.message.chat.id, 'Врачи:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('worker_'))
def echo_message(callback: CallbackQuery):
    bot.answer_callback_query(callback.id)
    logger.debug(callback.data)
    id = int(callback.data.split('_')[1])
    keyboard = queue_keyboard(id)
    worker = User.objects.prefetch_related('hospitalunit_set').get(id=id)
    units = []
    for i, el in enumerate(list(worker.hospitalunit_set.all())):
        units.append(f'{i + 1}. {el.name} \n')
    un = ''.join(units)
    text = f'Врач - {worker.last_name} {worker.first_name} \nОтделы работы: \n{un}'
    bot.send_message(callback.message.chat.id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('queue_'))
def echo_message(callback: CallbackQuery):
    bot.answer_callback_query(callback.id)
    logger.debug(callback.data)
    id = int(callback.data.split('_')[1])
    print(callback.message.from_user.id)
    uset_bot = UserBot.objects.select_related('django_user').get(id=int(callback.message.from_user.id))
    worker = User.objects.get(id=id)
    queue = WorkerQueue.objects.get(worker=worker)
    queue.clients.add(uset_bot.django_user)
    count = queue.clients.count()
    text = f'Вы в очереди к {worker.last_name} {worker.first_name} под номером {count}'
    bot.send_message(callback.message.chat.id, text)
