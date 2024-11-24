from django.shortcuts import render
from .models import ApiRequest, ActiveUser, PopularCourse

def active_users_report(request):
    active_users = ActiveUser.objects.all().order_by('-last_active')
    return render(request, 'active_user.html', {'active_users': active_users})

def popular_courses_report(request):
    popular_courses = PopularCourse.objects.all().order_by('-views')
    return render(request, 'popular_course.html', {'popular_courses': popular_courses})
