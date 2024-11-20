from .models import Student
from rest_framework import serializers
from courses.serializers import EnrollmentSerializer

class StudentSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True, source='enrollment_set')
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'date_of_birth', 'registration_date', 'enrollments']
        