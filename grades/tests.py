from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from courses.models import Course
from users.models import CustomUser
from grades.models import Grade  
from datetime import date

class GradeManagementTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test users (students and teachers)
        self.teacher = CustomUser.objects.create_user(username='teacheruser', password='testpassword', role='teacher')
        self.student = CustomUser.objects.create_user(username='studentuser', password='testpassword', role='student')
        
        # Create a course for testing
        self.course = Course.objects.create(name='Test Course', instructor=self.teacher)

    def test_assign_grade_to_student(self):
        # Assign a grade to the student
        self.client.login(username='teacheruser', password='testpassword')
        response = self.client.post('/api/grades/', {
            'student': self.student.id,
            'course': self.course.id,
            'date': str(date.today()),  # Pass the current date
            'teacher': self.teacher.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        grade = Grade.objects.get(student=self.student, course=self.course)
        self.assertEqual(grade.teacher, self.teacher)
        self.assertEqual(grade.date, date.today())

    def test_view_grade_as_student(self):
        # First assign a grade
        grade = Grade.objects.create(student=self.student, course=self.course, teacher=self.teacher, date=date.today())

        # Test student accessing their grade
        self.client.login(username='studentuser', password='testpassword')
        response = self.client.get(f'/api/grades/{grade.id}/')  # Use the grade id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date'], str(date.today()))
