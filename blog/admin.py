from django.contrib import admin

from blog.models import Blogpost, Comment, Like, LikeComment, ReplyComment,LikeCommentReply

# Register your models here.
class BlogpostAdmin(admin.ModelAdmin):
    list_display=['user','pub_date','status']

class CommentAdmin(admin.ModelAdmin):
    list_display=['blog_post','user','create_date',]
admin.site.register(Blogpost,BlogpostAdmin)
admin.site.register(Comment,CommentAdmin)


admin.site.register(LikeComment,CommentAdmin)
admin.site.register(ReplyComment,CommentAdmin)

admin.site.register(Like,CommentAdmin)
admin.site.register(LikeCommentReply)