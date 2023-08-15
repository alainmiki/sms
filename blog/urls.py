from django.urls import path
from . import views
app_name='blog'
urlpatterns=[
    path('',views.blog_home.as_view(),name='blog_home'),
    path('detail/<int:id>',views.blog_post_details,name='blog_post_details'),
    path('delete/<int:id>',views.blog_post_delete,name='blog_post_delete'),
    path ('create',views.blog_post_create,name='create_post'),
    path ('update/<int:id>',views.blog_post_update,name='blog_post_update'),
   
    
    path('comments/<int:id>',views.comment,name='comments'),

    path('replycomments/<int:id>',views.replycomments,name='replycomments'),

    path('likescomments/<int:id>',views.likescomments,name='likescomments'),
    
    path('likescomment-Reply/<int:id>',views.likescommentreply,name='likescommentreply'),


    path('like/<int:id>',views.likes,name='likes'),
 
    

]