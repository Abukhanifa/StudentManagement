from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacherOrAdmin 
from students.models import Student# Import custom permission
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger(__name__)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of attendance records",
        responses={200: AttendanceSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new attendance record",
        request_body=AttendanceSerializer,
        responses={201: AttendanceSerializer}
    )
    def create(self, request, *args, **kwargs):
        student_id = request.data.get('student')
        if student_id:
            student = get_object_or_404(Student, id=student_id)
            data = request.data.copy()
            data['student'] = student.id
            request._full_data = data  # Pass the correct data
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing attendance record",
        request_body=AttendanceSerializer,
        responses={200: AttendanceSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an attendance record",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
