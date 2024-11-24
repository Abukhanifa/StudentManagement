from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from courses.views import CourseViewSet, EnrollmentViewSet
from students.views import StudentViewSet
from attendance.views import AttendanceViewSet
from users.views import UserViewSet
from grades.views import GradeViewSet
from analytics.views import active_users_report, popular_courses_report

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'student', StudentViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'users', UserViewSet)
router.register(r'grades', GradeViewSet)

# Set up schema view for Swagger UI and OpenAPI schema
schema_view = get_schema_view(
   openapi.Info(
      title="School Management API",
      default_version='v1',
      description="API documentation for the School Management system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="support@school.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/drf-auth/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('openapi/', schema_view.without_ui(cache_timeout=0), name='openapi-schema'),
    path('docs/', include_docs_urls(title='School Management API Documentation')),
    path('active-users/', active_users_report, name='active_users_report'),
    path('popular-courses/', popular_courses_report, name='popular_courses_report'),
    
]
