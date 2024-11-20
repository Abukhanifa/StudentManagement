from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsAdmin, IsTeacher
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache


class CustomPagination(PageNumberPagination):
    page_size = 5  
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'instructor']

    def get_queryset(self):
        cache_key = 'courses_list'
        courses = cache.get(cache_key)
        if not courses:
            courses = self.queryset.all()
            cache.set(cache_key, courses, timeout=3600)  # Cache for 1 hour
        return courses

    def perform_create(self, serializer):
        course = serializer.save()
        cache.delete('courses_list')  # Invalidate cache when a new course is created

    def perform_update(self, serializer):
        course = serializer.save()
        cache.delete('courses_list')  # Invalidate cache when a course is updated

    def perform_destroy(self, instance):
        cache.delete('courses_list')  # Invalidate cache when a course is deleted
        super().perform_destroy(instance)
    
    
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
