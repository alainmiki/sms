
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

import random
# Create your views here.
from .models import FinalTimetable, Period, TimeTable
from .forms import ClassTimetableFilterForm, PeriodForm, StaffTimetableFilterForm, TimeTableForm



def to_seconds(sec):
    seconds=0
    for part in sec.split(":"):
        seconds=seconds*60+int(part,10)
        # print(sec.split(":"))
    return seconds

class TimeTableView(View):
    
    def get(self,request,id=None):
        if id != None:
            instance=TimeTable.objects.get(id=id)
            initial={
                "staff_id":instance.staff_id,
                "class_id":instance.class_id,
                "subject_id":instance.subject_id,
                "department_id":instance.department_id,
                "day":instance.day,
                # "start_time":instance.start_time,
                # "end_time":instance.end_time,
            }
            form=TimeTableForm(initial=initial)
        else:
            form=TimeTableForm()
        
        context={
            'form':form,
            'timetable_obj':TimeTable.objects.all().order_by("-created_date")
        }
        return render(request,"timetable/timetableForm.html",context)
    
        # return HttpResponse("get return this shit nigga")
    def post(self,request,id=None):
        print(request.POST)
        
        if id == None:
            form=TimeTableForm(request.POST)
        else:
            instance=TimeTable.objects.get(id=id)
            form=TimeTableForm( request.POST,instance=instance)
            print('update')
            
            
        
        if form.is_valid():
            staff_id=form.cleaned_data['staff_id']
            class_id=form.cleaned_data['class_id']
            day=form.cleaned_data['day']
            # start_time=form.cleaned_data['start_time']
            # end_time=form.cleaned_data['end_time']
            
            timetable=TimeTable.objects.filter(day=day).count()
            if timetable>=9:
                messages.info(request,f"{day} already has 9 periods ")
            else:
                form.save()
            return redirect("timetable:timetable-reg")
        else:
            # return HttpResponse(f"<h3 class='text-center text-info bg-danger'>Your Form is invalid make sure to fill everything carefully</h3> : {form.errors}")
            messages.warning(request,"Your Form is invalid make sure to fill everything carefully")
            context={
                "form":form,
            }
            return render(request,"timetable/timetableForm.html",context)
    

class SetPeriods(View):
    def get(self,request,id=None):
        if id != None:
            p=Period.objects.get(id=id)
            initial={
                "name":p.name,
                "start_time":p.start_time,
                "end_time":p.end_time,
            }
            form=PeriodForm(initial=initial)
        else:
            form=PeriodForm()
        context={
            'form':form,
            'periods':Period.objects.all()
        }
        return render(request,"timetable/period.html",context)    
    def post(self,request,id=None):
        if id != None:
            p=Period.objects.get(id=id)
           
            form=PeriodForm(request.POST,instance=p)
        else:
            form=PeriodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("timetable:period-reg")
        else:
            # return HttpResponse(f"<h4 class='alert text-info bg-warning'> The data you send was not valid please check and send again </h4>")
            context={
                'form':PeriodForm,
                'periods':Period.objects.all()
            }
            return render(request,"timetable/period.html",context)      
    

# def automate_timetable(request): 
#     timetable=TimeTable.objects.all()
#     period=Period.objects.all().exclude()
#     period=period.exclude(name="break").order_by("name")
#     monday=[t for t in timetable.filter(day='Mon')]
#     period=[p for p in period]
#     period.reverse()
    
#     # print(period,monday)
#     numbers=[]
#     ps=[]
    
#     # print(pn)
    
#     while period:
#         n=random.randint(0,len(monday)-1)
#         pn=list(range(len(period)))
#         # print(n)
#         if n not in numbers:
#             numbers.append(n)
#             ps.append(pn)
#             print(monday[n],n,)
#             print(period.pop(),pn.pop())
#             # period.pop(pn.pop())
#             print(period)
#         # if pn==len(period)-1:
#         #     pn=0
#         #     # n=random.randint(0,len(monday)-1)
#         # else:
#         #     pn+=1
    
#     return HttpResponse('automate timetable')
   
class TimeTableOutputView(View):   
    
    def get(self,request):
        form=StaffTimetableFilterForm()
        search_query = TimeTable.objects.all()
       
        timetable = search_query
        Mon=timetable.filter(day='Mon')
        Tues=timetable.filter(day='Tues')
        Wed=timetable.filter(day='Wed')
        Thurs=timetable.filter(day='Thurs')
        Fri=timetable.filter(day='Fri')
        
        period=Period.objects.all().exclude()
        period=period.exclude(name="break").order_by("name")
        monday=[t for t in timetable.filter(day='Mon')]
        period=[p for p in period]
        period.reverse()
        
       
        context={
            'timetable_obj': timetable,
            'monday':Mon,"tuesday":Tues,"wednesday":Wed,"thursday":Thurs,"friday":Fri,
             'class':True,
             'class1':"General school",
            "form":form
        }
    
        return render(request,"timetable/manage_timetable.html",context)
    def post(self,request):
        
        return HttpResponse("ok posted")
    
    
def timetable_class_filter(request):
    
    form = ClassTimetableFilterForm(request.POST)
   
    if form.is_valid():
        filter_by=form.cleaned_data['filter_by']
      
        search_query = TimeTable.objects.filter(class_id=filter_by)
       
        timetable = search_query
        if timetable==[]:
            # messages.error(request,"There is no data in the filtered category")
            return HttpResponse("There is no data in the filtered category")
        
        Mon=[t for t in timetable.filter(day='Mon')]
        Tues=[t for t in timetable.filter(day='Tues')]
        Wed=[t for t in timetable.filter(day='Wed')]
        Thurs=[t for t in timetable.filter(day='Thurs')]
        Fri=[t for t in timetable.filter(day='Fri')]
        days=[Mon,Tues,Wed,Thurs,Fri]
        
       
       
        # print(pn)
        
        for day in days:
            period=Period.objects.all()
            period=period.exclude(name="break").order_by("name")
        
            period=[p for p in period]
            period.reverse()
            numbers=[]
            ps=[]
    
            # print(day,period)
            if len(day)>0:
                while period:
                    n=random.randint(0,len(day)-1)
                    pn=list(range(len(period)))
                    # print(n)
                    if n not in numbers:
                        numbers.append(n)
                        ps.append(pn)
                        
                        p=period.pop()
                        if FinalTimetable.objects.filter(day=day[n].day,class_id=filter_by,period=p).exists():
                            print('class and day already exist')
                        else:
                            if FinalTimetable.objects.filter(staff_table=day[n],period=p).exists():
                                print("existe")
                            else:
                                FinalTimetable.objects.create(class_id=filter_by,staff_table=day[n],day=day[n].day,period=p)
                        # period.pop(pn.pop())
                        # print(period)
                else:
                    pass
        
        timetable=FinalTimetable.objects.filter(class_id=filter_by).order_by('period__start_time')
        Mon=timetable.filter(day='Mon')
        Tues=timetable.filter(day='Tues')
        Wed=timetable.filter(day='Wed')
        Thurs=timetable.filter(day='Thurs')
        Fri=timetable.filter(day='Fri')
        
        # print([Mon,Tues,Wed,Thurs,Fri])
        
        context = {
            'timetable_obj': timetable,
            'monday':Mon,"tuesday":Tues,"wednesday":Wed,"thursday":Thurs,"friday":Fri,'break':Period.objects.get(name="break"),
            'class1':filter_by,
            'form': form,

        }
        # print(timetable) 
        return render(request,'timetable/printableTimetable.html',context)
        # return HttpResponse(f'working well {filter_by} ,{class_room} ')
    
    return HttpResponse(f'Warning error: {form.errors}')

def timetable_staff_filter(request):
    
    form = StaffTimetableFilterForm(request.POST)
   
    if form.is_valid():
        filter_by=form.cleaned_data['filter_by']
      
        search_query = FinalTimetable.objects.filter(staff_table__staff_id=filter_by).order_by('period')
       
        timetable = search_query
        if timetable==[]:
            # messages.error(request,"There is no data in the filtered category")
            return HttpResponse("There is no data in the filtered category")
        
        Mon=timetable.filter(day='Mon')
        Tues=timetable.filter(day='Tues')
        Wed=timetable.filter(day='Wed')
        Thurs=timetable.filter(day='Thurs')
        Fri=timetable.filter(day='Fri')
        
        # print(Mon[0].start_time, to_seconds(str(Mon[0].start_time)))
        
        context = {
            'timetable_obj': timetable,
            'class':True,
            'class1':filter_by,
            'monday':Mon,"tuesday":Tues,"wednesday":Wed,"thursday":Thurs,"friday":Fri,
            
            'form': form, 

        }
        # print(timetable)
        return render(request,'timetable/printableTimetable.html',context)
        # return HttpResponse(f'working well {filter_by} ,{class_room} ')
    
    return HttpResponse(f'Warning error: {form.errors}')



def get_by_view(request,get_by):
    get_by=str(get_by).strip(" ")
    if get_by =='staff':
        form=StaffTimetableFilterForm()
        print("inside staff")
    elif get_by=='class':
        print("inside class")
        form=ClassTimetableFilterForm()
  
    context={
        "form":form
        }
    
    return render(request,"timetable/timetablePatialForm.html",context)