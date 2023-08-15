from django.urls import path
from .views import *
app_name="school_info"
urlpatterns = [
    # path('', SchoolInformationHome.as_view(), name="home"),
    path('', home, name="home"),
    
    path('setup-school-Information', CreateSchoolInformation.as_view(), name="setup"),
    
    path('update-school-Information/<int:id>', CreateSchoolInformation.as_view(), name="update"),
    
    path('create-activity', CreateActivities.as_view(), name="create-activity"),
    
    path('update-activity/<int:id>', CreateActivities.as_view(), name="update-activity"),
    path('delete-activity/<int:id>', delete_activity, name="delete-activity"),
    
    
    
]
