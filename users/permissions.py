from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Student'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Teacher'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Admin'
    
class IsTeacherOrAdmin(BasePermission):
    """
    Custom permission to allow access for either Teacher or Admin.
    """
    def has_permission(self, request, view):
        return request.user.role in ['Teacher', 'Admin']
