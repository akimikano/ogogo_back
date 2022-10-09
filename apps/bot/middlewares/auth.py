from telebot import BaseMiddleware
from telebot.types import (
    Message, CallbackQuery
)
from telebot.util import update_types
from typing import Union
from loguru import logger
from apps.bot.models import UserBot


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        super(AuthMiddleware, self).__init__()
        self.update_sensitive = False
        self.update_types = ['message', 'callback_query']

    def pre_process(self, message: Union[Message, CallbackQuery], data):
        logger.debug(message.text)
        user_data = message.from_user.to_dict()
        message.u, message.is_created = UserBot.get_user_and_created(user_data)
        if isinstance(message, Message):
            if '/start' in message.text:
                # id_profile = message.g()
                # if not id_profile:
                #     await message.answer("Запустите бота по ссылке с сайта.")
                #     raise CancelHandler()

                parent = message.text.split()
                if len(parent) == 2:
                    parent_id = parent[1]
                    if parent_id.isdigit() and message.is_created:
                        message.u.parent = UserBot.objects.get_or_none(id=parent_id)
                        message.u.save()
                        data['parent'] = message.u.parent

    def post_process(self, message: Message, data, exception):
        pass
