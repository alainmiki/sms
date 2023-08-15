
from django.urls import path
from . import views
app_name='marks'
urlpatterns = [
    path('',views.MarksGenView.as_view(),name='record-marks'),
    path('record-marks_fill/<int:mk_id>/<str:id>/<str:c_value>',views.MarksFilling.as_view(),name='record-marks_fill'),
    path('get-fill-input/<int:mk_id>/<str:id>/<str:c_value>',views.MarksFilling.as_view(),name='get-marks_fill-input'),
    # path('',views.MarksView.as_view(),name='record-marks'),
    path('update-marks/<int:id>',views.MarksUpdateView.as_view(), name='update-marks'),
    # path('update-htmx-marks/<int:id>',
        #  views.MarksUpdateHtmxView.as_view(), name='update-htmx-marks'),
    path('filter-marks', views.mark_filter, name='filter-marks'),
    path('filter-by',views.filterBy,name='filter-by'),
    path('manage-marks', views.manage_marks, name='manage-marks'),
    path('guardian-manage-marks', views.guardian_marks_home, name='guardian-manage-marks'),
    path('guardian-get-marks', views.get_marks_byChild_name, name='guardian-get-marks'),
    
    path('delete-marks', views.MarksView.as_view(), name='delete-marks'),
    
    path('report-card', views.ReportCardView.as_view(), name='report-card'),
    

]

