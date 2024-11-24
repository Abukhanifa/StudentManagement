from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status

from students.models import Student
from .models import Grade
from .serializers import GradeSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacherOrAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging
from rest_framework.response import Response


# Set up a logger
logger = logging.getLogger('grade_app')



class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    @swagger_auto_schema(
        operation_description="Retrieve a list of grades for all students or a specific student",
        responses={200: GradeSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new grade for a student",
        request_body=GradeSerializer,
        responses={201: GradeSerializer}
    )
    def create(self, request, *args, **kwargs):
        student_id = request.data.get('student')
        if student_id:  
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                return Response({"detail": "No Student matches the given query."}, status=status.HTTP_400_BAD_REQUEST)

            request.data._mutable = True
            request.data['student'] = student.id
            request.data._mutable = False  

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing grade for a student",
        request_body=GradeSerializer,
        responses={200: GradeSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a grade record",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
