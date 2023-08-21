from datetime import datetime

import os
from time import sleep
from django.http import HttpResponse,FileResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q

from django.utils import timezone
from django.views import View
from adminhod.models import CustomUser, Event, Gallery, PasswordStore
from guardian.forms import GuardianRegForm, GuardianUpdateForm
from marks.models import StudentAverage
from .forms import FeeForm, certificateFilterForm
from fees.models import Fee, OnlineFeesOnProgress, Receipt, ServicesTokenStorage
from guardian.models import Guardian
from library.models import DocumentOfStaff, Pass_Question,Library
from schoolinfo.models import Activity, SchoolInformation
from sms.forms import GetStudentForm
from student.forms import StudentRegistrationForm
from student.models import  Admission, ClassRoom,NotificationStudent, Student, StudentGovernment
from teacher.models import NotificationStaff
from django.contrib import messages
from django.contrib.auth import get_user_model

from  asgiref.sync import sync_to_async

from utils import generate_ref_code, receipt_generator, request_to_pay, send_email_func,get_pay_status



@sync_to_async
def student_government(request):
    candidates=StudentGovernment.objects.all()
    
    context={
        'candidates':candidates, 'time': timezone.now(),
    }
    
    return render(request,'student_government.html',context)


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
        
    else:
        return HttpResponse("not allowed")
    context={
        'notify': events,
    }
    
    return render(request,'notifipatial.html',context)


def full_notification(request):
    
    if request.user.user_type=='2':
        events=  NotificationStaff.objects.filter(staff_id__admin=request.user,status=False).order_by('-created_at')
        
    elif request.user.user_type=='3':
        events =  NotificationStudent.objects.filter(student_id__admin=request.user,status=False).order_by('-created_at')
        
    else:
        return HttpResponse("not allowed")
    context={
        'notifications': events,
    }
    
    return render(request,'notifications.html',context)


class Approve_admissions(View):
    
    def get(self,request,id=None):
        admissions=Admission.objects.all()
        context={'admissions':admissions,}
        return render(request,'approvedAdmissions.html',context)
    
    def post(self,request,id=None):
        admission=Admission.objects.get(id=id)
        email=admission.email
        first_name=admission.first_name
        last_name=admission.last_name
        # username=f"{first_name} {last_name}"
        gender=admission.gender
        place_of_birth = admission.place_of_birth
        
        address = admission.address
        phone=admission.phone
        class_room = admission.class_room
        department = admission.department
        date_of_birth = admission.date_of_birth
        
        profile_picture=admission.profile_picture
        guardian_profile_picture=admission.guardian_profile_picture
        
    
        user_type = admission.user_type
        student_uuid=generate_ref_code()
        passwd=f'{student_uuid}{first_name[1]}{last_name[1]}'
        initial={
            'first_name':first_name,'last_name':last_name,'email':email,'gender':gender,'place_of_birth':place_of_birth,'address':address,'phone':phone,'user_type':user_type,'profile_picture':profile_picture,'class_room':class_room,'department':department,'date_of_birth':date_of_birth,'password1':passwd,'password2':passwd
        }
        customuser=StudentRegistrationForm(initial)
        if CustomUser.objects.filter(email=email).exists():
            print("user with this email exist")
            # messages.info(request,"This email already has an account in our system please try another legit one")
            # admissions=Admission.objects.all()
            # context={'admissions':admissions,}
            # return render(request,'admissionList.html',context)
        #    =============this below lines are for bug finding=======
            # user_obj=CustomUser.objects.get(email=email)
            # if Student.objects.filter(admin=user_obj).exists():
            #     student = Student.objects.get(admin=user_obj)
            # else:
            #     student=Student.objects.create(admin=user_obj)
            #     student.date_of_birth=date_of_birth
            #     student.class_room = class_room
            #     student.department = department
            #     student.save()
            # ==========================================================
        else:
            if customuser.is_valid():
                # print('valid',passwd)
            
                instance=customuser.save()
                instance.username=f'{first_name} {last_name}'
                instance.uid=student_uuid
                instance.set_password(passwd)
                
                instance.profile_picture=profile_picture
                
                instance.save()
                print(instance.check_password(passwd),passwd)
                student = Student.objects.get(admin=instance)
                student.date_of_birth=date_of_birth
                student.class_room = class_room
                student.department = department
                
                
                student.save()
            
                send_email_func(recipient_list=[email,],from_email="smsprogram@gmail.com",body=f"Hay Dear {first_name} {last_name} Your admission into our school has been approved here is your password:'{passwd}'. Use it to login into your account with the combination of your Email:'{email}'",subject="Your Admission into our School has been approved",)
            
                send_email_func(recipient_list=[email,],from_email="smsprogram@gmail.com",body=f"Hay Dear {first_name} {last_name} here is your password:'{passwd}'. Use it to login into your account with the combination of your Email:'{email}'",subject="Your School website Account Password",)
            
            else:
                print('not valid',customuser.errors)
                
        guardian_title=admission.guardian_title
        guardian_full_name = admission.guardian_full_name
        guardian_address = admission.guardian_address
        guardian_phone=admission.guardian_phone
        guardian_email=admission.guardian_email
        student = Student.objects.get(admin=instance)
        
        if CustomUser.objects.filter(username=guardian_full_name,email=guardian_email).exists():
            guardian_object=Guardian.objects.get(admin__email=guardian_email)
            guardian_object.children.add(student)
            guardian_object.save()
        else:
            names=str(guardian_full_name).split(' ')
            firstname=names[0]
            lastname=' '.join(names[1:])
            uuid=generate_ref_code()
            passwd1=f'{uuid}{first_name[1]}{last_name[1]}'
            
            user=get_user_model().objects.create_user(email=guardian_email,username=guardian_full_name,user_type='4')
            user.set_password(passwd1)
            # user.user_type='4'
            user.uid=uuid
            user.first_name=firstname
            user.last_name=lastname
            user.address=guardian_address
            user.phone=guardian_phone
            user.profile_picture=guardian_profile_picture
            if guardian_title in  [ 'Mrs','Miss', 'Misses', 'Madam', "Sister"]:
                user.gender='F'
            elif guardian_title in  [ 'Mr', "Sir", 'Prof','Chief', "Senator"]:
                user.gender='M'
            else:
                user.gender="O"
            
            user.save()
            
           
            guardian_object=Guardian.objects.get(admin__email=guardian_email,admin__username=guardian_full_name)
            guardian_object.title=guardian_title
            guardian_object.save()
            # student = Student.objects.get(admin=instance)
            guardian_object.children.add(student)
            print(user,passwd1)
            send_email_func(recipient_list=[guardian_object.admin.email,],from_email="smsprogram@gmail.com",body=f"Hay {guardian_object.title}  {guardian_object.admin.username} here is your password:'{passwd1}'. Use it to login into our School account with the combination of your Email:'{guardian_object.admin.email}'. You are grand this access because your child has been admitted into you school",subject="Login Information in our School website Account Password",)
          
        send_email_func(recipient_list=[guardian_object.admin.email,],from_email="smsprogram@gmail.com",body=f"Hay Dear {guardian_object.title}  {guardian_object.admin.username} Your child by name '{student.admin.username}' admission into our school has been approved here is his/her password:'{passwd}'. He/she should Use it to login into his/her account with the combination his/her Email:'{student.admin.email}'",subject="Your child Admission into our School has been approved",)
    
        
       
            
        admission.delete()
        
        admissions=Admission.objects.all()
        context={'admissions':admissions,}
        return render(request,'admissionList.html',context)
        
        # return HttpResponse("Done")
        


def decline_admission(request,id):
    admission=Admission.objects.get(id=id)
    
    # messages.info(request,f"The following candidate has been decline and deleted:{admission.email}")
    admission.delete()
    admissions=Admission.objects.all()
    context={'admissions':admissions,}
    
    print("deleted")
    return render(request,'admissionList.html',context)

def librarybooks(request):
    
    context={
        'books':Library.objects.all()
    }
    
    return render(request,'librarybooks.html',context)       
        
def past_questions(request):
    
    context={
        'books':Pass_Question.objects.all()
    }
    return render(request,'pastquestions.html',context)       
        
def Document_staff(request):
    
    context={
        'books':DocumentOfStaff.objects.all()
    }
    return render(request,'staff_documents.html',context)       
        
def past_questions_view(request,id):
    book=Pass_Question.objects.get(id=id)
    context={
        'book':book
    }
    p=book.paper.path
    
    extension=os.path.basename(p).split('.')[1]
    # print(extension)
    if extension=='pdf':
        return FileResponse(open(p,'rb'),content_type=f'application/pdf')
    return render(request,'contentViewer.html',context)       
        
def librarybooks_view(request,id):
    book=Library.objects.get(id=id)
    context={
        'book':Library.objects.get(id=id),
        'bookobj':True,
    }
    # print(book.book.path)
    p=book.book.path
    
    extension=os.path.basename(p).split('.')[1]
    # print(extension)
    if extension=='pdf':
        return FileResponse(open(p,'rb'),content_type=f'application/pdf')

    return render(request,'contentViewer.html',context)       

        
def staffdocument_view(request,id):
    book=DocumentOfStaff.objects.get(id=id)
    context={
        'book':DocumentOfStaff.objects.get(id=id),
        'bookobj':True,
    }
    # print(book.book.path)
    p=book.document.path
    
    extension=os.path.basename(p).split('.')[1]
    # print(extension)
    if extension=='pdf':
        return FileResponse(open(p,'rb'),content_type=f'application/pdf')

    return render(request,'contentViewer.html',context)       


def gallery_view(request):
    
    context = {
        'gallery': Gallery.objects.all()
    }

    return render(request, 'gallery.html', context)


class OnlineFeesPay(View):
    
    def get(self,request):
        context={
            'form':GetStudentForm()
        }
        return render(request,"onlinefeesForm.html",context)
    
    def post(self,request):
        form=FeeForm(request.POST)
        context={
            'form':form,
            }
        if form.is_valid():
            print(form.cleaned_data)
            number=form.cleaned_data['phone']
            student_id=form.cleaned_data['student_id']
            class_room=form.cleaned_data['class_room']
            entry=form.cleaned_data['entry']
            amount=form.cleaned_data['amount']
            semester=form.cleaned_data['semester']
            # semester=form.cleaned_data['semester']
            amount_in_words=form.cleaned_data['amount_in_words']
            
            # res,x_ref,token=request_to_pay(amount,number)
            # print(res.status_code)
            # if res.status_code ==202:
                
            #     OnlineFeesOnProgress.objects.create(ref_id=x_ref,token=token,student_id=student_id,phone=number,class_room=class_room,entry=entry,amount=amount,semester=semester,amount_in_words=amount_in_words)
            # else:
            #     print("not accepted")
            
            
            messages.info(request,"please confirm the transaction on your phone. if a message does not pop up on your phone screen then dial:'*126#'. After you most have confirm the payment on your phone enter your child name on the new form below to get the receipt of your payment or if you are the child enter your name below to get your receipt if it doesn't show automatically ")
            
            receipts=Receipt.objects.filter(name=student_id)
            if receipts.exists():
                
                context['receipts']=receipts
                
            context['show']=True
            # return redirect(f"get_receipt")
            # if request.htmx:
            #     print(request,"htmx request")
            # return HttpResponseClientRedirect(f'get_receipt/{student_id}')
            return render(request,"feeFormPatial.html",context)
        else:
            return render(request,"feeFormPatial.html",context)

def news(request):
    # receipt=Receipt.objects.get()
    return HttpResponse("miki")

# check online payments for the approved,rejects,expired and faild transactions
def check_payment():
    initial=''
    while True:
        # =================================
        if ServicesTokenStorage.objects.filter(name__icontains="mtn").exists():
            token_obj=ServicesTokenStorage.objects.get(name__icontains="mtn")
            db_hours=token_obj.created_time.hour
            ctm=datetime.now().time().hour
            # check if token has expire if so create a new one and update the system
            if ctm-db_hours>0:
                token_obj.delete()
                print("miki")
        # ===============================
        # sleep(10)
        obj=OnlineFeesOnProgress.objects.filter(status=False)
        for pays in obj:
            ref_id=pays.ref_id
            token=pays.token
            resp=get_pay_status(ref_id,token)
            print(resp['status'])
            
            
            if resp['status']=="SUCCESSFUL":
                print(ref_id,resp['amount'],pays.student_id.admin)
                receipt_no= generate_ref_code()+str(timezone.now().date())
                try:
                    scif = SchoolInformation.objects.all()[0]
                except Exception as e:
                    HttpResponse(
                        "make sure school information has been set in the database correctly")
                # check if student is new or old
                if pays.entry == 'N':
                    total_fee = scif.new_student_fee
                    owing = total_fee-float(pays.amount)
                elif pays.entry == 'O':
                    total_fee = scif.old_student_fee
                    owing = total_fee-float(pays.amount)
                
                
                if owing<=0 or owing<=0.0:
                    due_fee = 0.0
                    fully_paid=True
                    partly_paid=False
                else:
                    due_fee = owing
                    fully_paid=False
                    partly_paid=True
                    
                # check if student is already in the database
                # print(Fee.objects.get(student_id=student)!=None)
                fee_object=Fee.objects.filter(student_id=pays.student_id).exists()
                
                # print(fee_object)
                # if fees doesn't exist we create new one
                if not fee_object :
                    if pays.amount >total_fee:
                        pays.amount=total_fee
                    # print(True)
                    
                
                    fee=Fee.objects.get_or_create(receipt_no=receipt_no,student_id=pays.student_id, class_room=pays.class_room, entry=pays.entry,
                                                semester=pays.semester, amount=pays.amount, due_fee=due_fee, total_fee=total_fee,fully_paid=fully_paid,partly_paid=partly_paid,amount_in_words=pays.amount_in_words)
                    
                            # print("created")
                    fee=Fee.objects.get(student_id=pays.student_id,receipt_no=receipt_no)
                    school_name=f"{scif.school_name_abbreviation} online Payment service"
                    file,name=receipt_generator(id=fee.receipt_no, st_name=fee.student_id.admin.username, semester=fee.semester, classroom=fee.class_room, amount=fee.amount, total_fee=fee.total_fee, amount_in_words=fee.amount_in_words, prepared_by=school_name,due=fee.due_fee,date=fee.date_paid)
                    
                    receipt=Receipt.objects.create(name=fee.student_id.admin.username,image=file,fee=fee)
                    
                # else we update the current one    
                else:
                    fee_object=Fee.objects.get(student_id=pays.student_id)
                    current_amount=(pays.amount
                                    +
                                    fee_object.amount)
                    if fee_object.amount>current_amount:
                        
                        owing=fee_object.total_fee-current_amount
                        # print(owing,current_amount)
                        if owing<=0 or owing<=0.0:
                            due_fee = 0.0
                            fully_paid=True
                            partly_paid=False
                        else:
                            due_fee = owing
                            fully_paid=False
                            partly_paid=True
                        
                    
                        current_amount_in_words=f'{fee_object.amount_in_words}+{pays.amount_in_words}'
                        fee_object.semester=pays.semester
                        fee_object.entry=pays.entry
                        fee_object.fully_paid=fully_paid
                        fee_object.partly_paid=partly_paid
                        fee_object.due_fee=due_fee
                        fee_object.class_room=pays.class_room
                        fee_object.amount_in_words=current_amount_in_words
                        
                        fee_object.amount=current_amount
                        
                        fee_object.save()
                        
                        fee=Fee.objects.get(student_id=pays.student_id,receipt_no=fee_object.receipt_no)
                        
                        school_name=f"{scif.school_name_abbreviation} online Payment service"
                        file,name=receipt_generator(id=fee.receipt_no, st_name=fee.student_id.admin.username, semester=fee.semester, classroom=fee.class_room, amount=fee.amount, total_fee=fee.total_fee, amount_in_words=fee.amount_in_words, prepared_by=school_name,due=fee.due_fee,date=fee.date_paid)
                        
                        receipt=Receipt.objects.create(name=fee.student_id.admin.username,image=file,fee=fee)
                        
                        
                    
                pays.status=True
                pays.save()
                # print("success")
            elif resp['status']=="FAILED":
                # print('expired')
                pays.delete()
            elif resp['status']=="REJECTED":
                # print('REJECTED')
                pays.delete()
            elif resp['status']=="TIMEOUT":
                # print('TIME OUT')
                pays.delete()
            elif resp['status']=="PENDING":
                print('PENDIN')
                
                if int(timezone.now().time().minute-pays.created_time.minute)>10:
                    # print("greater",timezone.now().time().minute-pays.created_time.minute)
                    pays.delete()
                else:
                    # print("not greater",timezone.now().time().minute-pays.created_time.minute)
                    pass
                
                
            if obj != initial:
                yield f'data: {obj}\n\n'
                initial=obj  
        sleep(6)
    
# check_payment()

class PostStreem(View):
    
    def get(self,request):
        response=StreamingHttpResponse(check_payment())
        response['content-type']='text/event-stream'
        return response



def showFeeForm(request):
    id_or_name=request.POST.get("ID")
    class_room=request.POST.get("class_room")
    
    if Fee.objects.filter(Q(student_id__admin__uid__iexact=id_or_name)|Q(student_id__admin__username__iexact=id_or_name),class_room=class_room).exists():
        try:
        
            # print(id_or_name)
            student_detail=Fee.objects.get(Q(student_id__admin__uid__iexact=id_or_name)|Q(student_id__admin__username__iexact=id_or_name),class_room=class_room)
            initial={
                'student_id':student_detail.student_id,
                'class_room':student_detail.class_room,
                'entry':student_detail.entry,
                'amount':student_detail.amount,
                'semester':student_detail.semester,
                'amount_in_words':student_detail.amount_in_words,
                
            }
            form=FeeForm(initial=initial)
            # print(student_detail,id_or_name,class_room)
            context={
                'form':form,
            }
            return render(request,'feeFormPatial.html',context)
        except Exception as e:
            return HttpResponse(f"<h2 class='text-danger bg-danger'>Please make sure the entered ID or Name is correct or check the class you selected because the one entered is incorrect : {e}</h2>")
    else:
        
        try:
        
            # print(id_or_name)
            student_detail=Student.objects.get(Q(admin__uid__iexact=id_or_name)|Q(admin__username__iexact=id_or_name),class_room=class_room)
            initial={
                'student_id':student_detail,
                'class_room':student_detail.class_room,
                'entry':student_detail.entry,
                'amount':'',
                'semester':'',
                'amount_in_words':'',
                
            }
            form=FeeForm(initial=initial)
            # print(student_detail,id_or_name,class_room)
            context={
                'form':form,
            }
            return render(request,'feeFormPatial.html',context)
            
        except Exception as e:
            return HttpResponse(f"<h2 class='text-danger bg-danger'>Please make sure the entered ID or Name is correct or check the class you selected because the one entered is incorrect : {e}</h2>")
    
   
    

def check_fee_remain(request):
    typest = request.POST.get('entry')
    scif = SchoolInformation.objects.all()[0]
    amount = float(request.POST.get('amount','0.0'))
    if typest=='N':
        stt="New"
        fee=scif.new_student_fee
        owing=fee-amount
    elif typest == 'O':
        stt="Old"
        fee=scif.old_student_fee
        owing = float(fee-amount)
        
        
    else:
        return HttpResponse("<span class='text-red badge badge-warning'>select a valid entry type eg New or Old</span>")
    if owing <= 0 or owing <= 0.0:
        owing = 0.0
    if amount >fee:
        amount=fee
    return HttpResponse(f"<span class='text-secondary bg-info'>{stt} Student total Fee : {fee}</span> <br> <span class='text-secondary bg-info'> If  {amount} is paid then student will be owing {owing} </span>")


def check_fee_student_type(request):
    
    typest = request.POST.get('entry')
    scif=SchoolInformation.objects.all()[0]
    if typest=='N':
        stt="New"
        fee=scif.new_student_fee
    elif typest == 'O':
        stt="Old"
        fee=scif.old_student_fee
    else:
        return HttpResponse("<span class='text-red badge badge-warning'>select a valid entry type eg New or Old</span>")
        
    return HttpResponse(f"<span class='text-secondary bg-info'>{stt} Student total Fee : {fee}</span>")

def check_user_payment(request):
    pass


def get_receipt(request,name=None):
    if name:
        student_id=name
    else:
        student_id=request.GET.get("name")
        
    print(student_id)
    receipts=Receipt.objects.filter(name__iexact=student_id)
    student_id_obj=Student.objects.get(admin__username__iexact=student_id)
    fee_object=Fee.objects.get(student_id=student_id_obj)
    school_info=SchoolInformation.objects.all()[0]
    if receipts.exists():
        
        context={'receipts':receipts,
                 'fee':fee_object,
                 "school_info":school_info,
        }
        print(school_info)
        return render(request,'receipt_images.html',context)
    

def activities_view(request):
    activities=Activity.objects.all()
    
    context={
        'activities':activities,
    }
    return render(request,"activities.html",context)



# def certificates(request):
    
#     context={
        
#     }
    
#     return render(request,"certificate/certificate.html",context)


class CertificatesView(View):
    
    def get(self,request):
        form=certificateFilterForm()
        context={'form':form,}
        
        return render(request,"certificate/certificate.html",context)
    
    
    def post(self,request):
        class_id=request.POST["class_id"]
        semester=request.POST["semester"]
       
        
        students=Student.objects.filter(class_room=class_id)
        school_info=SchoolInformation.objects.all()[0]
        classroom=ClassRoom.objects.get(pk=class_id)
        averages=StudentAverage.objects.filter(class_id=classroom,semester=semester)
        print(averages[1].subjects_grades.all())
        context={
            "schoolinfo":school_info,
            "averages":averages,
        
        }
    
        return render(request,"certificate/content.html",context)