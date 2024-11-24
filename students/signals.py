from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Student

# Get the custom user model
CustomUser = get_user_model()

@receiver(post_save, sender=CustomUser)
def create_student_for_user(sender, instance, created, **kwargs):
    """
    When a CustomUser is created, create a corresponding Student instance with the default role 'Student'.
    """
    if created and instance.role == 'Student':
        # Create a Student instance for the newly created user if they are a student
        Student.objects.create(user=instance, name=instance.username)  # Assuming 'name' is required for Student
