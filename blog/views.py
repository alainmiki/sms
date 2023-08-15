from django.shortcuts import get_object_or_404, redirect, render
from adminhod.models import CustomUser
from blog.forms import BlogpostForm, CommentForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from blog.models import Blogpost, Comment, Like, LikeComment, LikeCommentReply, ReplyComment
from asgiref.sync import sync_to_async
# Create your views here.


class blog_home(View):
  
    def post(self,request):
        sender=request.POST['from']
        from_email=request.POST['subject']
        from_email=request.POST['body']

        # send_mail(
        #         'Confirmation from Blog Global',
        #         'thanks for the feedback we just recieved it.',
        #         sender,
        #         ['echujbrown@gmail.com', 'alainmiki237@mail.com'],
        #         )

    
    def get(self,request):
    
        timez=timezone.now()
        posts=Blogpost.objects.published()
        
        for post in posts:
            if post.pub_date <= timezone.now():
                post.status=True
                post.save()
            else:
                post.status=False
                post.save()

        alluser=CustomUser.objects.all()
        paginator = Paginator(posts, 9)

        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        context={
            'time':timez,
            'posts':posts,
            'alluser':alluser,
            'title':'Blog Home'
        
        }
        
        return render(request,'blog/blog_home.html',context)


def blog_post_details(request,id):
    if request.user.is_authenticated:
        detailobj=get_object_or_404(Blogpost,id=id)
        comments=Comment.objects.all().order_by('-create_date')
        alluser=CustomUser.objects.all()
        context={
            'detail':detailobj,
            'comments':comments,
            'alluser':alluser
        }
        return render(request,'blog/blog_post_details.html',context)
    else:
        return redirect('blog:login')


def blog_post_update(request,id):
    obj=Blogpost.objects.get(pk=id)
    
    if request.method=='POST':
        form=BlogpostForm(request.POST or None,request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('blog:blog_home')
        
    form=BlogpostForm(request.POST or None ,instance=obj)
    context={'form':form,'title':'Create Blog',}
    # context={}
    return render(request,'blog/blog_post_create.html',context)


def blog_post_delete(request,id):
    
    update=get_object_or_404(Blogpost,id=id)
    update.delete()
    return redirect('/')

  

@login_required
def blog_post_create(request):
    if request.method == 'POST':
        
        user=Blogpost(user=request.user)
        form=BlogpostForm(request.POST,request.FILES or None,instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')

    
    initial={'user':request.user}
    context={
        'form':BlogpostForm(initial=initial),
        'title':'Create Blog',
    }
    return render(request,'blog/blog_post_create.html',context)


@login_required
def comment(request,id):
    post=Blogpost.objects.get(id=id)
    posts=post.comment_set.all()
    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page')
    compagination = paginator.get_page(page_number)
   
    if request.method=='POST':
        text=request.POST.get('text')
        print(text)
        createcomment=Comment.objects.create(text=text,blog_post_id=id,user=request.user)
        return redirect('blog:blog_post_details',post.id)

    else:
        # alluser=CustomUser.objects.all()
    
        context={
            'commentform': CommentForm(),
            'post':post,
            'posts':posts,
            # 'alluser':alluser
        }
        return render(request,'blog/comment_create.html',context)
    
@sync_to_async
@login_required
def likes(request,id):
    
    like=Like.objects.all()
    obj_to_like=get_object_or_404(Blogpost,id=id)
    User=request.user

    if like.count==0 :
        form=Like.objects.create(blog_post=obj_to_like,user=User,like=1)
        
        return redirect('blog:blog_post_details',id)


    elif obj_to_like.like_set.filter(user=User).exists():
        obj_to_like.like_set.filter(user=User).delete()
    else:
        form=Like.objects.create(blog_post=obj_to_like,user=User,like=1)
    
    return redirect('blog:blog_post_details',obj_to_like.id)
  


def replycomments(request,id):
    post=Comment.objects.get(id=id)
    if request.method=='POST':
        text=request.POST.get('text')
        createcomment=ReplyComment.objects.create(text=text,blog_post_id=id,user=request.user)
        return redirect('blog:replycomments',id)

    alluser=CustomUser.objects.all()
    context={
        'commentform': CommentForm(),
        'post':post,
        'alluser':alluser
    }
    return render(request,'blog/replycomments.html',context)
    
@sync_to_async
@login_required
def likescommentreply(request,id):
    
    likecomment=LikeCommentReply.objects.all()
    obj_to_like=get_object_or_404(ReplyComment,id=id)
    User=request.user

    
    if likecomment.count==0 :
        form=LikeCommentReply.objects.create(blog_post=obj_to_like,user=User,like=1)
        
        return redirect('blog:replycomments',id)
        


    elif obj_to_like.likecommentreply_set.filter(user=User).exists():
        obj_to_like.likecommentreply_set.filter(user=User).delete()
    else:
        form=LikeCommentReply.objects.create(blog_post=obj_to_like,user=User,like=1)
    
    return redirect('blog:replycomments',obj_to_like.blog_post.id)
    
    
@login_required
def likescomments(request,id):
    
    likecomment=LikeComment.objects.all()
    obj_to_like=get_object_or_404(Comment,id=id)
    User=request.user

    
    if likecomment.count==0 :
        form=LikeComment.objects.create(blog_post=obj_to_like,user=User,like=1)
        
        return redirect('blog:comments',obj_to_like.blog_post.id)
        


    elif obj_to_like.likecomment_set.filter(user=User).exists():
        obj_to_like.likecomment_set.filter(user=User).delete()
    else:
        form=LikeComment.objects.create(blog_post=obj_to_like,user=User,like=1)
    
    return redirect('blog:comments',obj_to_like.blog_post.id)
    
    