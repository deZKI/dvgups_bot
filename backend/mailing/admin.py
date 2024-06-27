from django.contrib import admin

from tgbot.bot.messages import send_mailing

from .models import Mailing, MailingRecipient


class MailingRecipientInline(admin.TabularInline):
    model = MailingRecipient
    extra = 0
    readonly_fields = ('tg_user', 'sent_at')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'sent')
    filter_horizontal = ('exams',)
    inlines = [MailingRecipientInline]
    actions = ['send_mailing']

    def send_mailing(self, request, queryset):
        for mailing in queryset:
            send_mailing(mailing)
        self.message_user(request, "Рассылка выполнена")

    send_mailing.short_description = "Отправить выбранные рассылки"


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'tg_user', 'sent_at')
    readonly_fields = ('mailing', 'tg_user', 'sent_at')
