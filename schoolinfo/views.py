
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages

from django.views.generic import ListView

from schoolinfo.forms import ActivityForm, SchoolInformationForm
from .models import Activity, SchoolInformation

# Create your views here.

def home(request):
    try:
        schoolinfo=SchoolInformation.objects.all()
    except:
        schoolinfo=['0']
        
    context={
        'info':schoolinfo[0],
        'schoolinfo':schoolinfo,
        'activities':Activity.objects.all()
    }
    
    return render(request,"schoolinfo/home.html",context)


class CreateActivities(View):
    def get(self,request,id=None):
        if id==None:
            form=ActivityForm()
        else:
            activity=Activity.objects.get(id=id)
            form=ActivityForm(initial={'name':activity.name,"description":activity.description})
        context={
            "form":form,
                'activities':Activity.objects.all()
        }
        return render(request,"schoolinfo/activitiesForm.html",context)
    
    def post(self,request,id=None):
        if id==None:
            form=ActivityForm(request.POST)
        else:
            activity=Activity.objects.get(id=id)
            form=ActivityForm(request.POST,instance=activity)
        
        if form.is_valid():
            form.save()
            return redirect("school_info:create-activity")
        else:
            
            context={
                "form":form,
                'activities':Activity.objects.all()
                
            }
            return render(request,"schoolinfo/activitiesForm.html",context)

def delete_activity(request,id):
    Activity.objects.get(id=id).delete()
    return redirect("school_info:create-activity")


class SchoolInformationHome(ListView, LoginRequiredMixin):
    model = SchoolInformation
    context_object_name="schoolinfo"
    template_name="schoolinfo/home.html"
    
    def get_context_data(self, **kwargs):
        
        return super().get_context_data(**kwargs)


class CreateSchoolInformation(View):
    def post(self,request,id=None):
        if SchoolInformation.objects.filter(id=1).exists():
            instance=SchoolInformation.objects.all()[0]
            form=SchoolInformationForm(request.POST,request.FILES,instance=instance)
           
        else:
            form=SchoolInformationForm(request.POST,request.FILES)

        if form.is_valid():
             form.save()
             messages.info(request,f" The information was saved successfully")
             return redirect('school_info:setup')
        else:
            messages.info(request,f" The information was no saved due to : {form.errors}")
            context={
                'form':form,
            }
            return render(request,'schoolinfo/infoForm.html',context)
  
    def get(self,request,id=None):
        if SchoolInformation.objects.filter(id=1).exists():
            instance=SchoolInformation.objects.all()[0]
            
            initials={
                'school_name_abbreviation':instance.school_name_abbreviation,
                'school_name_full':instance.school_name_full,
                'address':instance.address,
                'email':instance.email,
                'phone':instance.phone,
                'fee_phone':instance.fee_phone,
                'whatsApp':instance.whatsApp,
                'website':instance.website,
                'new_student_fee':instance.new_student_fee,
                'old_student_fee':instance.old_student_fee,
                'school_logo':instance.school_logo,
                'school_stamp':instance.school_stamp,
                'h_o_s_signature':instance.h_o_s_signature,
                'school_banner_image':instance.school_banner_image,
                'motto':instance.motto,
                'description':instance.description,
                'history':instance.history,
                'region':instance.region,
                'town':instance.town,
                'po_box':instance.po_box,
            }
            form=SchoolInformationForm(initial=initials)
        else:
            form=SchoolInformationForm()
       
        context={
            'form':form,
            'infos':SchoolInformation.objects.all(),
        }
        return render(request,'schoolinfo/infoForm.html',context)
    
    
    
