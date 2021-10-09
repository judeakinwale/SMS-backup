from rest_framework import viewsets, permissions
from academics import models, serializers, filters
from core import permissions as cpermissions

# Create your views here.


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsITDeptOrReadOnly
        )
    ]
    filterset_class = filters.FacultyFilter


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsITDeptOrReadOnly
        )
    ]
    filterset_class = filters.DepartmentFilter


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsITDeptOrReadOnly
        )
    ]
    filterset_class = filters.SpecializationFilter


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsITDeptOrReadOnly
        )
    ]
    filterset_class = filters.CourseFilter


class LevelViewSet(viewsets.ModelViewSet):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsITDeptOrReadOnly
        )
    ]
    filterset_class = filters.LevelFilter


class RecommendedCoursesViewSet(viewsets.ModelViewSet):
    queryset = models.RecommendedCourses.objects.all()
    serializer_class = serializers.RecommendedCoursesSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsITDeptOrReadOnly
        )
    ]
    filterset_class = filters.RecommendedCoursesFilter
