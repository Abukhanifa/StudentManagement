from django.shortcuts import render
from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging

logger = logging.getLogger('attendance')  # Use your custom logger

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def perform_create(self, serializer):
        attendance = serializer.save()
        logger.info(f"Attendance marked for student {attendance.student.name} in course {attendance.course.name} by {self.request.user.username}")

    def perform_update(self, serializer):
        attendance = serializer.save()
        logger.info(f"Attendance updated for student {attendance.student.name} in course {attendance.course.name} by {self.request.user.username}")

    def perform_destroy(self, instance):
        logger.info(f"Attendance record deleted for student {instance.student.name} in course {instance.course.name}")
        super().perform_destroy(instance)

    

