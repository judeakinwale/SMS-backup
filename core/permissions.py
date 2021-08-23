from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Allows full access to owner / creator"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # # Read and write permissions are only allowed to the owner of the snippet.
        # return obj.owner == request.user
        if hasattr(object, 'source'):
            return bool(request.user and obj.source == request.user)
        
        if hasattr(object, 'supervisor'):
            return bool(request.user and obj.supervisor == request.user)

        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allows full access to owner / creator, readonly access to everyone"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(object, 'source'):
            return bool(request.user and obj.source == request.user)
        
        if hasattr(object, 'supervisor'):
            return bool(request.user and obj.supervisor == request.user)

        return False


class IsSuperUser(permissions.BasePermission):
    """Allows full access to superuser"""
            
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """Allows full access to superuser, readonly access to everyone"""
            
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_superuser)


class IsStaff(permissions.BasePermission):
    """Allows full access to staff"""
            
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsStaffOrReadOnly(permissions.BasePermission):
    """Allows full access to staff, readonly access to everyone"""
            
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsITDept(permissions.BasePermission):
    """Allows full access to IT"""

    def has_permission(self, request, view):
        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_IT)
        else:
            return False
        

class IsITDeptOrReadOnly(permissions.BasePermission):
    """Allows full access to IT, readonly access to everyone"""
            
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_IT)
        else:
            return False


class IsBursar(permissions.BasePermission):
    """Allows full access to bursar"""
            
    def has_permission(self, request, view):
        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_bursar)
        else:
            return False


class IsBursarOrReadOnly(permissions.BasePermission):
    """Allows full access to bursar, readonly access to everyone"""
            
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_bursar)
        else:
            return False


class IsLecturer(permissions.BasePermission):
    """Allows full access to lecturer"""
            
    def has_permission(self, request, view):
        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_lecturer)
        else:
            return False


class IsLecturerOrReadOnly(permissions.BasePermission):
    """Allows full access to lecturer, readonly access to everyone"""
            
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_lecturer)
        else:
            return False


class IsHead(permissions.BasePermission):
    """Allows full access to head of department"""
            
    def has_permission(self, request, view):
        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_head_of_department)
        else:
            return False


class IsHeadOrReadOnly(permissions.BasePermission):
    """Allows full access to head of department, readonly access to everyone"""
            
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_head_of_department)
        else:
            return False


class IsDean(permissions.BasePermission):
    """Allows full access to dean of faculty"""
            
    def has_permission(self, request, view):
        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_dean_of_faculty)
        else:
            return False


class IsDeanOrReadOnly(permissions.BasePermission):
    """Allows full access to dean of faculty, readonly access to everyone"""
            
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff and request.user.staff_set.all().exists():
            return bool(request.user and request.user.staff_set.all()[0].is_dean_of_faculty)
        else:
            return False


class IsStudent(permissions.BasePermission):
    """Allows full access to student"""
            
    def has_permission(self, request, view):
        if request.user.is_active and request.user.student_set.all().exists():
            return True
        else:
            return False


class IsStudentOrReadOnly(permissions.BasePermission):
    """Allows full access to student, readonly access to everyone"""
            
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_active and request.user.student_set.all().exists():
            return True
        else:
            return False
