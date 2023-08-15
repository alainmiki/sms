from django.contrib import admin

from fees.models import Receipt, Fee,OnlineFeesOnProgress,ServicesTokenStorage

# Register your models here.

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):

    list_display = ['receipt_no', 'student_id', 'class_room',
                    'entry', "semester", 'amount', 'due_fee', 'total_fee']
    list_display_links = ['receipt_no', 'student_id', 'class_room',
                          'entry', "semester", 'amount', 'due_fee', 'total_fee']

admin.site.register(Receipt)
admin.site.register(OnlineFeesOnProgress)
admin.site.register(ServicesTokenStorage)