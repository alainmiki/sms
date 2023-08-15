import datetime
import os
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


from schoolinfo.models import SchoolInformation
from student.models import Student
from .models import Receipt, Fee
from fees.forms import FeeForm, FilterForm
from utils import generate_ref_code, receipt_generator
from django.contrib import messages
from schoolinfo.models import SchoolInformation


class FeesView(View):
    def post(self,request):
        if request.user.user_type=='1':
            try:
                scif = SchoolInformation.objects.all()[0]
            except Exception as e:
                HttpResponse(
                    "make sure school information has been set in the database correctly")
            form=FeeForm(request.POST)
            if form.is_valid():
                student_id=form.cleaned_data['student_id']
                class_room=form.cleaned_data['class_room']
                entry=form.cleaned_data['entry']
                semester=form.cleaned_data['semester']
                amount=form.cleaned_data['amount']
                amount_in_words=form.cleaned_data['amount_in_words']
                receipt_no= generate_ref_code()+str(timezone.now().date())
                
                student=Student.objects.get(
                    admin__username=student_id)
                
                # check if student class_room is == entered class_room
                if student.class_room == class_room:
                    
                    # check if student is new or old
                    if entry == 'N':
                        total_fee = scif.new_student_fee
                        owing = total_fee-amount
                    elif entry == 'O':
                        total_fee = scif.old_student_fee
                        owing = total_fee-amount
                    
                    
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
                    fee_object=Fee.objects.filter(student_id=student).exists()
                    
                    # print(fee_object)
                    if not fee_object :
                        if amount >total_fee:
                            amount=total_fee
                        # print(True)
                        fee=Fee.objects.get_or_create(receipt_no=receipt_no,student_id=student_id, class_room=class_room, entry=entry,
                                            semester=semester, amount=amount, due_fee=due_fee, total_fee=total_fee,fully_paid=fully_paid,partly_paid=partly_paid,amount_in_words=amount_in_words)
                        # print("created")
                        fee=Fee.objects.get(student_id=student_id,receipt_no=receipt_no)

                        file=receipt_generator(id=fee.receipt_no, st_name=fee.student_id.admin.username, semester=fee.semester, classroom=fee.class_room, amount=fee.amount, total_fee=fee.total_fee, amount_in_words=fee.amount_in_words, prepared_by=request.user.username,due=fee.due_fee,date=fee.date_paid)
                        
                        receipt=Receipt.objects.create(name=fee.student_id.admin.username,image=file,fee=fee)
                    else:
                        fee_object=Fee.objects.get(student_id=student)
                        return HttpResponse(f"<h3 class='text-light bg-warning card'>The student is already in the fee database so update the student fee information instead of trying to register it as new fee registration <a href='fees-get_updateForm-register/{fee_object.receipt_no}' class='nav-link bg-secondary text-info'>Click here to update </a></h3>")
                        
                else:
                    return HttpResponse("<h3 class='card text-light bg-warning '>Sorry the Student Name and Class did not match. The student is not in the class you entered </h3>")
                fesses=Fee.objects.all().order_by('-date_paid')
                context={
                    'form':form,
                    'fesses': fesses,
                    'file':receipt.image,
                    'feeHeads': Fee.objects.filter(student_id=student_id)
                }
                # print(file)
                # send_email_func(recipient_list=[email,],from_email="smsprogram@gmail.com",body=f"Hay Dear {first_name} {last_name} here is your password:'{passwd}'. Use it to login into your account with the combination of your Email:'{email}'",subject="Your School website Account Password",)
        
                return render(request,'fees/feeTable.html',context)
                
            return HttpResponse(f"{form.errors} the was an error")
        return HttpResponse("This is a warning from the head office \n This section is restricted so be warn")
    def get(self,request):
        if request.user.user_type=='1':
            form=FeeForm()
          
            fesses=Fee.objects.all().order_by('-date_paid')
            context={
                'form':form,
                'fesses':fesses
            }
            
            # print(fesses)
            return render(request,'fees/feesForm.html',context)
        else:
            return HttpResponse("This is a warning from the head office \n This section is restricted so be warn")



def manage_fees(request):
    if request.user.user_type == '1':

        fesses = Fee.objects.all().order_by('-date_paid')
       
        context = {
            'fesses':fesses,
            # 'partly_paid_fee':partly_paid_fee,
            'form': FilterForm(initial={'class_room':('0','all')})
            
        }

        # print(fesses)
        return render(request, 'fees/manage_fees.html', context)
    else:
        return HttpResponse("This is a warning from the head office \n This section is restricted so be warn")



class UpdateFee(View):
    
    def post(self,request,id):
        if request.user.user_type == '1':
            try:
                scif = SchoolInformation.objects.all()[0]
            except Exception as e:
                HttpResponse(
                    "make sure school information has been set in the database correctly")
            form = FeeForm(request.POST)
            if form.is_valid():
                student_id = form.cleaned_data['student_id']
                class_room = form.cleaned_data['class_room']
                entry = form.cleaned_data['entry']
                semester = form.cleaned_data['semester']
                amount = form.cleaned_data['amount']
                amount_in_words = form.cleaned_data['amount_in_words']
                # receipt_no = generate_ref_code()+str(timezone.now().date())

                student = Student.objects.get(
                    admin__username=student_id)

                # check if student class_room is == entered class_room
                if student.class_room == class_room:

                    # check if student is new or old
                    if entry == 'N':
                        total_fee = scif.new_student_fee
                        owing = total_fee-amount
                    elif entry == 'O':
                        total_fee = scif.old_student_fee
                        owing = total_fee-amount

                    if owing <= 0 or owing <= 0.0:
                        due_fee = 0.0
                        fully_paid = True
                        partly_paid = False
                    else:
                        due_fee = owing
                        fully_paid = False
                        partly_paid = True

                    # check if student is already in the database
                    # print(Fee.objects.get(student_id=student)!=None)
                    fee_object = Fee.objects.filter(
                        student_id=student).exists()
                    # print(fee_object)
                    if fee_object:
                        if amount > total_fee:
                            amount = total_fee
                        fee_to_update = Fee.objects.get(receipt_no=id)
                        # print(fee_to_update)
                        fee_to_update.amount = amount
                        fee_to_update.amount_in_words = amount_in_words
                        fee_to_update.due_fee = due_fee
                        fee_to_update.entry=entry
                        fee_to_update.semester = semester
                        fee_to_update.partly_paid=partly_paid
                        fee_to_update.fully_paid=fully_paid
                        fee_to_update.total_fee=total_fee
                        fee_to_update.student_id=student_id
                        fee_to_update.class_room = class_room
                        fee_to_update.save()
                        
                        fee=fee_to_update

                        file=receipt_generator(id=fee.receipt_no, st_name=fee.student_id.admin.username, semester=fee.semester, classroom=fee.class_room, amount=fee.amount, total_fee=fee.total_fee, amount_in_words=fee.amount_in_words, prepared_by=request.user.username,due=fee.due_fee,date=fee.date_paid)
                        
                        Receipt.objects.update(name=fee.student_id.admin.username,image=file,fee=fee)

                        receipt=Receipt.objects.get(name=fee.student_id.admin.username,fee=fee)
                       
                    else:
                        return HttpResponse("<h3 class='text-light bg-warning card'>The student is not in the fee database so register the student fee information instead of trying to update it as new fee registration <a href='fees-register' class='nav-link bg-secondary text-info'>Click here to register </a> </h3>")

                else:
                    return HttpResponse("<h3 class='card text-light bg-warning '>Sorry the Student Name and Class did not match. The student is not in the class you entered </h3>")
                fesses = Fee.objects.all().order_by('-date_paid')
                context = {
                    'form': form,
                    'file': receipt.image,
                    'fesses': fesses,
                    # 'feeHeads': Fee.objects.filter(student_id=student_id)
                }
                # print(fesses)
                return render(request, 'fees/feeTable.html', context)

            return HttpResponse(f"{form.errors} the was an error")
        return HttpResponse("This is a warning from the head office \n This section is restricted so be warn")


@csrf_exempt
def get_updateForm(request,id):
        if request.user.user_type == '1':

            fesses = Fee.objects.all().order_by('-date_paid')
            current_fee_to_update=fesses.get(receipt_no=id)
            initial_data={
                'student_id':current_fee_to_update.student_id,
                'class_room':current_fee_to_update.class_room,
                'entry':current_fee_to_update.entry,
                'semester':current_fee_to_update.semester,
                'amount':current_fee_to_update.amount,
                'amount_in_words':current_fee_to_update.amount_in_words,
            }
            form = FeeForm(initial_data)
            context = {
                'form': form,
                'fesses': fesses,
                'receipt_no':id,
            }

            # print(fesses)
            return render(request, 'fees/feeUpdate.html', context)
        else:
            return HttpResponse("This is a warning from the head office \n This section is restricted so be warn")
        
def get_updateFormbase(request,id):
        if request.user.user_type == '1':

            fesses = Fee.objects.all().order_by('-date_paid')
            current_fee_to_update=fesses.get(receipt_no=id)
            initial_data={
                'student_id':current_fee_to_update.student_id,
                'class_room':current_fee_to_update.class_room,
                'entry':current_fee_to_update.entry,
                'semester':current_fee_to_update.semester,
                'amount':current_fee_to_update.amount,
                'amount_in_words':current_fee_to_update.amount_in_words,
            }
            form = FeeForm(initial_data)
            context = {
                'form': form,
                'fesses': fesses,
                'receipt_no':id,
            }

            # print(fesses)
            return render(request, 'fees/feeUpdatebase.html', context)
        else:
            return HttpResponse("This is a warning from the head office \n This section is restricted so be warn")




        

        
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


def clear(request):
    
    return HttpResponse('')


def fee_filter(request):
    
    form = FilterForm(request.POST)
   
    if form.is_valid():
        filter_by=form.cleaned_data['filter_by']
        class_room=form.cleaned_data['class_room']
        get_by=form.cleaned_data['get_by']
        print(get_by)
        # return 0
        
        if filter_by == 'all' and class_room != 'all':
            search_query = Fee.objects.filter(class_room__name=class_room)

        elif filter_by == 'all' and class_room == 'all':
            search_query = Fee.objects.all()
            
        elif class_room != 'all' and filter_by != 'all':
            search_query = Fee.objects.filter(
                class_room__name=class_room).order_by('-'+str(filter_by))
        else:
            search_query = Fee.objects.all().order_by('-'+str(filter_by))
                
                
                
        # check gey by data category
        if get_by=='partly_paid':
            search_query1=[ ]
            for i in search_query:
                print(i)
                if i.partly_paid == True:
                    search_query1.append(i)
            search_query=search_query1
        
        elif get_by=='fully_paid':
            search_query1 = []
            for i in search_query:
                print(i)
                if i.fully_paid == True:
                    search_query1.append(i)
            
            search_query = search_query1
       
        fesses = search_query
        if fesses==[]:
            # messages.error(request,"There is no data in the filtered category")
            return HttpResponse("There is no data in the filtered category")
        
        context = {
            'fesses': fesses,
            
            'form': form,

        }
        print(fesses)
        return render(request,'fees/feeTable.html',context)
        # return HttpResponse(f'working well {filter_by} ,{class_room} ')
    
    return HttpResponse(f'Warning error: {form.errors}')
