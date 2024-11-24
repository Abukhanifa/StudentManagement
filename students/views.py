from rest_framework import viewsets, permissions
from .models import Student
from .serializers import StudentSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StudentPagination(PageNumberPagination):
    page_size = 5


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of students (for Teachers/Admin) or the authenticated student data",
        responses={200: StudentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new student record",
        request_body=StudentSerializer,
        responses={201: StudentSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing student record",
        request_body=StudentSerializer,
        responses={200: StudentSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a student record",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
