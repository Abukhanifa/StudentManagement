from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from courses.views import CourseViewSet, EnrollmentViewSet
from students.views import StudentViewSet
from attendance.views import AttendanceViewSet
from users.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet)
router.register(r'student', StudentViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'assign', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/drf-auth/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]