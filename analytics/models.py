from django.db import models
from users.models import CustomUser
from courses.models import Course

class ApiRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class ActiveUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_active = models.DateTimeField(auto_now=True)

class PopularCourse(models.Model):
    course = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
