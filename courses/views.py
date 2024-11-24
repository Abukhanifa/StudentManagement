from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsAdmin, IsTeacher, IsTeacherOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger('app_logger')

class CustomPagination(PageNumberPagination):
    page_size = 5  
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of courses",
        responses={200: CourseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a course record",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of enrollments for the authenticated user (Student/Teacher/Admin)",
        responses={200: EnrollmentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new enrollment record",
        request_body=EnrollmentSerializer,
        responses={201: EnrollmentSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing enrollment record",
        request_body=EnrollmentSerializer,
        responses={200: EnrollmentSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an enrollment record",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


