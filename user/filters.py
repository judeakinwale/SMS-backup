from django_filters import rest_framework as filters
from user import models


class UserFilter(filters.FilterSet):
    # first_name = filters.CharFilter(lookup_expr='icontains')
    # middle_name = filters.CharFilter(lookup_expr='icontains')
    # last_name = filters.CharFilter(lookup_expr='icontains')
    # email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.User
        fields = {
            'first_name': ['icontains'],
            'middle_name': ['icontains'],
            'last_name': ['icontains'],
            'email': ['icontains'],
            'is_active': ['exact'],
            'is_staff': ['exact'],
        }


class StaffFilter(filters.FilterSet):

    class Meta:
        model = models.Staff
        fields = {
            'user__first_name': ['icontains'],
            'user__last_name': ['icontains'],
            'user__email': ['icontains'],
            'employee_id': ['icontains'],
            'programme__name': ['icontains'],
            'is_active': ['exact'],
            'is_lecturer': ['exact'],
            'is_bursar': ['exact'],
            'is_IT': ['exact'],
            'is_head_of_department': ['exact'],
            'is_dean_of_faculty': ['exact'],
            'is_course_adviser': ['exact'],
        }


class StudentFilter(filters.FilterSet):

    class Meta:
        model = models.Student
        fields = {
            'user__first_name': ['icontains'],
            'user__last_name': ['icontains'],
            'user__email': ['icontains'],
            'matric_no': ['icontains'],
            'student_id': ['icontains'],
            'is_active': ['exact'],
        }


class CourseAdviserFilter(filters.FilterSet):

    class Meta:
        model = models.CourseAdviser
        fields = {
            'staff__user__first_name': ['icontains'],
            'staff__user__last_name': ['icontains'],
            'staff__user__email': ['icontains'],
            'department__name': ['icontains'],
            'level__code': ['icontains'],
        }


class BiodataFilter(filters.FilterSet):

    class Meta:
        model = models.Biodata
        fields = {
            'user__first_name': ['icontains'],
            'user__last_name': ['icontains'],
            'user__email': ['icontains'],
            'birthday': ['icontains'],
            'nationality': ['icontains'],
            'state_of_origin': ['icontains'],
            'local_govt': ['icontains'],
        }


class AcademicDataFilter(filters.FilterSet):

    class Meta:
        model = models.AcademicData
        fields = {
            'student__user__first_name': ['icontains'],
            'student__user__last_name': ['icontains'],
            'student__user__email': ['icontains'],
            'student__matric_no': ['icontains'],
            'programme__name': ['icontains'],
            'start_date': ['exact', 'lt', 'gt'],
            'end_date': ['exact', 'lt', 'gt'],
            'qualification': ['icontains'],
        }


class CourseRegistrationFilter(filters.FilterSet):

    class Meta:
        model = models.CourseRegistration
        fields = {
            'course__name': ['icontains'],
            'student__user__first_name': ['icontains'],
            'student__user__last_name': ['icontains'],
            'student__user__email': ['icontains'],
            'student__matric_no': ['icontains'],
            'session': ['icontains'],
            'semester': ['icontains'],
            'is_active': ['exact'],
            'is_completed': ['exact'],
            'is_passed': ['exact'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class AcademicHistoryFilter(filters.FilterSet):

    class Meta:
        model = models.AcademicHistory
        fields = {
            'biodata__user__first_name': ['icontains'],
            'biodata__user__last_name': ['icontains'],
            'biodata__user__email': ['icontains'],
            'institution': ['icontains'],
        }


class HealthDataFilter(filters.FilterSet):

    class Meta:
        model = models.HealthData
        fields = {
            'biodata__user__first_name': ['icontains'],
            'biodata__user__last_name': ['icontains'],
            'biodata__user__email': ['icontains'],
            'diabetes': ['exact'],
            'disabilities': ['icontains'],
        }


class FamilyDataFilter(filters.FilterSet):

    class Meta:
        model = models.FamilyData
        fields = {
            'biodata__user__first_name': ['icontains'],
            'biodata__user__last_name': ['icontains'],
            'biodata__user__email': ['icontains'],
        }
