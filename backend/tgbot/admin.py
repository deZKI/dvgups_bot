from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', 'username', 'is_banned']
    list_editable = ['is_banned']
    list_filter = ['is_banned']
