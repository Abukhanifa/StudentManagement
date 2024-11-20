from django.db import models
from django.conf import settings
from students.models import Student

class Course(models.Model):
    name = models.TextField()
    description = models.TextField(max_length=500)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='courses_instructed'
    )
    
    def __str__(self):
        return self.name
    
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.name}"
    

