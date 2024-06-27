from django.db import models

from abiturient.models import Exams
from tgbot.models import TelegramUser


class Mailing(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название рассылки')
    message = models.TextField(verbose_name='Сообщение для рассылки')
    exams = models.ManyToManyField(to=Exams, verbose_name='Экзамены', related_name='mailings')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    sent = models.BooleanField(default=False, verbose_name='Отправлено')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingRecipient(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='recipients')
    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='mailings')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
