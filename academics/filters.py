from django_filters import rest_framework as filters
from academics import models


class FacultyFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Faculty
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            # 'description': ['icontains'],
            'is_active': ['exact'],
        }


class DepartmentFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Department
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            # 'description': ['icontains'],
            'is_active': ['exact'],
        }


class SpecializationFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Specialization
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            # 'description': ['icontains'],
            'is_active': ['exact'],
        }


class CourseFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Course
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            # 'description': ['icontains'],
            'is_active': ['exact'],
        }


class LevelFilter(filters.FilterSet):

    class Meta:
        model = models.Level
        fields = {'code': ['icontains']}


class RecommendedCoursesFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.RecommendedCourses
        fields = {
            'specialization__name': ['icontains'],
            'specialization__code': ['icontains'],
            'courses__name': ['icontains'],
            'courses__code': ['icontains'],
            'semester__semester': ['icontains'],
            'level__code': ['icontains'],
        }
