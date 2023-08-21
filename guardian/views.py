from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from adminhod.models import CustomUser, PasswordStore
from library.models import Assignment
from schoolinfo.models import SchoolInformation
from student.models import AttendanceReport, Student
from utils import generate_ref_code, send_email_func

from guardian.forms import GeneralGuardianNotificationForm, GuardianRegForm, GuardianUpdateForm, SpecificGuardianNotificationForm
from guardian.models import Guardian, NotificationGuardian

# Create your views here.


class GuardianReg(View):
    
    def get(self,request,pk=None):
        guardians = Guardian.objects.all()
       
        if request.user.user_type=='1':
            if pk == None:
                form = GuardianRegForm()
            else:
                custom_user = CustomUser.objects.get(pk=pk)
                admin_instance = Guardian.objects.get(admin=custom_user)

                first_name = admin_instance.admin.first_name
                last_name = admin_instance.admin.last_name
                phone = admin_instance.admin.phone
            
                gender = admin_instance.admin.gender
                email = admin_instance.admin.email
                address = admin_instance.admin.address

                user_department = admin_instance.user_department
                post = admin_instance.post

                initial_data_for_update = {'first_name': first_name, 'last_name': last_name,
                                        'phone': phone, 'gender': gender, 'email': email, 'address': address,  'user_department': user_department, 'post': post, }

                form = GuardianUpdateForm(initial=initial_data_for_update)


                context = {
                    'form': form,
                    'guardians': guardians,
                    'title': f'Update Guardian {admin_instance.admin.username} ',
                    's_title': f'Update Guardian {admin_instance.admin.username} '
                }
                return render(request, 'admin/adminRegistration.html', context)
            context = {
                'form': form,
                'guardians': guardians,
                }
            return render(request,"guardian/guardianForm.html",context)
                    
        return HttpResponse("You don't have access into this department ")
    
    def post(self, request, pk=None):
        if request.user.user_type == '1':
            uuid_random=generate_ref_code()
            if pk == None:
                first_name=request.POST['first_name']
                last_name=request.POST['last_name']
                
            
                passwd=f'{uuid_random}{first_name[1]}{last_name[1]}'
                print('passwd:',passwd)
                form = GuardianRegForm(request.POST, request.FILES,initial={'password1':passwd,'password2':passwd})
            else:
                current_admin = CustomUser.objects.get(id=pk)
                form = GuardianUpdateForm(request.POST, request.FILES,
                                    instance=current_admin)

            if form.is_valid():
                
                title = form.cleaned_data['title']
                children = form.cleaned_data['children']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                password =form.cleaned_data['password1']
                repeatpassword =form.cleaned_data['password2']
                # uid =form.cleaned_data['uid']
                
                print(password,repeatpassword,title)

                instance = form.save()
                instance.set_password(password)
                
                instance.is_admin=True
                instance.is_staff=True
                instance.uid=uuid_random

                instance.username = f"{first_name} {last_name}"
                instance.save()
                Guardian_instance = Guardian.objects.create(admin=instance)
                
                Guardian_instance.title = title
                print(children)
                for child in children:
                    Guardian_instance.children.add(child)
                    # try:
                    std=Student.objects.get(id=child.id)
                    print(std)
                    # std.guardian=Guardian_instance
                    # std.save()
                    Guardian_instance.save()

                    # except Exception as e:
                    #     print(e)

                Guardian_instance.save()
                PasswordStore.objects.create(user=instance,password=password)
                try:
                    send_email_func(recipient_list=[instance.email,],from_email="smsprogram@gmail.com",body=f"Hay {Guardian_instance.title}  {instance.username} here is your password:'{password}'. Use it to login into our School account with the combination of your Email:'{instance.email}'",subject="Login Information in our School website Account Password",)
                except:
                    pass
                return redirect('guardian:register-guardian')
            else:
                guardians = Guardian.objects.all()
                context = {
                    'form': form,
                    'guardians': guardians,
                }
                return render(request, 'guardian/guardianForm.html', context)
        
         
        return HttpResponse("You don't have access into this department ")
    
    


def GuardianDelete(request,pk):
    guardian=Guardian.objects.get(pk=pk)
    
    guardian.delete()
    
    return redirect("guardian:register-guardian")




def profile(request):
    user=request.user
    if user.user_type=='4':
        guardian=Guardian.objects.get(admin=user)
        notify = NotificationGuardian.objects.filter(guardian_id=guardian)
        schoolinfo=SchoolInformation.objects.all()
        print(guardian)
        context={
            'guardian':guardian,
            'notify':notify,
            'schoolinfo':schoolinfo,
        }
        return render(request,"teacher/teacherProfile.html",context)
    return HttpResponse("YOU ARE NOT ALLOWED TO ACCESSED THIS PROFILE")


class SendGeneralNotification(View):

    def get(self, request):
        notifications = NotificationGuardian.objects.all().order_by("-created_at")
        form = GeneralGuardianNotificationForm()

        context = {
            'form': form,
            'notifications': notifications,
        }

        return render(request, "guardian/guardianNotificationForm.html", context)



    def post(self, request):

        form = GeneralGuardianNotificationForm(request.POST)
        guardians = Guardian.objects.all()

        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            message = form.cleaned_data['message']
            for guardian in guardians:
                NotificationGuardian.objects.create(
                    guardian_id=guardian, message=message, sender_name=sender_name)

        return redirect("guardian:notify-guardians")


class SendSpecialNotification(View):

    def get(self, request):
        notifications = NotificationGuardian.objects.all().order_by("-created_at")
        form = SpecificGuardianNotificationForm()

        context = {
            'form': form,
            'notifications': notifications,
        }

        return render(request, "guardian/guardianNotificationForm.html", context)

    def post(self, request):

        form = SpecificGuardianNotificationForm(request.POST)
      
        if form.is_valid():
            message = form.cleaned_data['message']
            sender_name = form.cleaned_data['sender_name']
            guardian = form.cleaned_data['guardian_id']
            NotificationGuardian.objects.create(guardian_id=guardian, message=message,sender_name=sender_name)
        else:
            print(form.errors)

        return redirect("guardian:notify-guardian")



def assignments(request):
    
    assignments_obj=Assignment.objects.all()
    context={
        'assignments':assignments_obj,
    }
    return render(request,'student/homeworkView.html',context)

# child_attendance.html
def guardian_view_child_attendance(request):
    
    user=Guardian.objects.get(admin=request.user)
    children=user.children.all()
    # print("children:",children)
    
    if children.count() >0:
    
        context= {
                "children":children,
                "attendance":AttendanceReport.objects.filter(student_id=children[0]),
                "guardian":True,
                "name":children[0],
            }
    return render(request,'guardian/child_attendance.html',context)


def get_attendance_byChild_name(request):
    child=request.POST['child']
    filter_by=request.POST['filter-by']
    student=Student.objects.get(id=child)
    
    if filter_by =='all':
        attendances=AttendanceReport.objects.filter(student_id=child)
    else:
        attendances=AttendanceReport.objects.filter(student_id=child,semester=filter_by)
    # print(attendances)
    if attendances.exists():
        context= {
                "attendance":attendances,
                "guardian":True,
                "name":student,
                }
        
        # print("exists")
                
        return render(request,"guardian/attendance_list.html",context)
    else:
        # print("do not exists")
        return HttpResponse(f"<h4 class='text-info bg-warning'>{student} doesn't yet have marks for this Semester/Trimester</h4>")

