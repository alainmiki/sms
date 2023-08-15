# Django REST Libs:
from rest_framework import serializers
from adminhod.models import CustomUser
from student.models import AttendanceReport, Subject
from guardian.models import Guardian
from schoolinfo.models import SchoolInformation
# Local Libs:
from student.models import ClassRoom, Department, Student, NotificationStudent, LeaveReportStudent

from adminhod.models import Event
from marks.models import Mark
from teacher.models import Staff
from fees.models import Fee

class CustomUserSerializer(serializers.ModelSerializer):
	"""
	CustomUser serializer
	Based on serializers.ModelSerializer
	"""
	class Meta:
         model = CustomUser
         exclude_fields=['password']
         fields = ['uid','first_name','username', 'last_name', 'email', 'address', 'gender',
            'place_of_birth', 'phone',  'profile_picture']

class ClassRoomSerializer(serializers.ModelSerializer):
	"""
	ClassRoom serializer
	Based on serializers.ModelSerializer
	"""
	class Meta:
		model = ClassRoom
		fields = ['name']

class DepartmentSerializer(serializers.ModelSerializer):
	"""
	Department serializer
	Based on serializers.ModelSerializer
	"""
	class Meta:
		model = Department
		fields = ['name']

class GuardianSerializer(serializers.ModelSerializer):
	"""
	Guardian serializer
	Based on serializers.ModelSerializer
	"""
	class Meta:
		model = Guardian
		fields = "__all__"
		depth=1
  
class EventSerializer(serializers.ModelSerializer):
	"""
	Event serializer
	Based on serializers.ModelSerializer
	"""
	class Meta:
		model = Event
		fields = "__all__"
		depth=1


  
class MarkSerializer(serializers.ModelSerializer):
    """
	Mark serializer
	Based on serializers.ModelSerializer
 """
    class Meta:
        model = Mark
        depth=1
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=['name']
    

class StudentSerializer(serializers.ModelSerializer):
    admin =CustomUserSerializer(many=False, read_only=False, required=True)
    class_room =ClassRoomSerializer(many=False, read_only=False, required=True)
    department =DepartmentSerializer(many=False, read_only=False, required=True)
    guardian =GuardianSerializer(many=False, read_only=False, required=True)
    
    class Meta:
        model = Student
        fields = "__all__"
        depth=1
    
          
class StaffSerializer(serializers.ModelSerializer):
    admin =CustomUserSerializer(many=False, read_only=False, required=True)
    # subjects =SubjectSerializer(many=False, read_only=False, required=True)
    class Meta:
        model = Staff
        fields = "__all__"
        depth=1

class MarkSerializer(serializers.ModelSerializer):
    """
	Mark serializer
	Based on serializers.ModelSerializer
 """
    student_id=StudentSerializer(many=False, read_only=False, required=True)
    staff_id=StaffSerializer(many=False, read_only=False, required=True)
    subject_id =SubjectSerializer(many=False, read_only=False, required=True)
    class Meta:
        model = Mark
        depth=2
        fields = "__all__"
        
class FeeSerializer(serializers.ModelSerializer):
    """
	Fee serializer
	Based on serializers.ModelSerializer
 """
    student_id=StudentSerializer(many=False, read_only=False, required=True)
    class_room=ClassRoomSerializer(many=False, read_only=False, required=True)
    class Meta:
        model = Fee
        depth=2
        fields = "__all__"
        


class AttendanceReportSerializer(serializers.ModelSerializer):
    student_id=StudentSerializer(many=False, read_only=False, required=True)
    # class_id=ClassRoomSerializer(many=False, read_only=False, required=True)
    staff_id=CustomUserSerializer(many=False, read_only=False, required=True)
    # staff_id=StaffSerializer(many=False, read_only=False, required=True)
    
    class Meta:
        model = AttendanceReport
        fields = "__all__"
        depth=1

class SchoolInformationSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = SchoolInformation
        exclude=[ "description", "history", "school_banner_image",]
        # fields = "__all__"
        depth=1
