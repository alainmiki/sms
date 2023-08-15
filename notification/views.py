from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from adminhod.models import Event
from guardian.models import NotificationGuardian
from student.models import NotificationStudent
from teacher.models import NotificationStaff

from  asgiref.sync import sync_to_async


@sync_to_async
def events(request):
    events=Event.objects.all().order_by('-end_date_and_time','-start_date_and_time')
    
    context={
        'events':events, 'time': timezone.now(),
    }
    
    return render(request,'events.html',context)

@sync_to_async
def notify(request):
    if request.user.user_type=='2':
        events=  NotificationStaff.objects.filter(staff_id__admin=request.user,status=False).order_by('-created_at')[:6]
        
    elif request.user.user_type=='3':
        events =  NotificationStudent.objects.filter(student_id__admin=request.user,status=False).order_by('-created_at')[:6]
        
    elif request.user.user_type=='4':
        events =  NotificationGuardian.objects.filter(guardian_id__admin=request.user,status=False).order_by('-created_at')[:6]
        
    else:
        return HttpResponse("not allowed")
    context={
        'notify': events,
    }
    
    return render(request,'notifipatial.html',context)


def full_notification(request,id=None):
    
    if request.user.user_type=='2':
        if id != None:
            ev=NotificationStaff.objects.get(id=id)
            ev.status=True
            ev.save()
        events=  NotificationStaff.objects.filter(staff_id__admin=request.user,status=False).order_by('-created_at')
        
    elif request.user.user_type=='3':
        if id != None:
            ev=NotificationStudent.objects.get(id=id)
            ev.status=True
            ev.save()
        events =  NotificationStudent.objects.filter(student_id__admin=request.user,status=False).order_by('-created_at')
        
    elif request.user.user_type=='4':
        if id != None:
            ev=NotificationStudent.objects.get(id=id)
            ev.status=True
            ev.save()
        events =  NotificationGuardian.objects.filter(guardian_id__admin=request.user,status=False).order_by('-created_at')
        
    else:
        return HttpResponse("not allowed")
    context={
        'notifications': events,
    }
    
    return render(request,'notifications.html',context)