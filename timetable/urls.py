from django.urls import path 
from . import views
app_name='timetable'
urlpatterns = [
    path("",views.TimeTableView.as_view(),name="timetable-reg"),
    path("<int:id>",views.TimeTableView.as_view(),name="timetable-reg"),

    path("set-period",views.SetPeriods.as_view(),name="period-reg"),
    path("update-period/<int:id>",views.SetPeriods.as_view(),name="update-period"),
    # path("automate-timetable",views.automate_timetable,name="automate-timetable"),
    
    path("output-timetables",views.TimeTableOutputView.as_view(),name="output-timetables"),
    path("clear",views.TimeTableOutputView.as_view(),name="clear"),
    path("timetable-class-filter",views.timetable_class_filter,name="timetable-class-filter"),
    path("timetable-staff-filter",views.timetable_staff_filter,name="timetable-staff-filter"),
    path("get_by/<str:get_by>",views.get_by_view,name="get_by"),
]

