from rest_framework import viewsets, permissions
from academics import models, serializers, filters
from core import permissions as cpermissions

# Create your views here.


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.FacultyFilter


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.DepartmentFilter


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.SpecializationFilter


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.CourseFilter


class LevelViewSet(viewsets.ModelViewSet):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.LevelFilter


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]


class SessionViewSet(viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]


class RecommendedCoursesViewSet(viewsets.ModelViewSet):
    queryset = models.RecommendedCourses.objects.all()
    serializer_class = serializers.RecommendedCoursesSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.RecommendedCoursesFilter
