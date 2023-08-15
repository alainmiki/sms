
from django.http import HttpResponse
from adminhod.forms import AdminHODForm, AdminHODUpdateForm, DocumentOfStaffForm, EventForm, GalleryForm, LibraryForm, Pass_QuestionForm
from adminhod.models import AdminHOD, CustomUser, Event, Gallery, PasswordStore

from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login, authenticate,logout
from student.models import ClassRoom, Subject
from guardian.models import Guardian
from library.models import DocumentOfStaff, Library, Pass_Question
from marks.models import Mark
from schoolinfo.models import SchoolInformation
from student.models import LeaveReportStudent, Student

from teacher.models import LeaveReportStaff, Staff
from django.contrib.auth.decorators import login_required

from utils import generate_ref_code, send_email_func

# Create your views here.

def showLogin(request):
    
    context={
        'schoolinfo':SchoolInformation.objects.all().values('address','email','whatsApp')
    }

    return render(request, "admin/login1.html",context)


class Login(View):

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # bb = CustomUser.objects.get(email=username)

        if '@' in request.POST.get('email'):

            # print("email backend",username,password)
            user = authenticate(
                username=username, password=password)
            # print(user)

            if user != None:
                print(user.user_type)

                login(request, user=user)
            else:
                messages.warning(request, 'Email or password is invalid')
                return render(request, 'admin/login1.html')

        else:
            print("username backend", username, password)
            user = authenticate(username=username, password=password)

            if user != None:
                login(request, user)
            else:
                messages.warning(
                    request, f'username or password is invalid {user} ')
                return render(request, 'admin/login1.html')
        # messages.info(
        #     request, f"successfully login {user} {user.user_type} {request.user}")
        
        if remember_me=='on':
            request.session['sms_username']=username
            request.session['sms_password']=password
        else:
            if request.session.has_key('sms_username') and request.session.has_key('sms_password'):
                del request.session['sms_username']
                del request.session['sms_password']
        # print(username,password,remember_me)
        # return HttpResponse(f"{username,password,remember_me}")

        if user.user_type == '2':
            return redirect("teacher:profile")

        if user.user_type == '3':
            return redirect("student:profile")

        if user.user_type == '1':
            return redirect("adminhod:dashboard")
        if user.user_type == '4':
            return redirect("guardian:profile")

        return redirect("/")

    def get(self, request):
        if request.session.has_key('sms_username') and request.session.has_key('sms_password'):
            username=request.session['sms_username']
            password=request.session['sms_password']
        else:
            username=''
            password=''
        print(username,password)
        context={
            "username":username,
            'password':password,
            'schoolinfo':SchoolInformation.objects.all().values('address','email','whatsApp','po_box','region')
        }

        return render(request, "admin/login1.html",context)


@login_required
def logoutView(request):
    logout(request)
    
    return redirect('adminhod:login')

class Signup(View):

    def post(self, request):

        print(request.POST)

        return redirect("login")

    def get(self, request):

        return render(request, "admin/signup.html")


class admindashbord(View):

    def post(self, request):
        pass

    def get(self, request):
        staff_count=Staff.objects.count()
        student_count=Student.objects.count()
        guardian_count=Guardian.objects.count()
        event_count=Event.objects.count()
        fees_count=Guardian.objects.count()
        marks_count=Mark.objects.count()
        gallery_count=Gallery.objects.count()
        student_leaves_count=LeaveReportStudent.objects.count()
        staff_leaves_count=LeaveReportStaff.objects.count()
        subject_count=Subject.objects.count()
        adminhod_count=AdminHOD.objects.count()
        
        library_count=3

        context={
            'staff_count':staff_count,
            'student_count':student_count,
            'guardian_count':guardian_count,
            'event_count':event_count,
            'fee_count':fees_count,
            'library_count':library_count,
            'marks_count': marks_count,
            'gallery_count': gallery_count,
            'student_leaves_count': student_leaves_count,
            'staff_leaves_count': staff_leaves_count,
            'subject_count': subject_count,
            'adminhod_count': adminhod_count,
        }

        return render(request, 'admin/base_template.html', context)


class EventView(View):

    def post(self, request, id=None):
        if request.user.user_type == '1':

            if id != None:
                instance = Event.objects.get(pk=id)
                form = EventForm(request.POST, instance=instance)
            else:
                form = EventForm(request.POST)

            if form.is_valid():
                print(form.cleaned_data['start_date_and_time'])
                form.save()
            else:
                messages.error(request, f' WARNING ERROR: {form.errors}')
                context = {"form": form, }

                return render(request, 'admin/eventRegistration.html', context)

            return redirect('adminhod:event-register')
        else:
            return HttpResponse('your are not allowed to venture into this section')

    def get(self, request, id=None):
        if request.user.user_type == '1':

            if id != None:
                instance = Event.objects.get(pk=id)
                # start_date_time = instance.start_date_and_time.strftime('mm/dd/yyyy hh:mm')
                # print(start_date_time)
                # datez, timez = str(instance.start_date_and_time).split(" ")
                # datez=str(datez)
                initial = {
                    'title': instance.title,
                    'location': instance.location,
                    'start_date_and_time': instance.start_date_and_time,
                    'end_date_and_time': instance.end_date_and_time,
                    'description': instance.description,
                    # 'location':instance.location,
                }
                form = EventForm(initial=initial)
            else:
                form = EventForm()

            events = Event.objects.all()
            context = {"form": form, 'events': events, 'time': timezone.now()}

            return render(request, 'admin/eventRegistration.html', context)
        else:
            return HttpResponse('your are not allowed to venture into this section')


@login_required
def event_management(request):
    if request.user.user_type == '1':

        events = Event.objects.all()

        upcoming_events = events.filter(
            start_date_and_time__gt=timezone.now(), end_date_and_time__gt=timezone.now())
        ongoing_events = events.filter(
            start_date_and_time__lte=timezone.now(), end_date_and_time__gte=timezone.now())
        pass_events = events.filter(
            start_date_and_time__lt=timezone.now(), end_date_and_time__lt=timezone.now())

        context = {"upcoming_events": upcoming_events,
                   'ongoing_events': ongoing_events, 'pass_events': pass_events, }

        return render(request, 'admin/events_management.html', context)
    else:
        return HttpResponse('your are not allowed to venture into this section')


class GalleryView(View):
    def post(self, request):
        if request.user.user_type == '1':
            form = GalleryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('adminhod:gallery')

        else:

            return HttpResponse("You are not allowed to access this section")

    def get(self, request):
        if request.user.user_type == '1':
            form = GalleryForm()
            context = {
                'form': form, 'gallery': Gallery.objects.all()
            }

            return render(request, 'admin/gallery.html', context)

        else:

            return HttpResponse("You are not allowed to access this section")


class AddAministrators(View):
   
    def get(self, request, id=None):
        admins = AdminHOD.objects.all()
        if id == None:
            form = AdminHODForm()
        else:
            custom_user = CustomUser.objects.get(id=id)
            admin_instance = AdminHOD.objects.get(admin=custom_user)

            first_name = admin_instance.admin.first_name
            last_name = admin_instance.admin.last_name
            phone = admin_instance.admin.phone
            place_of_birth = admin_instance.admin.place_of_birth
            gender = admin_instance.admin.gender
            email = admin_instance.admin.email
            address = admin_instance.admin.address

            user_department = admin_instance.user_department
            post = admin_instance.post

            initial_data_for_update = {'first_name': first_name, 'last_name': last_name,  'place_of_birth': place_of_birth,
                                       'phone': phone, 'gender': gender, 'email': email, 'address': address,  'user_department': user_department, 'post': post, }

            form = AdminHODUpdateForm(initial=initial_data_for_update)


            context = {
                'form': form,
                'admins': admins,
                'title': f'Update Admin {admin_instance.admin.username} ',
                's_title': f'Update AdminHOD {admin_instance.admin.username} '
            }
            return render(request, 'admin/adminRegistration.html', context)
        context = {
            'form': form,
            'admins': admins,
        }
        return render(request, 'admin/adminRegistration.html', context)

    def post(self, request, id=None):
        uuid_random=generate_ref_code()
        if id == None:
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
           
            passwd=f'{uuid_random}{first_name[1]}{last_name[1]}'
            print('passwd:',passwd)
            form = AdminHODForm(request.POST, request.FILES,initial={'password1':passwd,'password2':passwd,})
        else:
            current_admin = CustomUser.objects.get(id=id)
            form = AdminHODUpdateForm(request.POST, request.FILES,
                                instance=current_admin)

        if form.is_valid():
            # form.save()
            user_department = form.cleaned_data['user_department']
            post = form.cleaned_data['post']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            if id ==None:
                password =form.cleaned_data['password1']
                repeatpassword =form.cleaned_data['password2']
                # uid =form.cleaned_data['uid']
            
                print(password,repeatpassword)

            instance = form.save()
            if id ==None:
                instance.set_password(password)
                instance.uid=uuid_random
            
            instance.is_admin=True
            instance.is_staff=True
            

            instance.username = f"{first_name} {last_name}"
            instance.save()
            adminhod_instance = AdminHOD.objects.get(admin=instance)
            
            adminhod_instance.post = post
            adminhod_instance.user_department = user_department

            adminhod_instance.save()
            if id ==None:
                PasswordStore.objects.create(user=instance,password=password)
                send_email_func(recipient_list=[instance.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear Mr/Mrs/Miss/Sir {instance.username} here is your password:'{password}'. Use it to login into your School account with the combination of your Email:'{instance.email}'",subject="Your School website Account Password",)
            return redirect('adminhod:register-admin')
        else:
            admins = AdminHOD.objects.all()
            context = {
                'form': form,
                'admins': admins,
            }
            return render(request, 'admin/adminRegistration.html', context)


@login_required
def deleteAdminstrator(request,id):
    CustomUser.objects.get(id=id).delete()
    admins=AdminHOD.objects.all()
    context={
        'admins':admins
    }
    return render(request,'admin/adminTable.html',context)


@login_required
def show_or_hide_form(request):
    if request.method=="POST":
        if request.POST.get('showForm')=='on':
            
            context={
                'form':AdminHODForm()
            }
            return render(request,'admin/adminRegPatialForm.html',context)
        return HttpResponse("")

@login_required
def show_or_hide_library_form(request):
    if request.method=="POST":
        if request.POST.get('showForm')=='on':
            
            context={
                'form':LibraryForm()
            }
            return render(request,'admin/bookFormPatial.html',context)
        return HttpResponse("")

@login_required
def show_or_hide_question_form(request):
    if request.method=="POST":
        if request.POST.get('showForm')=='on':
            
            context={
                'form':Pass_QuestionForm()
            }
            return render(request,'admin/questionFormPatial.html',context)
        return HttpResponse("")



class CreateBook(View):
    
    def get(self,request,id=None):
        if request.user.user_type=='1':
            
            if id !=None:
                instance=Library.objects.get(id=id)
                initial={
                    'title':instance.title,
                    'author':instance.author,
                    'poster':instance.poster,
                    'subject':instance.subject,
                    'book':instance.book,
                    # 'content':instance.content,
                }
                form=LibraryForm(initial=initial)
            else:
                
                form=LibraryForm()
            
            context={
                'form':form,
                'books':Library.objects.all()
            }
            return render(request,'admin/libraryForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")
    
    def post(self,request,id=None):
        if request.user.user_type=='1':
           
            if id !=None:
                instance=Library.objects.get(id=id)
                
                form=LibraryForm(request.POST,request.FILES,instance=instance)
            else:
                
                form=LibraryForm(request.POST,request.FILES)
            
            if form.is_valid():
                instance=form.save()
                # instance.staff=staff
                # instance.save()
                return redirect('adminhod:library-create')
            
            context={
                'form':form,
                'books':Library.objects.all(),
            }
            print(form.errors)
            return render(request,'admin/libraryForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")


def delete_book(request,id):
    
    Library.objects.get(id=id).delete()
    
    return redirect('adminhod:library-create')
  
  
class CreateQuestion(View):
    
    def get(self,request,id=None):
        if request.user.user_type=='1':
            
            if id !=None:
                instance=Pass_Question.objects.get(id=id)
                initial={
                    'title':instance.title,
                    'paper':instance.paper,
                    'subject':instance.subject,
                }
                form=Pass_QuestionForm(initial=initial)
            else:
                
                form=Pass_QuestionForm()
            
            context={
                'form':form,
                'books':Pass_Question.objects.all()
            }
            return render(request,'admin/questionForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")
    
    def post(self,request,id=None):
        if request.user.user_type=='1':
           
            if id !=None:
                instance=Pass_Question.objects.get(id=id)
                
                form=Pass_QuestionForm(request.POST,request.FILES,instance=instance)
            else:
                
                form=Pass_QuestionForm(request.POST,request.FILES)
            
            if form.is_valid():
                instance=form.save()
                # instance.staff=staff
                # instance.save()
                return redirect('adminhod:pass_question-create')
            
            context={
                'form':form,
                'books':Pass_Question.objects.all(),
            }
            print(form.errors)
            return render(request,'admin/questionForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")


   
def delete_past_question(request,id):
    
    Pass_Question.objects.get(id=id).delete()
    
    return redirect('adminhod:pass_question-create')
    

@login_required
def show_or_hide_staffdocument_form(request):
    if request.method=="POST":
        if request.POST.get('showForm')=='on':
            
            context={
                'form':DocumentOfStaffForm()
            }
            return render(request,'admin/staffDocumentPatial.html',context)
        return HttpResponse("")



class CreateStaffDocument(View):
    
    def get(self,request,id=None):
        if request.user.user_type=='1':
            
            if id !=None:
                instance=DocumentOfStaff.objects.get(id=id)
                initial={
                    'title':instance.title,
                    'document':instance.document,
                    'subject':instance.subject,
                }
                form=DocumentOfStaffForm(initial=initial)
            else:
                
                form=DocumentOfStaffForm()
            
            context={
                'form':form,
                'books':DocumentOfStaff.objects.all()
            }
            return render(request,'admin/StaffDocumentForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")
    
    def post(self,request,id=None):
        if request.user.user_type=='1':
           
            if id !=None:
                instance=DocumentOfStaff.objects.get(id=id)
                
                form=DocumentOfStaffForm(request.POST,request.FILES,instance=instance)
            else:
                
                form=DocumentOfStaffForm(request.POST,request.FILES)
            
            if form.is_valid():
                instance=form.save()
                # instance.staff=staff
                # instance.save()
                return redirect('adminhod:staff-document-create')
            
            context={
                'form':form,
                'books':DocumentOfStaff.objects.all(),
            }
            print(form.errors)
            return render(request,'admin/StaffDocumentForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")


   
def delete_staff_document(request,id):
    
    DocumentOfStaff.objects.get(id=id).delete()
    
    return redirect('adminhod:staff-document-create')

class passwordStorView(View):
    def get(self,request):
        users=PasswordStore.objects.all()
        context={
            'users':users,
        }
        
        return render(request,'passwordResender/home.html',context)
    
    def post(self,request):
        name=request.POST['name']
        
        users=PasswordStore.objects.filter(user__username__icontains=name)
        
        context={
            'users':users,
        }
        
        return render(request,'passwordResender/table.html',context)


def resend_password(request,id):
    
    password_obj=PasswordStore.objects.get(id=id)
    # print(password_obj.user.email)
    try:
        send_email_func(recipient_list=[password_obj.user.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear  {password_obj.user.username} here is your resend password:'{password_obj.password}'. Use it to login into your School account with the combination of your Email:'{password_obj.user.email}'",subject="Your School website Account Password",)
    except:
        return HttpResponse("<span class='bg-info text-danger'>The password was not resend try again<span>")

    return HttpResponse("<span class='bg-info text-light'>The password was resend successfully<span>")

def getClassesForIdGeneration(request):
    cls=ClassRoom.objects.all()
    return render(request,'',{'classes':cls,})



def genStudentID(request,id):
    school_info=SchoolInformation.objects.all()[0]
    cls_room=ClassRoom.objects.get(id=id)
    students_info=Student.objects.filter(class_room=cls_room)
    
    context={
        
        'students':students_info,
        'school_info':school_info,
    }
    
    return render(request,'',context)

class studentIdgen(View):
    def get(self,request):
        # students=CustomUser.objects.all()
        students=Student.objects.all()
        school=SchoolInformation.objects.all()[0]
        
        # print(students)
        context={
            'students':students,
            'classes':ClassRoom.objects.all(),
            "logo":school.school_logo,'scname':school.school_name_full,
            'pobox':school.po_box,
            'email':school.email,
            'phone':school.phone,
            'website':school.website,
        }
        
        return render(request,'idtemplates/idcard.html',context)
    
    def post(self,request):
        cls_room=request.POST.get("stid")
        if cls_room =="all":
            students=Student.objects.all()
        else:
            # cls=ClassRoom.objects.get(id=int(cls_room))
            students=Student.objects.filter(class_room=cls_room)
        
        school=SchoolInformation.objects.all()[0]
        splited_date=str(timezone.now().date()).split('-')
        date_ext=int(str(splited_date[0]))+1
        
        splited_date[0]=str(date_ext)
        
        y,m,d=splited_date
        
        expire=f"{y}-{m}-{d}"
        
        
        context={
            'students':students,
            'expire':expire,
            'issue':str(timezone.now().date()),
            'classes':ClassRoom.objects.all(),
            "logo":school.school_logo,
            'scname':school.school_name_full,
            
            'pobox':school.po_box,
            'email':school.email,
            'phone':school.phone,
            'website':school.website,
        }
      
        
        
        return render(request,"idtemplates/patialID.html",context)
    
    

def adminIDView(request):
    
        staffs=AdminHOD.objects.all()
        
        school=SchoolInformation.objects.all()[0]
        splited_date=str(timezone.now().date()).split('-')
        date_ext=int(str(splited_date[0]))+1
        
        splited_date[0]=str(date_ext)
        
        y,m,d=splited_date
        
        expire=f"{y}-{m}-{d}"
        
      
      
        
        context={
            'staffs':staffs,
            'expire':expire,
            'issue':str(timezone.now().date()),
            'classes':ClassRoom.objects.all(),
            "logo":school.school_logo,
            'scname':school.school_name_full,
            'abbreviation':school.school_name_abbreviation,
            'pobox':school.po_box,
            'email':school.email,
            'phone':school.phone,
            'address':school.address,
            'website':school.website,
        }
        
        
        return render(request,"idtemplates/adminIDCard.html",context)
    


def staffIDView(request):
    
        staffs=Staff.objects.all()
        
        school=SchoolInformation.objects.all()[0]
        splited_date=str(timezone.now().date()).split('-')
        date_ext=int(str(splited_date[0]))+1
        
        splited_date[0]=str(date_ext)
        
        y,m,d=splited_date
        
        expire=f"{y}-{m}-{d}"
        
      
      
        
        context={
            'staffs':staffs,
            'expire':expire,
            'issue':str(timezone.now().date()),
            'classes':ClassRoom.objects.all(),
            "logo":school.school_logo,
            'scname':school.school_name_full,
            'abbreviation':school.school_name_abbreviation,
            'pobox':school.po_box,
            'email':school.email,
            'phone':school.phone,
            'address':school.address,
            'website':school.website,
        }
        
        
        return render(request,"idtemplates/staffPatialID.html",context)
    