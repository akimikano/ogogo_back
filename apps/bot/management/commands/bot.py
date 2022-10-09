import logging
from django.core.management.base import BaseCommand, CommandError
import os
from apps.bot.init_bot import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Бот запущен')
        bot.infinity_polling(logger_level=logging.DEBUG, long_polling_timeout=20)
