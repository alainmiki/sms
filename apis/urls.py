
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register('students',views.StudentModelViewset,basename='students')
router.register('staffs',views.StaffModelViewset,basename='staffs')
router.register('guardian',views.GuardianModelViewset,basename='guardian')
router.register('department',views.DepartmentModelViewset,basename='department')
router.register('class_room',views.ClassRoomtModelViewset,basename='class_room')
router.register('mark',views.MarksModelViewset,basename='mark')
router.register('events',views.EventModelViewset,basename='events')
router.register('fees',views.FeeModelViewset,basename='fees')
router.register('Attendance-Report',views.AttendanceReportModelViewset,basename='Attendance-Report')
router.register('school-info',views.SchoolInformationModelViewset,basename='school-info')

urlpatterns = [
    path('',include(router.urls)),
    path('st', views.StudentAPIView.as_view(), name='students'),
    path('<int:pk>', views.StudentAPIView.as_view(), name='students'),
]
# urlpatterns +=router.urls
