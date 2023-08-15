
from django.urls import path
from .import views

app_name='fees'

urlpatterns = [
    path('fees-register', views.FeesView.as_view(),name="fees-register"),
    path('fees-update/<str:id>', views.UpdateFee.as_view(), name="fees-update"),
    
    path('fees-get_updateForm/<str:id>',views.get_updateForm, name="fees-get_updateForm"),
    
    path('fees-get_updateForm-register/<str:id>',
         views.get_updateFormbase, name="fees-get_updateForm-register"),
    
    path('fees-delete', views.FeesView.as_view(),name="fee-delete"),
    
    path('fees-management', views.manage_fees, name="fees-management"),
    
    path('fee-check-remaining', views.check_fee_remain,name="fee-check-remaining"),
    path('fees-get_updateForm-register/fee-check-remaining', views.check_fee_remain,name="fee-check-remaining"),
    
    path('check_fee_student_type', views.check_fee_student_type,name="check_fee_student_type"),
    path('fees-get_updateForm-register/check_fee_student_type', views.check_fee_student_type,name="check_fee_student_type"),
    
    path('clear', views.clear,name="clear"),
    path('fees-filter', views.fee_filter,name="fees-filter"),
]
