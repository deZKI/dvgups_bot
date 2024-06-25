# Generated by Django 4.2.2 on 2023-07-09 13:33

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, unique=True, verbose_name='Предмет ЕГЭ')),
                ('slug', models.CharField(db_index=True, max_length=18, unique=True, verbose_name='Для работы в телеграмме')),
            ],
            options={
                'verbose_name': 'Предмет ЕГЭ',
                'verbose_name_plural': 'Предметы ЕГЭ',
            },
        ),
        migrations.CreateModel(
            name='StudyDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, unique=True, verbose_name='Направление')),
                ('description', models.TextField(blank=True, max_length=250, verbose_name='описание направление')),
                ('code', models.CharField(blank=True, max_length=3, unique=True, verbose_name='Код направления')),
            ],
            options={
                'verbose_name': 'Направление',
                'verbose_name_plural': 'Направления',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, unique=True, verbose_name='Специальность')),
                ('code', models.CharField(blank=True, max_length=20, unique=True, verbose_name='Код специальности')),
                ('description', models.TextField(blank=True, max_length=250, verbose_name='описание специальности')),
                ('study_forms', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Очная'), (2, 'Заочная'), (3, 'Очно-заочная')], max_length=3)),
                ('lot_of_budgets', models.IntegerField(blank=True, default=5, verbose_name='количество бюджетных мест')),
                ('lot_of_extrabudgets', models.IntegerField(blank=True, default=5, verbose_name='количество внебюджетных мест')),
                ('degree', models.CharField(choices=[('0', 'Магистратура'), ('1', 'Специалитет'), ('2', 'Бакалавриат')], max_length=70, verbose_name='Вид Обучения')),
                ('choice_subjects', models.ManyToManyField(related_name='choice_subjects', to='abiturient.exams', verbose_name='предметы на выбор ЕГЭ для поступления')),
                ('field_of_study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abiturient.studydirection', verbose_name='направление поступления')),
                ('main_subjects', models.ManyToManyField(related_name='main_subjects', to='abiturient.exams', verbose_name='основные предметы ЕГЭ для поступления')),
            ],
            options={
                'verbose_name': 'Специальность',
                'verbose_name_plural': 'Специальности',
            },
        ),
    ]
