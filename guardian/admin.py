from django.contrib import admin

from guardian.models import Guardian, NotificationGuardian

# Register your models here.

admin.site.register(Guardian)
admin.site.register(NotificationGuardian)