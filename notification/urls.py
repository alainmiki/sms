
from django.urls import include, path
from .views import events, notify,full_notification
app_name='notification'
urlpatterns = [
    
    path("notify", notify, name='get-notifi'),
    path("notifications", full_notification, name='notifications'),
    path("notifications/<int:id>", full_notification, name='notifications-status'),
]
