"""sms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .import views
from .views import CertificatesView, Document_staff, PostStreem, activities_view, decline_admission, events, gallery_view, notify,full_notification,Approve_admissions,librarybooks,past_questions,past_questions_view,librarybooks_view,OnlineFeesPay, showFeeForm, staffdocument_view, student_government

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("schoolinfo.urls")),
    # path("ckeditor/",include("ckeditor_uploader.urls")),
    path("adminhod/", include("adminhod.urls")),
    path("staff/", include("teacher.urls")),
    path("guardian/", include("guardian.urls")),
    path("student/", include("student.urls")),
    path("attendance/", include("attendance.urls")),
    path("fees/", include("fees.urls")),
    path("marks/", include("marks.urls")),
    path("blog/", include("blog.urls")),
    path("notification/", include("notification.urls")),
    path("timetable/", include("timetable.urls")),
    
    
    path("books", librarybooks,name='books'),
    path("past-question", past_questions,name='past-question'),
    path("past-question-view/<int:id>", past_questions_view,name='past-question-view'),
    path("book-view/<int:id>", librarybooks_view,name='book-view'),
    path("events", events,name='events'),
    path("staffdocument-view/<int:id>", staffdocument_view,name='staffdocument-view'),
    path("staff-document", Document_staff,name='staff-document'),
    path("gallery", gallery_view,name='gallery'),
    path("student-government", student_government,name='student-government'),
    path("activities", activities_view,name='activities'),
    
    
    path("certificate", CertificatesView.as_view(),name='certificate'),
    
    
    path("fees-pay-online", OnlineFeesPay.as_view(), name='fees-pay-online'),
    path("show-fee-form",showFeeForm, name='show-fee-form'),
    path('fee-check-remaining', views.check_fee_remain,name="fee-check-remaining"),
    path('check_fee_student_type', views.check_fee_student_type,name="check_fee_student_type"),
    
    
    path("stream", PostStreem.as_view(), name='stream'),
    path("news", views.news, name='news'),
    path("get_receipt", views.get_receipt, name='get_receipt'),
    path("get_receipt/<str:name>", views.get_receipt, name='get_receipt'),
    path('admission-approve', Approve_admissions.as_view(), name="admission-approve"),
    path('admission-approve-candidate<int:id>', Approve_admissions.as_view(), name="admission-approve-candidate"),
    path('admission-decline-candidate<int:id>', decline_admission, name="admission-decline-candidate"),
    
    # apis url
    path('api/', include('apis.urls')),
]
# urlpatterns +=static(settings.STATIC_URL,
#                         document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL,
#                         document_root=settings.MEDIA_ROOT)
