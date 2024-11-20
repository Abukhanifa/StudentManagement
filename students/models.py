from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    email = models.EmailField(max_length=100, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField()
    
    def __str__(self):
        return self.name
    