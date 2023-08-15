import json
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from apis import serializers
from apis.serializers import AttendanceReportSerializer, ClassRoomSerializer, CustomUserSerializer, DepartmentSerializer, EventSerializer, FeeSerializer, GuardianSerializer, MarkSerializer, SchoolInformationSerializer, StaffSerializer, StudentSerializer
from rest_framework.viewsets import ModelViewSet
from student.models import AttendanceReport
from guardian.models import Guardian
from marks.models import Mark
from schoolinfo.models import SchoolInformation

from student.models import ClassRoom, Department, Student
from teacher.models import Staff
from utils import generate_ref_code, send_email_func
from adminhod.models import Event
from fees.models import Fee

# Create your views here.
class StudentModelViewset(ModelViewSet):
    serializer_class=StudentSerializer
    queryset=Student.objects.all()
    
    def create(self, request, *args, **kwargs):
        serial=StudentSerializer(request.data)
        if serial.is_valid():
            print('valid',serial.data)
        return Response({"dd":f'outer not valid {serial.errors}'})

class StaffModelViewset(ModelViewSet):
    serializer_class=StaffSerializer
    queryset=Staff.objects.all()
    
    def create(self, request, *args, **kwargs):
        serial=StaffSerializer(request.data)
        if serial.is_valid():
            print('valid',serial.data)
        return Response({"dd":f'outer not valid {serial.errors}'})



class GuardianModelViewset(ModelViewSet):
    serializer_class=GuardianSerializer
   
    queryset=Guardian.objects.all()

class DepartmentModelViewset(ModelViewSet):
    serializer_class=DepartmentSerializer
    queryset=Department.objects.all()
    
class ClassRoomtModelViewset(ModelViewSet):
    serializer_class=ClassRoomSerializer
    queryset=ClassRoom.objects.all()

class MarksModelViewset(ModelViewSet):
    serializer_class=MarkSerializer
    queryset=Mark.objects.all()
    
class EventModelViewset(ModelViewSet):
    serializer_class=EventSerializer
    queryset=Event.objects.all()
class SchoolInformationModelViewset(ModelViewSet):
    serializer_class=SchoolInformationSerializer
    queryset=SchoolInformation.objects.all()

class FeeModelViewset(ModelViewSet):
    serializer_class=FeeSerializer
    queryset=Fee.objects.all()

class AttendanceReportModelViewset(ModelViewSet):
    serializer_class=AttendanceReportSerializer
    queryset=AttendanceReport.objects.all()


class StudentAPIView(APIView):
    
    def get(self,request,pk=None):
        if pk:
            print("get request with id:",pk)
            students=get_object_or_404(Student,pk=pk)
            data=StudentSerializer(students).data
        else:
            print("get request without id:")
            students=Student.objects.all()
            # print(students)
            data=StudentSerializer(students,many=True).data
        return Response(data)

    def post(self,request):
        # model=Student
        # students = Student.objects.all()
        data=json.loads(request.body)
        p=StudentSerializer(data=data)
        if p.is_valid():
            print(data.get('admin'),data.get('class_room'),data.get('deparment'),)
        else:
            
            print('error found',p.errors)
        print(data.get('admin'),data.get('class_room'),data.get('department'),data.get('guardian'),)
        return Response({"new":"data to post"})
    
    def put(self,request,pk=None):
        model=Student
        
        return Response({"new":"data to put"})

    def delete(self, request,pk=None):
        get_object_or_404(Student, pk=pk).delete()
        return Response({"new": "data to delete"})
