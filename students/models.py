from datetime import date
from django.db import models
from users.models import CustomUser
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    email = models.EmailField(max_length=100, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(default=date.today)
    
    def __str__(self):
        return self.name
    