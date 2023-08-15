from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from adminhod.models import AdminHOD, CustomUser, Event, Gallery, PasswordStore

# Register your models here.


class CustomUserModel(UserAdmin):
    list_display = ['email', 'username', 'created_at', 'last_login']
    search_fields = ['email', 'username', 'first_name']
    readonly_fields = ['id', 'created_at', 'last_login']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CustomUser, CustomUserModel)
admin.site.register(AdminHOD)
admin.site.register(Event)
admin.site.register(Gallery)
admin.site.register(PasswordStore)
