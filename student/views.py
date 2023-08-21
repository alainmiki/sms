from django.http import HttpResponse

from django.utils import timezone
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from adminhod.models import CustomUser, PasswordStore
from student.models import AttendanceReport, StudentGovernment, Subject
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
from library.models import Assignment
from marks.models import Mark
from student.models import ClassRoom, Department, LeaveReportStudent, NotificationStudent, Student
from teacher.models import Staff
from utils import generate_ref_code, send_email_func
from .forms import AttendanceFilterForm, ClassForm, DepartmentForm, GenerallStudentNotificationForm, SpecificStudentNotificationForm, StudentAdmissionForm, StudentGovernmentForm, StudentLeaveFormForm, StudentMarksFilterForm, StudentRegistrationForm, StudentUpdateForm
# Create your views here.

class RegisterStudent(View):
    def post(self,request,c_id=None,id=None):
        if request.user.user_type=='1':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            # custom_password uuid+first_name[3]+last_name[2]
            uuid_random=generate_ref_code()
            passwd=f'{uuid_random}{first_name[1]}{last_name[1]}'
            
            if id == None:
                form=StudentRegistrationForm(request.POST,request.FILES,initial={'password1':passwd,'password2':passwd,})
            else:
                user=CustomUser.objects.get(id=c_id)
                form=StudentUpdateForm(request.POST,instance=user)
            
            
            if form.is_valid():
                dob=form.cleaned_data['date_of_birth']
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                class_room=form.cleaned_data['class_room']
                department = form.cleaned_data['department']
                # guardian=form.cleaned_data['guardian']
                print(form.cleaned_data['password1'],passwd)
                
                
                
                instance=form.save()
                instance.uid=uuid_random
                pwd=CustomUser.objects.get(id=instance.id)
                # pwd.set_password(passwd)
                instance.username=f"{first_name} {last_name}"
                # CustomUser.check_password()
                instance.save()
                # print(pwd.check_password(passwd))
                student = Student.objects.get(admin=pwd)
                student.date_of_birth=dob
                student.class_room = class_room
                student.department = department
                # student.guardian = guardian
                
                student.save()
                PasswordStore.objects.create(user=instance,password=passwd)
                NotificationStudent.objects.create(sender_name="school automated system",student_id=student,message=f" Hay  {instance.username}  You are welcome to your account")
                
                try:
                    send_email_func(recipient_list=[instance.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear  {instance.username} here is your password:'{passwd}'. Use it to login into your School account with the combination of your Email:'{instance.email}'",subject="Your School website Account Password",)
                except:
                    pass
                return redirect("student:register-student")
            else:
                print(form.errors)
               
                messages.info(request,form.errors)
                # form = StudentRegistrationForm()
                students = Student.objects.all()[:10]
                # print(students)
                context = {
                    'form': form,
                    'students':students
                }

                return render(request, 'student/registrationform.html', context)
            
        else:
            return HttpResponse("You are not allowed to access this section")
            


    def get(self, request, c_id=None, id=None):
        # messages.info(request, form.errors)
        students = Student.objects.all()[:10]
        if id == None:
            
            form = StudentRegistrationForm()
        else:
            custom_user = CustomUser.objects.get(id=c_id)
            student = Student.objects.get(admin=custom_user)

            first_name = custom_user.first_name
            last_name = custom_user.last_name
            phone = custom_user.phone
            place_of_birth = custom_user.place_of_birth
            gender = custom_user.gender
            email = custom_user.email
            address = custom_user.address
            
            date_of_birth = student.date_of_birth
            class_room = student.class_room
            department = student.department
            guardian = student.guardian

            initial_data_for_update = {'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'place_of_birth': place_of_birth,
                                       'phone': phone, 'gender': gender, 'email': email, 'address': address, 'class_room': class_room, 'department': department, 'guardian': guardian, }
            
            form = StudentUpdateForm(initial=initial_data_for_update)
        # print(students)
            context = {
                'form': form,
                'students': students,
                'title':f'Update Student {student} ',
                's_title': f'Update Student {student} '
            }
            return render(request,'student/registrationform.html',context)
        context = {
            'form': form,
            'students': students,
           
        }
        
        return render(request,'student/registrationform.html',context)


# def StudentProfile(request):
    
#     return HttpResponse(f"{request.user} is login right now")


def manageStudents(request):
    if request.user.user_type=="1":
        
        students=Student.objects.all()
        
        context={
            'students':students,
        }
        
        return render(request,'student/manage_student.html',context)

    return HttpResponse(f"{request.user} You are not allowed to access students information")

def deleteStudent(request,pk):
    if request.user.user_type=="1":
        
        student=CustomUser.objects.get(pk=pk)
        student.delete()
        
       
        return redirect("student:manage-student")

    return HttpResponse(f"{request.user} You are not allowed to delete")


class SendGeneralNotification(View):

    def get(self, request):
        notifications = NotificationStudent.objects.all().order_by("-created_at")
        form = GenerallStudentNotificationForm()

        context = {
            'form': form,
            'notifications': notifications,
        }

        return render(request, "student/studentNotificationForm.html", context)

    def post(self, request):

        form = GenerallStudentNotificationForm(request.POST)
        students = Student.objects.all()

        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            message = form.cleaned_data['message']
            for student in students:
                NotificationStudent.objects.create(
                    student_id=student, message=message, sender_name=sender_name)

        return redirect("student:notify-students")


class SendSpecialNotification(View):

    def get(self, request):
        notifications = NotificationStudent.objects.all().order_by("-created_at")
        form = SpecificStudentNotificationForm()

        context = {
            'form': form,
            'notifications': notifications,
        }

        return render(request, "student/studentNotificationForm.html", context)

    def post(self, request):

        form = SpecificStudentNotificationForm(request.POST)
      
        if form.is_valid():
            message = form.cleaned_data['message']
            sender_name = form.cleaned_data['sender_name']
            student = form.cleaned_data['student']
            NotificationStudent.objects.create(student_id=student, message=message,sender_name=sender_name)
        else:
            print(form.errors)

        return redirect("student:notify-student")


class StudentApplyLeave(View):
    def get(self, request):
        if request.user.user_type == '3':
            form = StudentLeaveFormForm()
            leaves = LeaveReportStudent.objects.filter(student_id=request.user.student)
            context = {
                'form': form,
                'leaves': leaves, 'time': timezone.now()
            }
            return render(request, 'student/leaveForm.html', context)
        return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")

    def post(self, request):
        if request.user.user_type == '3':
            form = StudentLeaveFormForm(request.POST)
            if form.is_valid():
               
                user = form.cleaned_data['student_id']
                form.save()

            leaves = LeaveReportStudent.objects.filter(
                student_id=user).order_by('-leave_status')
            context = {
                'form': form,
                'leaves': leaves, 'time': timezone.now
            }
            return render(request, 'student/leaveForm.html', context)
        else:
            # print(leave_date, leave_date, leave_message, type(request.user.user_type))
            return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")


class ManageApproveStudentsLeaves(View):
    def get(self, request):
        form = StudentLeaveFormForm()
        aplied_leaves = LeaveReportStudent.objects.filter(
            leave_status=False, leave_end_date__gte=timezone.now())
        aproved_leaves = LeaveReportStudent.objects.filter(leave_status=True)
        Expired_leaves = LeaveReportStudent.objects.filter(
            leave_end_date__lt=timezone.now())
        context = {
            'form': form,
            'aplied_leaves': aplied_leaves,
            'aproved_leaves': aproved_leaves,
            'Expired_leaves': Expired_leaves,
        }
        if request.user.user_type == '1':
            return render(request, 'student/manageStudentLeaves.html', context)
        else:
            return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")

    def post(self, request):
        context = {}
        if request.user.user_type == '1':
            return render(request, 'student/manageStudentLeaves.html', context)
        else:
            return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")


def change_leave_status(request, id):
    leave = LeaveReportStudent.objects.get(id=id)
    leave.leave_status = True
    leave.save()
    NotificationStudent.objects.create(sender_name="school automated system",student_id=leave.student_id,message=f" Hay  {leave.student_id.admin.username}  Your leave was approved")
                
    try:
        send_email_func(recipient_list=[leave.student_id.admin.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear  {leave.student_id.admin.username} Your leave request was approved",subject="Your SchoolLeave request",)
    except:
        pass

    return redirect("student:manage-student-leaves")


def change_leave_status_unapproved(request, id):
    leave = LeaveReportStudent.objects.get(id=id)
    leave.leave_status = False
    leave.save()
    
    NotificationStudent.objects.create(sender_name="school automated system",student_id=leave.student_id,message=f" Hay  {leave.student_id.admin.username}  Your leave was nOT approved")
                
    try:
        send_email_func(recipient_list=[leave.student_id.admin.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear  {leave.student_id.admin.username} Your leave request was NOT approved",subject="Your SchoolLeave request",)
    except:
        pass

    return redirect("student:manage-student-leaves")



class ClassRoomAdd(View):
    def get(self,request):
        if request.user.user_type=='1':
            form=ClassForm()
            items=ClassRoom.objects.all()
            
            context={
                'form':form,
                'title':'Add & View Class Rooms',
                'display':'Classes Details',
                'items':items,
                'type':"class",
            }
            
            return render(request,'student/addClassAndDepartment.html',context)
        return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")
    
    def post(self,request):
        if request.user.user_type == '1':
            form = ClassForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("student:add-class")
        pass


class DepartmentRoomAdd(View):
    
    def get(self,request):
        if request.user.user_type=='1':
            form=DepartmentForm()
            items=Department.objects.all()
            
            context={
                'form':form,
                'title':'Add & View Class Department',
                'display': 'Classes Department Details',
                'items':items,
                 'type':"department",
            }
            
            return render(request,'student/addClassAndDepartment.html',context)
        
        return HttpResponse("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")
    
    
    def post(self,request):
        if request.user.user_type == '1':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("student:add-department")
       


def deleteClassOrDepartment(request, type_arg, id):
    if type_arg=="class":
        cls=ClassRoom.objects.get(id=id)
        
        cls.delete()
        return redirect("student:add-class")
    elif type_arg=="department":
        cls=Department.objects.get(id=id)
        
        cls.delete()
        return redirect("student:add-department")

        

def StudentProfile(request):
    user = request.user
    if user.user_type == '3':
        student = Student.objects.get(admin=user)
        notify = NotificationStudent.objects.filter(student_id=student)
        print(student)
        context = {
            'student': student,
            'notify': notify,
        }
        return render(request, "teacher/teacherProfile.html", context)
    return HttpResponse("YOU ARE NOT ALLOWED TO ACCESSED THIS PROFILE")

# student attendance report section

@sync_to_async
@login_required
def student_attendance_report(request):
    
    attendance=AttendanceReport.objects.filter(student_id__admin=request.user)
    form=AttendanceFilterForm()
    context={
        'attendance':attendance,
        'form':form,
    }
    return render(request,'student/attendance.html',context)


@sync_to_async
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


# student marks records section


def student_marks_record(request):
    student_marks=Mark.objects.filter(student_id__admin=request.user)
    context={
        'marks':student_marks,
        'form':StudentMarksFilterForm()
    }
    
    return render(request,'student/studentMarks.html',context)


def student_mark_filter(request):
    
    form = StudentMarksFilterForm(request.POST)
   
    # get_by=request.POST['getby']
    filter_by = request.POST['filter_by']
    sort_by = request.POST['sort_by']
    get_by = request.POST['get_by']
    # class_room = request.POST['class_room']
    data=None
    if filter_by =='subject':
        data=Mark.objects.filter(student_id__admin=request.user,subject_id__name=get_by)

    elif filter_by =='staff':
        # print(get_by)
        data=Mark.objects.filter(student_id__admin=request.user,staff_id__admin__username=get_by)
        
    elif filter_by =='semester':
        data=Mark.objects.filter(student_id__admin=request.user,semester=get_by)
        
    if get_by =='all':
        data=Mark.objects.filter(student_id__admin=request.user,)
        # print(filter_by,get_by)

    
    if sort_by !='all' and data!=None:
        data=data.all().order_by('-'+str(sort_by))
    else:
        data == Mark.objects.filter(student_id__admin=request.user,)
        
        
        
    # print(filter_by,get_by)
    if request.user.user_type=='2':
        marks=data.filter(staff_id__admin=request.user)
    else:
        marks = data
    if marks==[]:
        # messages.error(request,"There is no data in the filtered category")
        return HttpResponse("There is no data in the filtered category")
    
    context = {
        'marks': marks,
        
        'form': form,

    }
    # print(marks, form)
    return render(request,'student/studentMarksTable.html',context)

    
    # return HttpResponse(f'Warning error: {form.errors}')

def Student_filterBy(request):
    
    ftby=request.POST.get('filter_by')
    if ftby =='subject':
        data=Subject.objects.all()
        list_it=False
        by_student=False
    elif ftby =='student':
        data=Student.objects.all()
        by_student=True
        list_it=False
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
        
    
    # data=''
    
    context={
        'object': data, 'list_it': list_it, 'by_student': by_student
    }
    
    return render(request,'student/markspatialInput.html',context)

def homework(request):
    user=Student.objects.get(admin=request.user)
    cls=user.class_room
    assignments=Assignment.objects.filter(class_room__name__icontains=cls,submission_date__gte=timezone.now())
    context={
        'assignments':assignments,
    }
    return render(request,'student/homeworkView.html',context)

class create_Student_government(View):
    
    def get(self,request,id=None):
      
        if request.user.user_type=='1':
            if id == None:
                
                form=StudentGovernmentForm()
            else:
                candidate=StudentGovernment.objects.get(id=id)
                initial={
                    'student_id':candidate.student_id,
                    'position':candidate.position,
                }
                form=StudentGovernmentForm(initial=initial)
                
            candidates=StudentGovernment.objects.all()
            context={
                'form':form,
                'candidates':candidates,
            }
            return render(request,'student/student_government.html',context)
        else:
            return HttpResponse("not allowed access")
            
    def post(self,request,id=None):
        if request.user.user_type=='1':
            if id == None:
                
                form=StudentGovernmentForm(request.POST)
            else:
                candidate=StudentGovernment.objects.get(id=id)
                
                form=StudentGovernmentForm(request.POST,instance=candidate)
            if form.is_valid():
                form.save()
                
                return redirect("student:student-government")
            
            candidates=StudentGovernment.objects.all()
            context={
                'form':form,
                'candidates':candidates,
            }
            return render(request,'student/student_government.html',context)
        else:
            return HttpResponse("not allowed access")
            
def delete_Student_government(request,id):
    StudentGovernment.objects.get(id=id).delete()
    return redirect("student:student-government")

class AdmissionView(View):
    def post(self,request):
        form=StudentAdmissionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,'Your Admission Details Was Send Successfully :)')
            return redirect('student:admission')
        else:
            messages.warning(request,'Your Admission Details Was not  Send Successfully make sure you fill every entry carefully (:(❁´◡`❁)')
            print(form.errors)
            context={
                'form':form,
            }
            
            return render(request,'schoolinfo/admissionForm.html',context)

    def get(self,request):
        form=StudentAdmissionForm()
        context={
            'form':form,
        }
        
        return render(request,'schoolinfo/admissionForm.html',context)
