from django.core.management.base import BaseCommand
from celery.result import AsyncResult

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class Command(BaseCommand):
    help = 'Set up periodic tasks for Celery Beat'

    def handle(self, *args, **kwargs):
        # Set up the daily task for attendance reminder at 7:00 AM
        daily_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=0, hour=7  # Daily at 7:00 AM
        )
        PeriodicTask.objects.get_or_create(
            crontab=daily_schedule,
            name='Send Daily Attendance Reminder',
            task='notifications.tasks.attendance_reminder',  # Modify task name as needed
            enabled=True,  # Ensure task is enabled
        )

        # Set up the weekly task for performance summary on Monday at 8:00 AM
        weekly_schedule, _ = CrontabSchedule.objects.get_or_create(
            day_of_week='mon',  # Monday
            hour=8,             # 8:00 AM
            minute=0
        )
        PeriodicTask.objects.get_or_create(
            crontab=weekly_schedule,
            name='Send Weekly Performance Summary',
            task='notifications.tasks.send_weekly_performance_summary',  # Modify task name as needed
            enabled=True,  # Ensure task is enabled
        )

        # Output success message to the terminal
        self.stdout.write(self.style.SUCCESS('Successfully set up periodic tasks for Celery Beat'))
