from django.contrib import admin

from schoolinfo.models import  Activity, SchoolInformation


# Register your models here.

class schoolInformationAdmin(admin.ModelAdmin):
    list_display = ['school_name_abbreviation', 'address']
    list_display_links = ['school_name_abbreviation', 'address']
    ordering = ['school_name_abbreviation']
    # actions = [make_published]


admin.site.register(SchoolInformation, schoolInformationAdmin)
admin.site.register(Activity)

