from django.contrib import admin

from library.models import Assignment, DocumentOfStaff, Library, Pass_Question

# Register your models here.

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Pass_Question)
class Pass_QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(DocumentOfStaff)
class DocumentOfStaffAdmin(admin.ModelAdmin):
    pass

