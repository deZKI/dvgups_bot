# Generated by Django 4.2.2 on 2024-06-27 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('abiturient', '0001_initial'),
        ('tgbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название рассылки')),
                ('message', models.TextField(verbose_name='Сообщение для рассылки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('sent', models.BooleanField(default=False, verbose_name='Отправлено')),
                ('exams', models.ManyToManyField(related_name='mailings', to='abiturient.exams', verbose_name='Экзамены')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='mailing.mailing')),
                ('tg_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to='tgbot.telegramuser')),
            ],
            options={
                'verbose_name': 'Получатель рассылки',
                'verbose_name_plural': 'Получатели рассылки',
            },
        ),
    ]
