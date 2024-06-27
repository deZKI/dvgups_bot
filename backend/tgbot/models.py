from django.db import models

from abiturient.models import Exams


class TelegramUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='имя в телеграмме', blank=True)
    username = models.CharField(max_length=64, verbose_name='ник в телеграмме', blank=True)
    is_banned = models.BooleanField(verbose_name='забанен', default=False)
    history = models.JSONField(default=dict, blank=True)

    subjects = models.ManyToManyField(to=Exams, verbose_name='предметы ЕГЭ для поступления')

    def __str__(self):
        return f'id: {self.telegram_id} - {self.name}'

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'
