from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from attendance.models import Attendance
from students.models import Student
from courses.models import Course
from rest_framework.test import APIClient
from django.urls import reverse

# Create test users and objects

class AttendanceTests(TestCase):
    def setUp(self):
        # Create a Teacher and a Student user
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher', password='testpassword', role='Teacher'
        )
        self.student_user = get_user_model().objects.create_user(
            username='student', password='testpassword', role='Student'
        )

        # Create a course
        self.course = Course.objects.create(name='Math 101', instructor=self.teacher_user)

        # Create a Student and assign a course
        self.student = Student.objects.create(user=self.student_user)
        self.student.course = self.course
        self.student.save()

        # Create an Attendance record for the student
        self.attendance = Attendance.objects.create(student=self.student, course=self.course, date='2024-11-01', status='Present')

        # Create API client and authenticate teacher
        self.client = APIClient()
        self.client.login(username='teacher', password='testpassword')

        # URL endpoints
        self.attendance_url = reverse('attendance-list')

    def test_create_attendance(self):
        """Test creating an attendance record"""
        data = {
            'student': self.student.id,
            'course': self.course.id,
            'date': '2024-11-02',
            'status': 'Absent'
        }
        response = self.client.post(self.attendance_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Attendance.objects.count(), 2)

    def test_create_attendance_for_student_without_permission(self):
        """Test creating an attendance record as a non-teacher user"""
        self.client.login(username='student', password='testpassword')
        data = {
            'student': self.student.id,
            'course': self.course.id,
            'date': '2024-11-02',
            'status': 'Absent'
        }
        response = self.client.post(self.attendance_url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_list_attendance(self):
        """Test listing all attendance records"""
        response = self.client.get(self.attendance_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Only one record should exist

    def test_retrieve_attendance(self):
        """Test retrieving a single attendance record"""
        url = reverse('attendance-detail', args=[self.attendance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'Present')

    def test_update_attendance(self):
        """Test updating an attendance record"""
        url = reverse('attendance-detail', args=[self.attendance.id])
        data = {
            'status': 'Late'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.status, 'Late')

    def test_update_attendance_without_permission(self):
        """Test updating an attendance record as a non-teacher user"""
        self.client.login(username='student', password='testpassword')
        url = reverse('attendance-detail', args=[self.attendance.id])
        data = {
            'status': 'Late'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_destroy_attendance(self):
        """Test deleting an attendance record"""
        url = reverse('attendance-detail', args=[self.attendance.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Attendance.objects.count(), 0)

    def test_destroy_attendance_without_permission(self):
        """Test deleting an attendance record as a non-teacher user"""
        self.client.login(username='student', password='testpassword')
        url = reverse('attendance-detail', args=[self.attendance.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)  # Forbidden
