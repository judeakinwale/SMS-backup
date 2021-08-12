from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only staff to edit an object"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff == True


class IsItDept(permissions.BasePermission):
    """Custom permission to allow only IT department staff to view and edit an object"""

    def has_object_permission(self, request, view, obj):
            
        if request.user.is_staff == True:
            return request.user.staff_set.all()[0].is_IT
        else:
            return False
        

class IsItDeptOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only IT department staff to edit an object"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if request.user.is_staff == True:
            return request.user.staff_set.all()[0].is_IT
        else:
            return False


class IsBursarOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only bursars to edit an object"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff == True:
            return request.user.staff_set.all()[0].is_bursar
        else:
            return False


class IsLecturerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only lecturers to edit an object"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if request.user.is_staff == True:
            return request.user.staff_set.all()[0].is_lecturer
        else:
            return False


class IsHeadOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only heads of department to edit an object"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if request.user.is_staff == True:
            return request.user.staff_set.all()[0].is_head_of_department
        else:
            return False


class IsDeanOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only deans of faculties to edit an object"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if request.user.is_staff == True:
            return request.user.staff_set.all()[0].is_dean_of_faculty
        else:
            return False


class IsStudentOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only deans of faculties to edit an object"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if request.user.student_set.all()[0].exists():
            return True
        else:
            return False

