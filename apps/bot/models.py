from django.db import models
from loguru import logger

nb = {'blank': True, 'null': True}


class UserBot(models.Model):
    id = models.PositiveBigIntegerField('Telegram ID', primary_key=True)  # telegram_i
    username = models.CharField('Имя пользователя', max_length=32, **nb)
    first_name = models.CharField('Имя', max_length=256)
    last_name = models.CharField('Фамилия', max_length=256, **nb)
    language_code = models.CharField('Язык', max_length=8, help_text="Telegram client's lang", **nb)
    deep_link = models.CharField('Диплинк', max_length=64, **nb)
    is_accepted = models.BooleanField('Подтвержден', default=False)
    is_blocked_bot = models.BooleanField('Заблокированный', default=False)
    is_bot = models.BooleanField('Бот', default=False)
    is_admin = models.BooleanField('Админ', default=False)
    django_user = models.OneToOneField('users.User', models.CASCADE, **nb)

    @classmethod
    def init_kwargs(cls, arg_dict):
        model_fields = [f.name for f in cls._meta.get_fields()]
        return {k: v for k, v in arg_dict.items() if k in model_fields}

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id):
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @classmethod
    def get_user_and_created(cls, user_data):
        """ python-telegram-bot's Update, Context --> User instance """
        data = cls.init_kwargs(user_data)

        u, created = cls.objects.update_or_create(defaults=data, id=data['id'])

        logger.info(f"User {u.tg_str} created: {created}")
        return u, created
