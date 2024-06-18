from django.contrib import admin
from main.models import Mailing, Client, Letter, TryMailing

# admin.site.register(Mailing)
# admin.site.register(Client)
# admin.site.register(Letter)
# admin.site.register(TryMailing)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'comment')
    search_fields = ('email', 'fullname', 'comment')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('first_sent', 'periodicity', 'status')
    list_filter = ('periodicity', 'status')
    search_fields = ('first_sent', 'periodicity', 'status')


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
    search_fields = ('title', 'body')


@admin.register(TryMailing)
class TryMailingAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'status_try', 'answer')
    list_filter = ['status_try']
    search_fields = ('last_try', 'status_try', 'answer')