
from django.http import HttpResponse
from django.shortcuts import redirect, render
from asgiref.sync import sync_to_async
from django.views import View
from django.contrib import messages
from student.models import Guardian, Subject
from marks.forms import FilterForm, FilterFormAdmin, MarkForm, ReportCardForm, markgenForm, markgenFormAdmin
from marks.models import Mark, StudentAverage, StudentSubjectAverageGrade
from student.models import ClassRoom, Department, Student
from teacher.models import Staff
from schoolinfo.models import SchoolInformation

# Create your views here.


class MarksGenView(View):
    def get(self,request):
        if request.user.user_type=='1' or request.user.user_type=='2':
            if request.user.user_type=='1':
                form=markgenFormAdmin()
            else:
                form = markgenForm()
            last_10_records=Mark.objects.all()
            context={
                'form':form,
                'marks': last_10_records,
            }
            if request.user.user_type=='1':
                return render(request,'marks/markForm.html',context)
            else:
                last_10_records = Mark.objects.filter(staff_id__admin__username=request.user.username).order_by('student_id__admin__first_name','student_id__admin__last_name')
                context = {
                'form': form,
                'marks': last_10_records,
            }
                return render(request, 'marks/teacherMarkForm.html', context)
            
        else:
            return HttpResponse("You are not allowed to access this section")
    # @sync_to_async
    def post(self,request):
        if request.user.user_type=='1' or request.user.user_type=='2':
            if request.user.user_type=='1':
                form=markgenFormAdmin(request.POST)
            else:
                form = markgenForm(request.POST)
                
            if form.is_valid():
                if request.user.user_type=='1':
                    staff_id =form.cleaned_data['staff_id']
                else:
                    staff_id =Staff.objects.get(admin= request.user)
                class_id = form.cleaned_data['class_id']
                subject_id = form.cleaned_data['subject_id']
                department_id = form.cleaned_data['department_id']
                semester = form.cleaned_data['semester']
                month = form.cleaned_data['month']
                print(staff_id,class_id,subject_id,department_id,semester)
                # return HttpResponse("working well")
                if Mark.objects.filter(staff_id=staff_id,class_id=class_id,subject_id=subject_id,semester=semester,month=month,).exists():
                    marks=Mark.objects.filter(staff_id=staff_id,class_id=class_id,subject_id=subject_id,semester=semester,month=month,).order_by('student_id__admin__first_name','student_id__admin__last_name')
                else:
                    if department_id!=None:
                        student_obj=Student.objects.filter(class_room=class_id,department=department_id)
                        for student in student_obj:
                            Mark.objects.create(staff_id=staff_id,class_id=class_id,subject_id=subject_id,semester=semester,student_id=student,test_mark=0,exam_mark=0,home_work=0,project=0,department_id=department_id,month=month)
                    else:
                        student_obj=Student.objects.filter(class_room=class_id)
                    
                        for student in student_obj:
                            Mark.objects.create(staff_id=staff_id,class_id=class_id,subject_id=subject_id,semester=semester,month=month,student_id=student,test_mark=0,exam_mark=0,home_work=0,project=0)
                            
                    marks=Mark.objects.filter(staff_id=staff_id,class_id=class_id,subject_id=subject_id,semester=semester,month=month).order_by('student_id__admin__first_name','student_id__admin__last_name')
                context={
                    'marks':marks,
                }
                return render(request,'marks/editableMarksTable.html',context)
            return HttpResponse("mark sure to fill the above form before submitting")
                
                
                
        else:
            return HttpResponse("You are not allowed to access this section")


class MarksFilling(View):
    def get(self,request,mk_id=None,id=None,c_value=None):
        if request.user.user_type=='1' or request.user.user_type=='2':
            if id=='home_work':
                # hx-target='#test{mk_id}' 
                return HttpResponse(f"<input type='text' value={c_value} name='home_work' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            
            elif id=='test':
                # hx-target='#test{mk_id}' 
                return HttpResponse(f"<input type='text' value={c_value} name='test' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            
            elif id=='exam':
                return HttpResponse(f"<input type='text' value={c_value} name='exam' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            
            elif id=='project':
                return HttpResponse(f"<input type='text' value={c_value} name='project' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            
            elif id=='exam_o':
                return HttpResponse(f"<input type='text' value={c_value} name='exam_o' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            elif id=='project_o':
                return HttpResponse(f"<input type='text' value={c_value} name='project_o' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            
            elif id=='test_o':
                return HttpResponse(f"<input type='text' value={c_value} name='test_o' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            
            elif id=='home_work_o':
                return HttpResponse(f"<input type='text' value={c_value} name='home_work_o' class='form-control rounded' hx-post='record-marks_fill/{mk_id}/{id}/{c_value}' hx-trigger='change delay:1s' hx-swap='outerHTML' >")
            
            else:
                return HttpResponse("not valid")
                
        else:
            return HttpResponse("You are not allowed to access this section")


    def post(self,request,mk_id=None,id=None,c_value=None):
        if request.user.user_type=='1' or request.user.user_type=='2':
            if id=='test':
                test=request.POST.get("test")
                mark=Mark.objects.get(id=mk_id)
                mark.test_mark=float(test)
                mark.save()
                # return HttpResponse(f"{float(test)}")
                return HttpResponse(f"<td class='jsgrid-cell' style='width: 200px;background:gray;' id='test{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(test)}</td>")
            
            elif id=='exam':
                exam=request.POST.get("exam")
                mark=Mark.objects.get(id=mk_id)
                mark.exam_mark=float(exam)
                mark.save()
                # return HttpResponse(f"{float(exam)}")
                return HttpResponse(f"<td class='jsgrid-cell' style='width: 200px;background:gray;' id='test{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(exam)}</td>")
            
            elif id=='project':
                project=request.POST.get("project")
                mark=Mark.objects.get(id=mk_id)
                mark.project=float(project)
                mark.save()
                # return HttpResponse(f"{float(exam)}")
                return HttpResponse(f"<td class='jsgrid-cell' style='width: 200px;background:gray;' id='project{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(project)}</td>")
            
            elif id=='home_work':
                home_work=request.POST.get("home_work")
                mark=Mark.objects.get(id=mk_id)
                mark.home_work=float(home_work)
                mark.save()
                # return HttpResponse(f"{float(exam)}")
                return HttpResponse(f"<td class='jsgrid-cell' style='width: 200px;background:gray;' id='home_work{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(home_work)}</td>")
            
            
            elif id=='exam_o':
                exam_ov=request.POST.get("exam_o")
                mark=Mark.objects.get(id=mk_id)
                mark.exam_on=float(exam_ov)
                mark.save()
                return HttpResponse(f"<td class='jsgrid-cell bg-secondary' style='width: 200px;background:gray;' id='test{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(exam_ov)}</td>")
            
            elif id=='project_o':
                project_ov=request.POST.get("project_o")
                mark=Mark.objects.get(id=mk_id)
                mark.project_on=float(project_ov)
                mark.save()
                return HttpResponse(f"<td class='jsgrid-cell bg-secondary' style='width: 200px;background:gray;' id='project_o{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(project_ov)}</td>")
            
            
            elif id=='home_work_o':
                home_work_ov=request.POST.get("home_work_o")
                mark=Mark.objects.get(id=mk_id)
                mark.home_work_on=float(home_work_ov)
                mark.save()
                return HttpResponse(f"<td class='jsgrid-cell bg-secondary' style='width: 200px;background:gray;' id='home_work_o{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(home_work_ov)}</td>")
            
            elif id=='test_o':
                test_ov=request.POST.get("test_o")
                mark=Mark.objects.get(id=mk_id)
                mark.test_on=float(test_ov)
                mark.save()
                return HttpResponse(f"<td class='jsgrid-cell bg-secondary' style='width: 200px;background:gray;' id='test{mk_id}' hx-get='get-fill-input/{mk_id}/{id}/{c_value}' hx-swap='outerHTML' hx-trigger='click once'>{float(test_ov)}</td>")
            
            else:
                return HttpResponse("not valid")
            
            # print(request.POST,mk_id,id)
        else:
            return HttpResponse("You are not allowed to access this section")



# this class is not used
class MarksView(View):
    
    def get(self,request,id=None):
        if request.user.user_type=='1' or request.user.user_type=='2':
            if id != None:
                instance = Mark.objects.get(id=id)
                initial={
                    "student_id":instance.student_id,
                    "staff_id":instance.staff_id,
                    "class_id":instance.class_id,
                    "subject_id":instance.subject_id,
                    "semester":instance.semester,
                    
                    "test_mark":instance.test_mark,
                    "test_on":instance.test_on,
                    
                    "project":instance.project,
                    "project_on":instance.project_on,
                    
                    "home_work":instance.home_work,
                    "home_work_on":instance.home_work_on,
                    
                    "exam_mark":instance.exam_mark,
                    "exam_on":instance.exam_on,
                    
                }
                form = MarkForm(initial=initial)
            else:
                form = MarkForm()
            last_10_records=Mark.objects.all()[:10]
            context={
                'form':form,
                'marks': last_10_records,
            }
            if request.user.user_type=='1':
                return render(request,'marks/markForm.html',context)
            else:
                last_10_records = Mark.objects.filter(staff_id__admin__username=request.user.username)[:10]
                context = {
                'form': form,
                'marks': last_10_records,
            }
                return render(request, 'marks/teacherMarkForm.html', context)
            
        else:
            return HttpResponse("You are not allowed to access this section")
        
        
    def post(self,request,id=None):
        if request.user.user_type == '1' or request.user.user_type == '2':
            if id !=None:
                instance=Mark.objects.get(id=id)
                form=MarkForm(request.POST,instance=instance)
            else:
                form=MarkForm(request.POST)
                
            if form.is_valid():
                student = form.cleaned_data['student_id']
                class_id = form.cleaned_data['class_id']
                if Student.objects.filter(admin__username=student, class_room__name=class_id).exists():
                    form.save()
                    return redirect('marks:record-marks')
                else:
                    messages.error(
                        request, "student and class did NOT MATCH!. make sure the student is a student of  the class you selected")
                    pass

                # print(form.errors)
            context = {
                'form': form,
            }
            if request.user.user_type == '1':
                return render(request, 'marks/markForm.html', context)
            else:
                return render(request, 'marks/teacherMarkForm.html', context)

        else:
            return HttpResponse("You are not allowed to access this section")

# this class is not used
class MarksUpdateView(View):

    def get(self, request, id=None):
        if request.user.user_type == '1' or request.user.user_type == '2':
           
            instance = Mark.objects.get(id=id)
            initial = {
                "student_id": instance.student_id,
                "staff_id": instance.staff_id,
                "class_id": instance.class_id,
                "subject_id": instance.subject_id,
                "semester": instance.semester,
                "test_mark": instance.test_mark,
                "test_on": instance.test_on,
                "exam_mark": instance.exam_mark,
                "exam_on": instance.exam_on,

            }
            form = MarkForm(initial=initial)
           
            last_10_records = Mark.objects.all()[:10]
            context = {
                'form': form,
                'marks': last_10_records,
            }
            if request.user.user_type == '1':
                return render(request, 'marks/markForm.html', context)
            else:
                last_10_records = Mark.objects.filter(
                    staff_id__admin__username=request.user.username)[:10]
                context = {
                    'form': form,
                    'marks': last_10_records,
                }
                return render(request, 'marks/teacherMarkForm.html', context)

        else:
            return HttpResponse("You are not allowed to access this section")

    def post(self, request, id=None):
        if request.user.user_type == '1' or request.user.user_type == '2':
            instance = Mark.objects.get(id=id)
            form = MarkForm(request.POST, instance=instance)
            
            if form.is_valid():
                student = form.cleaned_data['student_id']
                class_id = form.cleaned_data['class_id']
                if Student.objects.filter(admin__username=student, class_room__name=class_id).exists():
                    form.save()
                    return redirect('marks:record-marks')
                else:
                    messages.error(
                        request, "student and class did NOT MATCH!. make sure the student is a student of  the class you selected")
                    pass
               
            context = {
                'form': form,
            }
            if request.user.user_type == '1':
                return render(request, 'marks/markForm.html', context)
            else:
                return render(request, 'marks/markForm1.html', context)

        else:
            return HttpResponse("You are not allowed to access this section")
        
        
def manage_marks(request):
    if request.user.user_type == '1':

        marks = Mark.objects.all().order_by('class_id','-student_id')
        
        context = {
            'marks':marks,
            'form': FilterFormAdmin()
            
        }
        
        # print(FilterForm())
        return render(request, 'marks/manage_marks.html', context)
    elif request.user.user_type == '2':
        
        marks = Mark.objects.filter(staff_id__admin=request.user).order_by('class_id','-student_id')
        
        context = {
            'marks':marks,
            'form': FilterForm()
            
        }
        
        # print(FilterForm())
        return render(request, 'marks/teacherManageMarks.html', context)
        
    elif request.user.user_type == '4':
        
        marks = Mark.objects.filter(staff_id__admin=request.user).order_by('class_id','-student_id')
        
        context = {
            'marks':marks,
            'form': FilterForm()
            
        }
        
        # print(FilterForm())
        return render(request, 'marks/teacherManageMarks.html', context)
        
        
        
        
    else:
        return HttpResponse("This is a warning from the head office \n This section is restricted so be warn")


def mark_filter(request):
    
    form = FilterForm(request.POST)
   
    # get_by=request.POST['getby']
    filter_by = request.POST['filter_by']
    sort_by = request.POST['sort_by']
    get_by = request.POST['get_by']
    class_room = request.POST['class_room']
    data=None
    if filter_by == 'class':
        data = Mark.objects.filter(class_id__name=get_by)

    elif filter_by =='subject':
        data=Mark.objects.filter(subject_id__name=get_by)
        
    elif filter_by =='student':
        data=Mark.objects.filter(student_id__admin__username=get_by)
        
    elif filter_by =='department':
        data=Mark.objects.filter(department_id__name=get_by)
        
    elif filter_by =='staff':
        # print(get_by)
        data=Mark.objects.filter(staff_id__admin__username=get_by)
        
    elif filter_by =='semester':
        data=Mark.objects.filter(semester=get_by)
        
    elif filter_by =='month':
        data=Mark.objects.filter(month=get_by)
        
    if get_by =='all':
        data=Mark.objects.all()
        # print(filter_by,get_by)
        
    if class_room!='all':
        data=data.filter(class_id__name=class_room)
    
    if sort_by !='all' and data!=None:
        data=data.all().order_by('-'+str(sort_by))
    else:
        data == Mark.objects.all()
        
        
        
    # print(filter_by,get_by)
    if request.user.user_type=='2':
        marks=data.filter(staff_id__admin=request.user)
        form = FilterForm(request.POST)
    else:
        marks = data
        form = FilterFormAdmin(request.POST)
    if marks==[]:
        # messages.error(request,"There is no data in the filtered category")
        return HttpResponse("There is no data in the filtered category")
    
    context = {
        'marks': marks,
        
        'form': form,

    }
    # print(marks, form)
    return render(request,'marks/marksTable.html',context)

    
    # return HttpResponse(f'Warning error: {form.errors}')

def filterBy(request):
    
    ftby=request.POST.get('filter_by')
    if ftby == 'class':
        data=ClassRoom.objects.all()
        list_it=False
        by_student = False
        by_class=True
    elif ftby =='subject':
        data=Subject.objects.all()
        list_it=False
        by_class=False
        by_student=False
    elif ftby =='department':
        data=Department.objects.all()
        list_it=False
        by_class=False
        by_student=False
    elif ftby =='student':
        data=Student.objects.all()
        by_student=True
        list_it=False
        by_class=False
    elif ftby =='staff':
        if request.user.user_type=="2":
            data=[]
        else:
            data=Staff.objects.all()
        by_student=True
        list_it=False
        by_class=False
        
    elif ftby =='semester':
        data=['ft','st','tt']
        list_it=True
        by_class = False
        by_student = False
        
    elif ftby =='month':
        data=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
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
        'object': data, 'list_it': list_it, 'by_student': by_student,'by_class':by_class
    }
    
    return render(request,'marks/patialInput.html',context)


def guardian_marks_home(request):
    
    user=Guardian.objects.get(admin=request.user)
    children=user.children.all()
    # print("children:",children)
    
    if children.count() >0:
    
        context= {
                "children":children,
                "marks":Mark.objects.filter(student_id=children[0]),
                "guardian":True,
                "name":children[0],
            }
            
        return render(request,"marks/staff_manage_marks.html",context)

def get_marks_byChild_name(request):
    child=request.POST['child']
    filter_by=request.POST['filter-by']
    student=Student.objects.get(id=child)
    
    if filter_by =='all':
        marks=Mark.objects.filter(student_id=child)
    else:
        marks=Mark.objects.filter(student_id=child,semester=filter_by)
    # print(marks)
    if marks.exists():
        context= {
                "marks":marks,
                "guardian":True,
                "name":student,
                }
            
        
        return render(request,"marks/marksTable.html",context)
    else:
        return HttpResponse(f"<h4 class='text-info bg-warning'>{student} doesn't yet have marks for this Semester/Trimester</h4>")
    
class ReportCardView(View):
    def post(self,request):
        class_id=request.POST["class_id"]
        # print(class_id)
        staff_id=request.POST["staff_id"]
        semester=request.POST["semester"]
        month=request.POST["month"]
        report_type=request.POST["report_type"]
        students=Student.objects.filter(class_room=class_id)
        school_info=SchoolInformation.objects.all()[0]
        
        # monthly report section
        if report_type =="monthly":  
            
            # print("monthly")
            monthly=True
            marks=Mark.objects.only("month","subject_id","student_id","home_work","home_work_on","test_mark","test_on").filter(class_id=class_id,month=month,semester=semester)
            if not marks.exists():
                return HttpResponse(f"<h1 class='alert bg-dark text-danger'> No data found in the database for this {report_type} . so check well before submiting  </h2>")
            
            marks_by_student_list=[]
            student_list=[]
            
            for student in students:
                # looping through all students  and filtering their marks
                s_marks=marks.filter(student_id=student)
            
                # student_list.append(student)
                
                hts=[]
                subject_mark=[]
            
                # for student_mark,student in zip(marks_by_student_list,student_list):
                for subject in Subject.objects.all():
                    # looping through all subjects and filtering their data 
                    st_mark_query=s_marks.filter(subject_id=subject,student_id=student)
                    sum_hts=0
                    for st_mark in st_mark_query:
                        
                        # going through all the data filter from student data through subjects
                        
                        if st_mark:
                            ht=(st_mark.home_work+st_mark.test_mark)/(st_mark.home_work_on+st_mark.test_on)*100
                            hts.append(ht)
                            
                            
                            
                            subject_mark.append({"subject":st_mark,'ht':ht})
                            # print(ht,subject)
                            # print(sum_hts)
                            
                    
                av=round((sum(hts)/len(hts)),2)
                print(av,hts)
                grade=''
                if av>80:grade='A'
                elif av<80 and av>=70: grade="B"
                elif av <70 and av>50: grade="C"
                elif av <50 and av>30: grade="D"
                else:grade="U"
                marks_by_student_list.append({"marks":s_marks,"subject_mark":subject_mark,'hts':hts,"average":av,"grade":grade,"student":student})
                
            context={
            'monthly':monthly,
            'staff':Staff.objects.get(pk=staff_id),
            "schoolinfo":school_info,
            'marks_by_student_list':marks_by_student_list,
            }
            
            # return HttpResponse("changed")
    
            return render(request,"report/reportcardcontent.html",context)
            
        # termly assesment report section
        else:
            # print("trimesters")
            monthly=False
            marks=Mark.objects.filter(class_id=class_id,semester=semester)
            if not marks.exists():
                return HttpResponse(f"<h1 class='alert bg-dark text-danger'> No data found in the database for this {report_type} . so check well before submiting  </h2>")
        
        # marks=Mark.objects.filter(class_id=class_id)
        
        
            marks_by_student_list=[]
            student_list=[]
            
            for student in students:
                s_marks=marks.filter(student_id=student)
            
                student_list.append(student)
                
                hts=[]
                htps=[]
                subject_mark=[]
                
                content=[]
            
                # for month in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']:
              
                subject_obj=None
                for subject in Subject.objects.all():
                    
                    st_mark_query=s_marks.filter(subject_id=subject,student_id=student)
                    if st_mark_query.exists():
                        
                        htp=0
                        c=0
                        hw_total=0
                        hw_on_total=0
                        exam_total=0
                        exam_on_total=0
                        test_total=0
                        test_on_total=0
                        project_total=0
                        project_on_total=0
                        for st_mark in st_mark_query:
                        
                            if st_mark:
                                subject_obj=subject
                                hw_total+=float(st_mark.home_work)
                                hw_on_total+=st_mark.home_work_on
                                
                                
                                test_total+=float(st_mark.test_mark)
                                test_on_total+=st_mark.test_on
                                
                                if st_mark.exam_mark >0 or st_mark.exam_mark >= 1:
                                    exam_total+=float(st_mark.exam_mark)
                                    exam_on_total+=st_mark.exam_on
                                else:
                                    exam_total+=float(0)
                                    exam_on_total+=0
                                
                                if st_mark.project >0 or st_mark.project >= 1:
                                    project_total+=float(st_mark.project)
                                    project_on_total+=st_mark.project_on
                                else:
                                    project_total+=float(0)
                                    project_on_total+=0
                                    
                                    
                                # ht=(st_mark.home_work+st_mark.test_mark)/(st_mark.home_work_on+st_mark.test_on)*100
                                # # hts.append(ht)
                                
                                # htp=(st_mark.home_work+st_mark.test_mark+st_mark.project)/(st_mark.home_work_on+st_mark.test_on+st_mark.project_on)*100
                                
                                # htps.append(htp)
                                c+=1
                                # subject_mark.append({"subject":st_mark,'ht':ht})
                                # subject_mark.append({"subject":st_mark,'ht':ht})
                                # print(ht,subject)
                                # print(st_mark.subject_id,st_mark.student_id,st_mark.month,ht)
                                sums=(hw_total,hw_on_total,test_total,test_on_total,project_total,project_on_total,exam_total,exam_on_total)
                                
                                totals=(round(hw_total/c,1),round(hw_on_total/c,1),round(test_total/c,1),round(test_on_total/c,1),round(project_total/c,1),round(project_on_total/c,1),round(exam_total/c,1),round(exam_on_total/c,1))
                                
                                ht=float((round(hw_total/c,1)+round(test_total/c,1)+round(project_total/c,1)) )/float((round(hw_on_total/c,1)+round(test_on_total/c,1)))*100
                                
                                htp=float((round(hw_total/c,1)+round(test_total/c,1)))/float((round(hw_on_total/c,1)+round(test_on_total/c,1)+round(project_on_total/c,1)))*100
                                
                                gtotal=float((round(hw_total/c,1)+round(test_total/c,1)+round(exam_total/c,1)))/float((round(hw_on_total/c,1)+round(test_on_total/c,1)+round(project_on_total/c,1)+round(exam_on_total/c,1)))*100
                                
                        footers_calculations=[round(ht,2),round(htp,2),round(gtotal,2)]
                        
                        # print(ht)
                        hts.append(gtotal)
                
                        content.append([st_mark_query,sums,totals,footers_calculations])
                        
                        
                        # storing subject averages and grades
                        if subject_obj:
                            classroom=ClassRoom.objects.get(pk=class_id)
                            grade=''
                            if gtotal>=90:grade='A*'
                            elif gtotal<90 and gtotal>=80: grade="A"
                            elif gtotal <80 and gtotal>=70: grade="B"
                            elif gtotal <70 and gtotal>=60: grade="C"
                            elif gtotal <60 and gtotal>=50: grade="D"
                            elif gtotal <50 and gtotal>=40: grade="E"
                            else:grade="U"
                            if StudentSubjectAverageGrade.objects.filter(class_id=classroom,student_id=student,semester=semester,subject_id=subject_obj).exists():
                                
                                subject_grade=StudentSubjectAverageGrade.objects.get(class_id=classroom,student_id=student,semester=semester,subject_id=subject_obj)
                                subject_grade.average=gtotal
                                subject_grade.grade=grade
                                subject_grade.save()
                            
                            else:
                                StudentSubjectAverageGrade.objects.create(class_id=classroom,student_id=student,semester=semester,subject_id=subject_obj,average=gtotal,grade=grade)
                        
                        # print(hw_total,hw_on_total,test_total,test_on_total,project_total,project_on_total,exam_total,exam_on_total,c)  
                # print("content")  
                # print(hts)  
                    
                av=round((sum(hts)/len(hts)),2)
                # print(av,len(hts))
                # av=54
                grade=''
                if av>=90:grade='A*'
                elif av<90 and av>=80: grade="A"
                elif av <80 and av>=70: grade="B"
                elif av <70 and av>=60: grade="C"
                elif av <60 and av>=50: grade="D"
                elif av <50 and av>=40: grade="E"
                else:grade="U"
                marks_by_student_list.append({"marks":s_marks,"subject_mark":content,'hts':hts,"average":av,"grade":grade,"student":student})
                
                classroom=ClassRoom.objects.get(pk=class_id)
                
                if StudentAverage.objects.filter(class_id=classroom,student_id=student,semester=semester).exists():
                    # print("exist")
                    student_data=StudentAverage.objects.get(class_id=classroom,student_id=student,semester=semester)
                    
                    student_data.average =av
                    student_data.save()
                else:
                    # print(" not  exist")
                    aver=StudentAverage.objects.create(class_id=classroom,student_id=student,semester=semester,average=av)
                    
                    subject_grade=StudentSubjectAverageGrade.objects.filter(class_id=classroom,student_id=student,semester=semester)
                    for subject_g in subject_grade:
                        aver.subjects_grades.add(subject_g)
                        aver.save()
                    # print(aver)

            # print(marks_by_student_list)
            trimester=''
            if semester=="st":
                trimester="Second Trimester"
            elif semester =="ft":
                trimester="First Trimester"
                
            elif semester =="tt":
                trimester="Third Trimester"
                
            context={
                'monthly':monthly,
                'trimester':trimester,
                'staff':Staff.objects.get(pk=staff_id),
                "schoolinfo":school_info,
                'marks_by_student_list':marks_by_student_list,
            }
            
            # return HttpResponse("changed")
        
            return render(request,"report/termreportcard.html",context)
        
    def get(self,request):
        context={
            "form":ReportCardForm,
        }
        return render(request,'report/reportcard.html',context)






# class MarksUpdateHtmxView(View):

#     def get(self, request, id=None):
#         if request.user.user_type == '1' or request.user.user_type == '2':
           
#             instance = Mark.objects.get(id=id)
#             initial = {
#                 "student_id": instance.student_id,
#                 "staff_id": instance.staff_id,
#                 "class_id": instance.class_id,
#                 "subject_id": instance.subject_id,
#                 "semester": instance.semester,
#                 "test_mark": instance.test_mark,
#                 "test_on": instance.test_on,
#                 "exam_mark": instance.exam_mark,
#                 "exam_on": instance.exam_on,

#             }
#             form = MarkForm(initial=initial)
           
#             last_10_records = Mark.objects.all()[:10]
#             context = {
#                 'form': form,
#                 'id': id,
#                 'marks': last_10_records,
#             }
#             if request.user.user_type == '1':
#                 return render(request, 'marks/markFormPatial.html', context)
#             else:
#                 return render(request, 'marks/markForm1.html', context)

#         else:
#             return HttpResponse("You are not allowed to access this section")

#     def post(self, request, id=None):
#         if request.user.user_type == '1' or request.user.user_type == '2':
#             instance = Mark.objects.get(id=id)
#             form = MarkForm(request.POST, instance=instance)
            
#             if form.is_valid():
#                 student = form.cleaned_data['student_id']
#                 class_id = form.cleaned_data['class_id']
#                 if Student.objects.filter(admin__username=student, class_id__name=class_id).exists():
#                     form.save()
#                     return redirect('marks:record-marks')
#                 else:
#                     messages.error(
#                         request, "student and class did NOT MATCH!. make sure the student is a student of  the class you selected")
#                     pass
               
#             context = {
#                 'form': form,
#                 'id':id,
#             }
#             if request.user.user_type == '1':
#                 return render(request, 'marks/markFormPatial.html', context)
#             else:
#                 return render(request, 'marks/markForm1.html', context)

#         else:
#             return HttpResponse("You are not allowed to access this section")
