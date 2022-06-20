from django_filters import rest_framework as filters
from academics import models


class FacultyFilter(filters.FilterSet):

    class Meta:
        model = models.Faculty
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            'description': ['icontains'],
            'is_active': ['exact'],
        }


class DepartmentFilter(filters.FilterSet):

    class Meta:
        model = models.Department
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            'description': ['icontains'],
            'is_active': ['exact'],
        }


class SpecializationFilter(filters.FilterSet):

    class Meta:
        model = models.Specialization
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            'description': ['icontains'],
            'is_active': ['exact'],
        }


class CourseFilter(filters.FilterSet):

    class Meta:
        model = models.Course
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
            'description': ['icontains'],
            # 'coordinator': ['icontains'],
            'coordinator__id': ['exact'],
            'is_active': ['exact'],
        }


class LevelFilter(filters.FilterSet):

    class Meta:
        model = models.Level
        fields = {'code': ['icontains']}


class RecommendedCoursesFilter(filters.FilterSet):

    class Meta:
        model = models.RecommendedCourses
        fields = {
            'specialization__name': ['icontains'],
            'specialization__code': ['exact', 'icontains'],
            'specialization__id': ['exact'],
            'course__name': ['icontains'],
            'course__code': ['exact', 'icontains'],
            'course__id': ['exact'],
            'semester__semester': ['icontains'],
            'level__code': ['exact', 'icontains', 'gte', 'lte'],
        }
