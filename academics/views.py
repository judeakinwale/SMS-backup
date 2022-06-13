from rest_framework import viewsets, permissions
from rest_framework import status, views, response
from academics import models, serializers, filters
from core import permissions as cpermissions
from core import mixins
from drf_yasg.utils import no_body, swagger_auto_schema

# Create your views here.


class FacultyViewSet(mixins.swagger_documentation_factory("faculty", "a", "faculty"), viewsets.ModelViewSet):
    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.FacultyFilter


class DepartmentViewSet(mixins.swagger_documentation_factory("department"), viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    serializer_action_classes = {
        'list': serializers.DepartmentResponseSerializer,
        'retrieve': serializers.DepartmentResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.DepartmentFilter
        
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class SpecializationViewSet(mixins.swagger_documentation_factory("specialization"), viewsets.ModelViewSet):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    serializer_action_classes = {
        'list': serializers.SpecializationResponseSerializer,
        'retrieve': serializers.SpecializationResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.SpecializationFilter
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class CourseViewSet(mixins.swagger_documentation_factory("course"), viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    serializer_action_classes = {
        'list': serializers.CourseResponseSerializer,
        'retrieve': serializers.CourseResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.CourseFilter
        
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class LevelViewSet(mixins.swagger_documentation_factory("level"), viewsets.ModelViewSet):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.LevelFilter


class SemesterViewSet(mixins.swagger_documentation_factory("semester"), viewsets.ModelViewSet):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]


class SessionViewSet(mixins.swagger_documentation_factory("session"), viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]


class RecommendedCoursesViewSet(mixins.swagger_documentation_factory("recommended course"), viewsets.ModelViewSet):
    queryset = models.RecommendedCourses.objects.all()
    serializer_class = serializers.RecommendedCoursesSerializer
    serializer_action_classes = {
        'list': serializers.RecommendedCoursesResponseSerializer,
        'retrieve': serializers.RecommendedCoursesResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.RecommendedCoursesFilter
        
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
