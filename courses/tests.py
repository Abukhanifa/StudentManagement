from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from courses.models import Course
from users.models import CustomUser

class CourseViewSetTest(TestCase):
    def setUp(self):
        # Create test users with roles
        self.teacher = CustomUser.objects.create_user(username='teacheruser', password='testpassword')
        self.teacher.role = 'teacher'
        self.teacher.save()

        self.admin = CustomUser.objects.create_superuser(username='adminuser', password='testpassword')

        self.client = APIClient()

    def test_create_course_as_teacher(self):
        self.client.login(username='teacheruser', password='testpassword')
        response = self.client.post('/api/courses/', {
            'name': 'Test Course',
            'instructor': self.teacher.id,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Teachers should not be able to create

    def test_create_course_as_admin(self):
        self.client.login(username='adminuser', password='testpassword')
        response = self.client.post('/api/courses/', {
            'name': 'Test Course',
            'instructor': self.teacher.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Admin should be able to create courses
