from django.urls import path
from .import views
app_name="guardian"
urlpatterns = [
    path("register-guardian",views.GuardianReg.as_view(),name="register-guardian"),
    path("edit-guardian/<int:pk>",views.GuardianReg.as_view(),name="edit-guardian"),
    path('profile',views.profile, name='profile'),
    path('assignments',views.assignments, name='assignments'),
    path("delete-guardian/<int:pk>",views.GuardianDelete,name="delete-guardian"),
       path('send-guardian-notification',
         views.SendSpecialNotification.as_view(), name='notify-guardian'),
       path('child-attendance',
         views.guardian_view_child_attendance, name='child-attendance'),
       path('get-child-attendance',
         views.get_attendance_byChild_name, name='get-child-attendance'),
    
    path('send-guardians-notification',
         views.SendGeneralNotification.as_view(), name='notify-guardians'),
]
