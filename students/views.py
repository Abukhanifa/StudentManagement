from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

class StudentPagination(PageNumberPagination):
    page_size = 5


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StudentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email']

    def get_queryset(self):
        user = self.request.user
        cache_key = f'students_list_{user.role}'
        students = cache.get(cache_key)
        if not students:
            if user.role == 'Student':
                students = self.queryset.filter(id=user.id)
            elif user.role in ['Teacher', 'Admin']:
                students = self.queryset.all()
            cache.set(cache_key, students, timeout=3600)  # Cache for 1 hour
        return students

    def perform_create(self, serializer):
        student = serializer.save()
        cache.delete(f'students_list_{student.role}')  # Invalidate cache for specific role

    def perform_update(self, serializer):
        student = serializer.save()
        cache.delete(f'students_list_{student.role}')  # Invalidate cache for specific role

    def perform_destroy(self, instance):
        cache.delete(f'students_list_{instance.role}')  # Invalidate cache for specific role
        super().perform_destroy(instance)


    
    