# Generated by Django 4.2.2 on 2023-07-09 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abiturient', '0003_alter_speciality_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciality',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='Код специальности'),
        ),
    ]