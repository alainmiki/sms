from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField,CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from adminhod.models import CustomUser
Categories = [('SPORT', 'sport'), ('WAR', 'war'), ('FILM', 'film'),
              ('EVENT', 'event'), ('ACIDENT', 'acident'), ('MUSIC', 'music')]

class BlogpostManager(models.Manager):
    def published(self):
        now = timezone.now()
        return self.get_queryset().filter(pub_date__lte=now)

    def get_by_natural_key(self, user, content, pub_date):
        return (self.user,self.content, self.pub_date)


class Blogpost(models.Model):
    # category=models.CharField(max_length=10,choices=Categories)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    # file=models.FileField(upload_to="uploads/",default='path not found',blank=True,null=True,)
    # title=models.CharField(max_length=100)
    content=RichTextField()
    # content=RichTextUploadingField()
    pub_date=models.DateTimeField(auto_now=False,auto_now_add=True,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    status=models.BooleanField(null=True,blank=True)


    objects=BlogpostManager()
    def top3comment(self):
        return self.objects.all()[:3]
    class Meta:
        ordering=('-pub_date',)
        unique_together = [['user','pub_date', 'content']]
        # unique_together = [['category', 'user','file', 'title','pub_date', 'content']]
    def natural_key(self):
        return (self.user,self.content,self.pub_date)

        
    def __str__(self):
        return str(self.user)
    def get_absolute_url(self):
        return reverse("Blogpost", kwargs={"pk": self.pk,'content':self.content})
   
    

class Comment(models.Model):
    blog_post=models.ForeignKey(Blogpost,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text=models.TextField()
    create_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.blog_post)
    def top3comment(self):
        return self.objects.all()[:3]
    class Meta:
        ordering=('-create_date',)


class ReplyComment(models.Model):
    blog_post=models.ForeignKey(Comment,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text=models.TextField()
    create_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.blog_post)
    
    def top3comment(self):
        return self.objects.all()[:3]

    class Meta:
        ordering=('-create_date',)



class LikeComment(models.Model):
    blog_post=models.ForeignKey(Comment,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    like=models.IntegerField()
    create_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)

class LikeCommentReply(models.Model):
   
    blog_post=models.ForeignKey(ReplyComment,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    like=models.IntegerField()
    create_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)


class Like(models.Model):
    blog_post=models.ForeignKey(Blogpost,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    like=models.IntegerField()
    create_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)
        
