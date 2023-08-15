from django.urls import path
from . import views

app_name = "adminhod"
urlpatterns=[
    path("login", views.showLogin, name="showlogin"),
    path("logout", views.logoutView, name="logout"),
    
    path("", views.Login.as_view(), name="login"),
    
    path("signup", views.Signup.as_view(), name="signup"),
    
    path("dashboard", views.admindashbord.as_view(), name="dashboard"),
    
    path("event-register", views.EventView.as_view(), name="event-register"),
    
    path("event-update/<int:id>", views.EventView.as_view(), name="event-update"),
    
    path("events-management", views.event_management, name="events-management"),
    
    path("gallery", views.GalleryView.as_view(), name="gallery"),
    
    path("register-admin", views.AddAministrators.as_view(), name="register-admin"),
    
    path("update-admin/<int:id>", views.AddAministrators.as_view(), name="update-admin"),
    
    path("delete-admin/<int:id>", views.deleteAdminstrator, name="delete-admin"),
    path("show_or_hide_form", views.show_or_hide_form, name="show-or-hide-form"),
    path("show-or-hide-library-form", views.show_or_hide_library_form, name="show-or-hide-library-form"),
    path("show-or-hide-question-form", views.show_or_hide_question_form, name="show-or-hide-question-form"),
    path("show-or-hide-staffdocument-form", views.show_or_hide_staffdocument_form, name="show-or-hide-staffdocument-form"),
    
    path("library-create", views.CreateBook.as_view(), name="library-create"),
    path("library-update/<int:id>", views.CreateBook.as_view(), name="library-update"),
    path("library-delete/<int:id>", views.delete_book, name="library-delete"),
    
    path("pass_question-create", views.CreateQuestion.as_view(), name="pass_question-create"),
    path("pass_question-update/<int:id>", views.CreateQuestion.as_view(), name="pass_question-update"),
    path("pass_question-delete/<int:id>", views.delete_book, name="pass_question-delete"),
    
    path("staff-document-create", views.CreateStaffDocument.as_view(), name="staff-document-create"),
    path("staff-document-update/<int:id>", views.CreateStaffDocument.as_view(), name="staff-document-update"),
    path("staff-document-delete/<int:id>", views.delete_staff_document, name="staff-document-delete"),
    
    path("password-store", views.passwordStorView.as_view(), name="password-store"),
    path("password-resend/<int:id>", views.resend_password, name="password-resend"),
    
    
    path("manage_admins", views.AddAministrators.as_view(), name="manage_admins"),
    path("student-id-card", views.studentIdgen.as_view(), name="student-id-card"),
    path("staff-id-card", views.staffIDView, name="staff-id-card"),
    path("admin-id-card", views.adminIDView, name="admin-id-card"),
    
    
]

