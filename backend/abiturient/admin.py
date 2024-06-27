from django.contrib import admin

from abiturient.models import Exams, Speciality, StudyDirection


@admin.register(Exams)
class ExamsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(StudyDirection)
class StudyDirectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_filter = ['code']
    search_fields = ['code']


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'degree', 'lot_of_budgets', 'lot_of_extrabudgets']
    list_filter = ['main_subjects', 'choice_subjects', 'degree']
    list_editable = ['description', 'lot_of_extrabudgets', 'lot_of_budgets']
    ordering = ('-name', 'id')
    search_fields = ['name']
    readonly_fields = ['total_number_of_places']
