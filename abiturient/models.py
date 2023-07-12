import types

from django.db import models
from multiselectfield import MultiSelectField

STATUSES = (
    ('0', 'Магистратура'),
    ('1', 'Специалитет'),
    ('2', 'Бакалавриат')
)

STUDY_FORMS = ((1, 'Очная'),
               (2, 'Заочная'),
               (3, 'Очно-заочная'))
class Exams(models.Model):
    name = models.CharField(max_length=65, unique=True, verbose_name='Предмет ЕГЭ')
    slug = models.CharField(max_length=18, unique=True, db_index=True, verbose_name="Для работы в телеграмме")

    class Meta:
        verbose_name = 'Предмет ЕГЭ'
        verbose_name_plural = 'Предметы ЕГЭ'

    @property
    def combine_name_slug(self) -> tuple:
        return (self.name, self.slug)

    def __str__(self):
        return f'{self.name}'


class StudyDirection(models.Model):
    name = models.CharField(max_length=65, unique=True, verbose_name='Направление')
    description = models.TextField(max_length=250, verbose_name='описание направление', blank=True)
    code = models.CharField(max_length=3, unique=True,  verbose_name='Код направления', blank=True)
    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f'{self.name}'


class Speciality(models.Model):
    name = models.CharField(max_length=140, unique=True, verbose_name='Специальность')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код специальности')
    description = models.TextField(max_length=250, verbose_name='описание специальности', blank=True)
    main_subjects = models.ManyToManyField(to=Exams, verbose_name='основные предметы ЕГЭ для поступления',
                                           related_name='main_subjects')
    choice_subjects = models.ManyToManyField(to=Exams, verbose_name='предметы на выбор ЕГЭ для поступления',
                                             related_name='choice_subjects')
    study_forms = MultiSelectField(choices=STUDY_FORMS,max_choices=3, max_length=5)

    field_of_study = models.ForeignKey(to=StudyDirection, on_delete=models.CASCADE,
                                       verbose_name='направление поступления')
    lot_of_budgets = models.IntegerField(verbose_name='количество бюджетных мест', blank=True, default=5)
    lot_of_extrabudgets = models.IntegerField(verbose_name='количество внебюджетных мест', blank=True, default=5)

    degree = models.CharField(max_length=70, choices=STATUSES, verbose_name='Вид Обучения')

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    @property
    def total_number_of_places(self):
        return self.lot_of_budgets.real + self.lot_of_extrabudgets.real

    total_number_of_places.fget.short_description = 'Общее количество мест'

    def __str__(self):
        return self.name + 'вид:' + self.degree
# Create your models here.
