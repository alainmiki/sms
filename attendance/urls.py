from django.urls import path
from .import views
app_name="attendance"
urlpatterns = [
    path('add-subject',views.AddSubject.as_view(),name='add-subject'),
    path('Update-subject/<int:id>',views.AddSubject.as_view(),name='Update-subject'),
    path('delete-subject/<int:id>', views.deleteSubject, name='delete-subject'),
    path('staff-take-attendance', views.StaffTakeAttendance.as_view(), name='take-attendance'),
    path('attendance-status-update/<int:a_id>/<str:s_id>', views.StaffTakeAttendance_statu_update,
         name='take-attendance-status-update'),
    
]
