# Generated by Django 4.0.6 on 2022-10-09 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBot',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name='Telegram ID')),
                ('username', models.CharField(blank=True, max_length=32, null=True, verbose_name='Имя пользователя')),
                ('first_name', models.CharField(max_length=256, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Фамилия')),
                ('language_code', models.CharField(blank=True, help_text="Telegram client's lang", max_length=8, null=True, verbose_name='Язык')),
                ('deep_link', models.CharField(blank=True, max_length=64, null=True, verbose_name='Диплинк')),
                ('is_accepted', models.BooleanField(default=False, verbose_name='Подтвержден')),
                ('is_blocked_bot', models.BooleanField(default=False, verbose_name='Заблокированный')),
                ('is_bot', models.BooleanField(default=False, verbose_name='Бот')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админ')),
                ('django_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
