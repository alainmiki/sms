

from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from adminhod.models import CustomUser, PasswordStore
from library.models import Assignment
from schoolinfo.models import SchoolInformation

from teacher.forms import AssignmentForm, GenerallStaffNotificationForm, SpecificStaffNotificationForm, StaffLeaveFormForm, StaffUpdateForm, StaffRegistrationForm
from teacher.models import AttendanceReport, LeaveReportStaff, NotificationStaff, Staff
from utils import generate_ref_code, send_email_func


# Create your views here.

class registration(View):
    
    def post(self,request):
        # print( request.POST,request.FILES)
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        # custom_password uuid+first_name[3]+last_name[2]
        uuid_random=generate_ref_code()
        passwd=f'{uuid_random}{first_name[1]}{last_name[1]}'
        form = StaffRegistrationForm(request.POST, request.FILES,initial={'password1':passwd,'password2':passwd,})
        
        if form.is_valid():
            # print(form.cleaned_data['first_name'])
            first_name =form.cleaned_data['first_name']
            last_name =form.cleaned_data['last_name']
           
            subjects =form.cleaned_data['subjects']
            duty_post =form.cleaned_data['duty_post']
            matricule =form.cleaned_data['matricule']
            password =form.cleaned_data['password1']
            repeatpassword =form.cleaned_data['password2']
            profile_picture = form.cleaned_data['profile_picture']
           
            username=f"{first_name} {last_name}"
            print(subjects)
            # print(password, repeatpassword)
            if password == repeatpassword:
                
                instance=form.save()
                
                instance.username=username
                instance.uid=uuid_random
                instance.save()
                staff = Staff.objects.get(admin=instance)
               
                staff.duty_post = duty_post
                staff.matricule = matricule
                staff.subjects.set(subjects)
                staff.save()
                PasswordStore.objects.create(user=instance,password=passwd)
                NotificationStaff.objects.create(sender_name="school automated system",staff_id=staff,message=f" Hay  {instance.username}  You are welcome to your account")
                
                try:
                    send_email_func(recipient_list=[instance.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear Mr/Mrs/Miss/Sir {instance.username} here is your password:'{passwd}'. Use it to login into your School account with the combination of your Email:'{instance.email}'",subject="Your School website Account Password",)
                except:
                    pass
        
                
                messages.success(request, "success")
            else:
                messages.error(request, "error")
        else:
            # print("error", form.errors)
            pass
        
        
       
        staffs=Staff.objects.all()
        context={
                'staffs':staffs,
                'form':form
            }
       
       
        return  render(request, 'teacher/registrationform.html',context)
    
    def get(self,request):
        form = StaffRegistrationForm()
        staffs = Staff.objects.all()
        context={
                'staffs':staffs,
                'form':form,
            }

        return render(request, 'teacher/registrationform.html', context)

class manage_staffs(View):
    
    def get(self,request):
        
        staffs=Staff.objects.all().order_by("-created_at")
        
        context={
            'staffs':staffs
        }
        
        return render(request, 'teacher/manage_staffs.html', context)

class update_staff(View):
    
    def get(self,request,c_id,id):
        custom_user=CustomUser.objects.get(id=c_id)
        staff=Staff.objects.get(admin=custom_user)
      
        first_name =custom_user.first_name
        last_name =custom_user.last_name
        phone =custom_user.phone
        username =custom_user.username
        place_of_birth =custom_user.place_of_birth
        gender =custom_user.gender
        email =custom_user.email
        address =custom_user.address
        subjects =staff.subjects.all()
        duty_post = staff.duty_post
        matricule = staff.matricule
       
        
        initial_data_for_update = {'first_name': first_name, 'last_name': last_name,'username':username,'place_of_birth':place_of_birth, 'phone': phone, 'gender': gender, 'email': email,
                                   'address': address, 'subjects': subjects, 'duty_post': duty_post, 'matricule': matricule,}
    
        form = StaffUpdateForm(initial=initial_data_for_update)
        staffs=Staff.objects.all().order_by('-created_at')
      

        context = {
             "title":f"Update staff {custom_user.username}",
            'staffs': staffs,
            'form': form
        }
        
        return render(request, 'teacher/update_staff.html', context)
    
    def post(self, request, c_id, id):
        
        user=get_object_or_404(CustomUser,id=c_id)
        staff=Staff.objects.get(id=id)
        
        form=StaffUpdateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            subjects =form.cleaned_data['subjects']
            duty_post =form.cleaned_data['duty_post']
            matricule =form.cleaned_data['matricule']
            
            staff.duty_post=duty_post
            staff.matricule=matricule
            staff.subjects.set(subjects)
            
            staff.save()

        return redirect("teacher:manage-staffs")


class SendGeneralNotification(View):
    
    def get(self,request):
        notifications=NotificationStaff.objects.all()
        form=GenerallStaffNotificationForm()
        
        context={
            'form':form,
            'notifications':notifications,
        }
        
        return render(request,"teacher/generalNotification.html",context)
        
    def post(self,request):
        
        form=GenerallStaffNotificationForm(request.POST)
        staffs=Staff.objects.all()
        
        if form.is_valid():
            message=form.cleaned_data['message']
            sender_name = form.cleaned_data['sender_name']
            for staff in staffs:
                NotificationStaff.objects.create(staff_id=staff,message=message,sender_name=sender_name)
                
            
        return redirect("teacher:notify-staffs")


class SendSpecialNotification(View):
    
    def get(self,request):
        notifications=NotificationStaff.objects.all()
        form=SpecificStaffNotificationForm()
        
        context={
            'form':form,
            'notifications':notifications,
        }
        
        return render(request,"teacher/generalNotification.html",context)
        
    def post(self,request):
        
        form = SpecificStaffNotificationForm(request.POST)
        # staffs=Staff.objects.all()
        
        if form.is_valid():
            message=form.cleaned_data['message']
            sender_name = form.cleaned_data['sender_name']
            staff=form.cleaned_data['staff']
            NotificationStaff.objects.create(staff_id=staff,message=message,sender_name=sender_name)
        else:
            
            print(form.errors)
           
                
            
        return redirect("teacher:notify-staff")



class StaffApplyLeave(View):
    def get(self,request):
        if request.user.user_type == '2':
            form=StaffLeaveFormForm()
            # staff=Staff.objects.get(admin=request.user)
            leaves = LeaveReportStaff.objects.filter(
                staff_id__admin=request.user)
            context={
                'form':form,
                'leaves': leaves, 'time': timezone.now()
                }
            return render(request,'teacher/leaveForm.html',context)
        return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")
    def post(self,request):
        if request.user.user_type == '2':
            staff_id=Staff.objects.get(admin=request.user)
            form = StaffLeaveFormForm(request.POST,initial={'staff_id':staff_id})
            if form.is_valid():
                leave_start_date=form.cleaned_data['leave_start_date']
                leave_end_date=form.cleaned_data['leave_end_date']
                leave_message = form.cleaned_data['leave_message']
                
                LeaveReportStaff.objects.create(staff_id=staff_id,leave_start_date=leave_start_date,leave_end_date=leave_end_date,leave_message=leave_message)
                return redirect('teacher:staff-apply-leave')
                
            messages.warning(request,f"You didn't fill form well!. The following is the errors: {form.errors}")
            leaves=LeaveReportStaff.objects.filter(staff_id=staff_id).order_by('-leave_status')
            context={
                'form':form,
                'leaves': leaves,'time':timezone.now
                }
            return render(request, 'teacher/leaveForm.html', context)
        else:
            # print(leave_date, leave_date, leave_message, type(request.user.user_type))
            return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")


class ManageAproveStaffsLeaves(View):
    def get(self, request):
        form = StaffLeaveFormForm()
        aplied_leaves = LeaveReportStaff.objects.filter(
            leave_status=False, leave_end_date__gte=timezone.now())
        aproved_leaves=LeaveReportStaff.objects.filter(leave_status=True)
        Expired_leaves = LeaveReportStaff.objects.filter(leave_end_date__lt=timezone.now())
        context = {
            'form': form,
            'aplied_leaves':aplied_leaves,
            'aproved_leaves': aproved_leaves,
            'Expired_leaves':Expired_leaves,
        }
        if request.user.user_type=='1':
            return render(request, 'teacher/manageStaffLeaves.html', context)
        else:
            return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")

    def post(self, request):
        context = {}
        if request.user.user_type == '1':
            return render(request, 'teacher/manageStaffLeaves.html', context)
        else:
            return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")


class CreateAssignment(View):
    
    def get(self,request,id=None):
        if request.user.user_type=='2':
            staff=Staff.objects.get(admin=request.user)
            if id !=None:
                instance=Assignment.objects.get(id=id)
                initial={
                    'class_room':instance.class_room.all(),
                    'subject':instance.subject,
                    'submission_date':instance.submission_date,
                    'content':instance.content,
                }
                form=AssignmentForm(initial=initial)
            else:
                
                form=AssignmentForm()
            
            context={
                'form':form,
                'assignments':Assignment.objects.filter(staff=staff)
            }
            return render(request,'teacher/assignmentForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")
    
    def post(self,request,id=None):
        if request.user.user_type=='2':
            staff=Staff.objects.get(admin=request.user)
            if id !=None:
                instance=Assignment.objects.get(id=id)
                
                form=AssignmentForm(request.POST,instance=instance)
            else:
                
                form=AssignmentForm(request.POST)
            
            if form.is_valid():
                instance=form.save()
                instance.staff=staff
                instance.save()
                return redirect('teacher:assignment-create')
            
            context={
                'form':form,
                'assignments':Assignment.objects.filter(staff=staff),
            }
            return render(request,'teacher/assignmentForm.html',context)
        else:
            return HttpResponse("You are not allowed to access this section")




def change_leave_status(request,id):
    leave=LeaveReportStaff.objects.get(id=id)
    leave.leave_status=True
    leave.save()
    
    NotificationStaff.objects.create(sender_name="school automated system",staff_id=leave.staff_id,message="Your permission was Approved")
    
    try:
        send_email_func(recipient_list=[leave.staff_id.admin.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear Mr/Mrs/Miss/Sir {leave.staff_id.admin.username} Your permission was approved",subject="Your School permission Approval",)
    except:
        pass
    
    return redirect("teacher:manage-staff-leaves")

def change_leave_status_unapprove(request,id):
    leave=LeaveReportStaff.objects.get(id=id)
    leave.leave_status=False
    leave.save()
    NotificationStaff.objects.create(sender_name="school automated system",staff_id=leave.staff_id,message="Your permission was not Approved")
    try:
        send_email_func(recipient_list=[leave.staff_id.admin.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear Mr/Mrs/Miss/Sir {leave.staff_id.admin.username} Your permission was NOT approved",subject="Your School permission Approval",)
    except:
        pass
    
    
    
    return redirect("teacher:manage-staff-leaves")

def profile(request):
    user=request.user
    if user.user_type=='2':
        staff=Staff.objects.get(admin=user)
        notify = NotificationStaff.objects.filter(staff_id=staff)
        schoolinfo=SchoolInformation.objects.all()
        print(staff)
        context={
            'staff':staff,
            'notify':notify,
            'schoolinfo':schoolinfo,
        }
        return render(request,"teacher/teacherProfile.html",context)
    return HttpResponse("YOU ARE NOT ALLOWED TO ACCESSED THIS PROFILE")


def create_daily_staff_attendance(request):
    if request.user.user_type=='1':
        if AttendanceReport.objects.filter(attendance_date=timezone.now()).exists():
            staff_attendance=AttendanceReport.objects.filter(attendance_date=timezone.now())
        else:
            staff_obj=CustomUser.objects.filter(user_type='2')
            for staff in staff_obj:
                AttendanceReport.objects.create(staff_id=staff)
            staff_attendance=AttendanceReport.objects.filter(attendance_date=timezone.now())
        context={
            "attendances":staff_attendance,
        }
        return render(request,"teacher/take_staff_attendance.html",context)
    return HttpResponse("YOU ARE NOT ALLOWED TO ACCESSED THIS PROFILE")
class StaffTakeAttendance(View):
    
    def get(self,request):
        print(request.user.user_type)
        if request.user.user_type=='2':
            form=AttendanceFilterForm()
            context={
                'form':form,
            }
            return render(request,'attendance/take_attendace.html',context)
        return HttpResponse("YOU ARE NOT ALLOWED ACCESS  INTO THIS SECTION")
    
    def post(self,request):
        
        if request.user.user_type == '2':
            form=AttendanceFilterForm(request.POST)
            
            if form.is_valid():
                class_id=form.cleaned_data['class_id']
                subject_id=form.cleaned_data['subject_id']
                semester=form.cleaned_data['semester']
                
                subject_id=Subject.objects.get(name=subject_id)
                
                # class_id = ClassRoom.objects.get(name=class_id)
                
                # getting students of this selected class
                students=Student.objects.filter(class_room__name=class_id)
                for student in students:
                    AttendanceReport.objects.get_or_create(
                        class_id=class_id, subject_id=subject_id, student_id=student,staff_id=request.user,semester=semester, attendance_date=timezone.now())
                
                   
                # print(attendance_instance)
                attendance = AttendanceReport.objects.filter(
                    class_id=class_id,staff_id=request.user, subject_id=subject_id,semester=semester, attendance_date=timezone.now())
            
                context={
                    'attendance':attendance,
                    'form':form
                }
                return render(request, 'attendance/attendanceList.html', context)
            else:
                return HttpResponse(f"<h3 class='text-center card badge-danger text-info'><span class='text-warning'>{str(request.user.username).upper()}</span> please mark sure the CLASS and SUBJECT FIELDS ard not empty </h3>")
            
            
        return HttpResponse("YOU ARE NOT ALLOWED ACCESS  INTO THIS SECTION")

@csrf_exempt
def StaffAttendance_statu_update(request,t_id,id):
    if request.user.user_type == '1':
        
        # student=Student.objects.get(id=s_id)
        attendance = AttendanceReport.objects.get(
            id=id, attendance_date=timezone.now())
        
        print(attendance.coming_status,attendance.going_status)
        if t_id==1:
            
            if attendance.coming_status == True:
                attendance.coming_status=0
                attendance.coming_time=None
                status_report = "absent"
                
            else:
                attendance.coming_status=1
                attendance.coming_time=timezone.now()
                status_report="present"
            
            attendance.save()
        
            # print(a_id,s_id)
            

            return HttpResponse(f"<span class='text-center'>{attendance.staff_id.username} has been marked {status_report} for coming </span>") 
        elif t_id==2:
            
            if attendance.going_status == True:
                attendance.going_status=0
                attendance.going_time=None
                status_report = "absent"
                
            else:
                attendance.going_status=1
                attendance.going_time=timezone.now()
                status_report="present"
            
            attendance.save()
        
            # print(a_id,s_id)
            

            return HttpResponse(f"<span class='text-center'>{attendance.staff_id.username} has been marked {status_report} for closing </span>") 
        
    return HttpResponse("YOU ARE NOT ALLOWED ACCESS  INTO THIS SECTION")

sync_to_async
def filter_attendance(request):
    
    form = AttendanceFilterForm(request.POST)
   
    filter_by = request.POST['filter_by']
    sort_by = request.POST['sort_by']
    get_by = request.POST['get_by']
   
    data=None
    student=request.user
    if filter_by =='subject':
        data=AttendanceReport.objects.filter(student_id__admin=student,subject_id__name=get_by)
        
    
    elif filter_by =='staff':
        data=AttendanceReport.objects.filter(student_id__admin=student,staff_id__username=get_by)
        
    elif filter_by =='semester':
        data=AttendanceReport.objects.filter(student_id__admin=student,semester=get_by)
        
    if get_by =='all':
        data=AttendanceReport.objects.filter(student_id__admin=student,class_id=student.class_room)
        # print(filter_by,get_by)
   
    
    if sort_by !='all' and data!=None:
        data=data.all().order_by('-'+str(sort_by))
    else:
        data == AttendanceReport.objects.all()
        
        
        
    # print(filter_by,get_by)
    if request.user.user_type=='2':
        attendance=data.filter(staff_id__admin=request.user)
    else:
        attendance = data
    if attendance==[]:
        return HttpResponse("There is no data in the filtered category")
    
    context = {
        'attendance': attendance,
        
        'form': form,

    }
    # print(marks, form)
    return render(request,'student/attendance_list.html',context)

@sync_to_async
def filterBy(request):
    
    ftby=request.POST.get('filter_by')
    
    if ftby =='subject':
        data=Subject.objects.all()
        list_it=False
        by_student=False
   
    elif ftby =='staff':
        data=Staff.objects.all()
        by_student=True
        list_it=False
        
    elif ftby =='semester':
        data=['ft','st','tt']
        list_it=True
        by_class = False
        by_student = False
    else:
        data = ['all']
        list_it = True
        by_class = False
        by_student = False
        
    context={
        'object': data, 'list_it': list_it, 'by_student': by_student
    }
    
    return render(request,'student/patialInput.html',context)
