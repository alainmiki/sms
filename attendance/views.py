from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from attendance.forms import AttendanceFilterForm, SubjectForm
from django.views.decorators.csrf import csrf_exempt
from student.models import AttendanceReport, Subject
from student.models import ClassRoom, Student

# Create your views here.

class AddSubject(View):
    def post(self,request,id=None):
        if request.user.user_type == '1':
            if id != None:
                subject = Subject.objects.get(id=id) 
                title = "Update or View Subjects"
                
                form = SubjectForm(request.POST,instance=subject)
            else:
                form = SubjectForm(request.POST)
                title = "Add or View Subjects"
            
            if form.is_valid():
                form.save()
                
                messages.success(request,"Submitted Successfully")
                return redirect('attendance:add-subject')
            
            else:
                messages.error(request,"Submitted Successfully")
                items = Subject.objects.all()
                context = {
                    'items': items,
                    'form': form,
                    'title': title,
                        }
                return render(request, "attendance/subjectTemplate.html", context)
        return HttpResponse("YOU ARE NOT ALLOWED ACCESS  INTO THIS SECTION")
    
    
    def get(self,request,id=None):
        if request.user.user_type == '1':
            if id !=None:
                subject=Subject.objects.get(id=id)
                
                initial_data = {"name": subject.name,
                                'coefficient': subject.coefficient}
                title = "Update or View Subjects"
                form = SubjectForm(initial=initial_data)
            else:
                form=SubjectForm()
                title = "Add or View Subjects"
                
            items = Subject.objects.all()
            context = {
                'items':items,
                'form':form,
                'title':title,
                    }
            return render(request,"attendance/subjectTemplate.html",context)
        return HttpResponse("YOU ARE NOT ALLOWED ACCESS  INTO THIS SECTION")
       
    

def deleteSubject(request,id):
    if request.user.user_type=='1':
        subject=Subject.objects.get(id=id)
        subject.delete()
        return redirect('attendance:add-subject')
    return HttpResponse("YOU ARE NOT ALLOWED ACCESS  INTO THIS SECTION")


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
def StaffTakeAttendance_statu_update(request,a_id,s_id):
    if request.user.user_type == '2':
        
        student=Student.objects.get(id=s_id)
        attendance = AttendanceReport.objects.get(
            id=a_id, student_id=student, attendance_date=timezone.now())
        print(attendance.status)
        if attendance.status == True:
            attendance.status=0
            status_report = "absent"
            
        else:
            attendance.status=1
            status_report="present"
        
        attendance.save()
    
        # print(a_id,s_id)
        

        return HttpResponse(f"<span class='text-center'>{student.admin.username} has been marked {status_report}</span>") 
    return HttpResponse("YOU ARE NOT ALLOWED ACCESS  INTO THIS SECTION")
