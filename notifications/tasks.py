from celery import shared_task
from django.core.mail import send_mail
from students.models import Student
from attendance.models import Attendance
from grades.models import Grade

@shared_task
def attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            'Attendance Reminder',
            'This is a reminder to mark your attendance for today.',
            'abuhanifathebest@gmail.com',
            [student.email],
            fail_silently=False,
        )
    return f"Attendance reminders sent to {students.count()} students."

@shared_task
def notify_grade_update(student_id, course_name, grade):
    student = Student.objects.get(pk=student_id)  
    send_mail(
        'Grade Update Notification',
        f'Your grade in {course_name} has been updated to {grade}.',
        'a_kuatuly@kbtu.kz',
        [student.email],
        fail_silently=False,
    )
    

@shared_task
def send_daily_report():
    # Generate attendance and grades report
    attendance_summary = Attendance.objects.values('course', 'student').count()
    grades_summary = Grade.objects.values('student', 'course', 'grade')

    # Compose email content
    email_body = f"""
    Daily Report:
    Attendance Summary: {attendance_summary} records.
    Grades Summary: {grades_summary} records.
    """
    send_mail(
        'Daily Attendance and Grades Report',
        email_body,
        'a_kuatuly@kbtu.kz',
        ['a_kuatuly@kbtu.kz'],  # Replace with recipient emails
        fail_silently=False,
    )
    
    
@shared_task
def weekly__emails():
    from students.models import Student
    from grades.models import Grade
    from courses.models import Course

    for student in Student.objects.all():
        grades = Grade.objects.filter(student=student)
        courses = Course.objects.filter(enrollment__student=student)

        # Compose the email
        email_body = f"""
        Hello {student.name},
        
        Here's your weekly performance summary:
        Courses: {', '.join(course.name for course in courses)}
        Grades: {', '.join(f"{grade.course}: {grade.grade}" for grade in grades)}
        """
        send_mail(
            'Weekly Performance Summary',
            email_body,
            'a_kuatuly@kbtu.kz',
            [student.email],
            fail_silently=False,
        )


