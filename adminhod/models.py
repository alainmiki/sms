
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save



user_types_data = (('1', "HOD"), ('2', "Staff"),
                   ('3', 'Student'), ('4', 'Guardian'))
user_department_data = (('1', "admin"), ('2', "secretary"),
                   ('3', 'bossier'), ('4', 'chief of staff'))

genders=(('M',"Male"),("F","Female"),("O","Others"))

class CustomUserManager(BaseUserManager):
    def create_user(self, email,username,password=None):
        if not email:
            raise ValueError('User most have an email address.')
        if not username:
            raise ValueError("user most have a username.") 
        user=self.model(email=self.normalize_email(email),username=username,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), username=username,password=password)
        user.is_admin=True
        user.is_staff=True
        # user.is_active=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    uid=models.CharField(max_length=50, blank=True,null=True)
    email=models.EmailField(max_length=254,verbose_name='email',unique=True)
    first_name=models.CharField(max_length=50, blank=True,null=True)
    last_name=models.CharField(max_length=50, blank=True,null=True)
    username=models.CharField(max_length=50, unique=True,)
    gender=models.CharField(choices=genders, max_length=10, blank=True,null=True)

    place_of_birth = models.CharField(max_length=200, blank=True, null=True)
    
    address = models.CharField(max_length=100, blank=True, null=True)
    phone=models.CharField(max_length=50, blank=True,null=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    profile_picture=models.ImageField(upload_to="profile_pictures",  max_length=100,default="static/images/default.jpg", blank=True, null=True)
    
  
    user_type = models.CharField( choices=user_types_data, max_length=15, blank=True,null=True)
    
    objects= CustomUserManager()
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=["username","user_type","password"]
    
    def __str__(self) -> str:
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True


class AdminHOD(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    post=models.CharField(max_length=50,blank=True,null=True)
    
    user_department=models.CharField(
        default=1, choices=user_department_data, max_length=15, blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return str(self.admin.username)



class Event(models.Model):
    """Model definition for Event."""
    title=models.CharField(max_length=250)
    location=models.CharField(max_length=250)
    start_date_and_time=models.DateTimeField()
    end_date_and_time=models.DateTimeField()
    description=models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Event."""
        ordering=['-created_date','-updated_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        """Unicode representation of Event."""
        return self.title


class Gallery(models.Model):
    categories=[('student','student'),('staff','staff'),('adminhod','adminhod'),('guardian',"guardian")]
    category=models.CharField(choices=categories, max_length=50)
    image=models.ImageField(upload_to='gallery')
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    """Model definition for Gallery."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Gallery."""

        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'

    def __str__(self):
        """Unicode representation of Gallery."""
        return self.image.name


class PasswordStore(models.Model):
    """Model definition for PasswordStore."""

    # TODO: Define fields here
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    password=models.CharField(max_length=10)

    class Meta:
        """Meta definition for PasswordStore."""

        verbose_name = 'PasswordStore'
        verbose_name_plural = 'PasswordStores'

    def __str__(self):
        """Unicode representation of PasswordStore."""
        return self.user.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == '1':
            AdminHOD.objects.create(admin=instance)
      
