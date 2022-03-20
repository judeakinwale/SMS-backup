from rest_framework import viewsets, permissions
from academics import models, serializers, filters
from core import permissions as cpermissions

from drf_yasg.utils import no_body, swagger_auto_schema

# Create your views here.


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.FacultyFilter
    
    @swagger_auto_schema(
        operation_description="create a faculty",
        operation_summary='create faculty'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all faculty",
        operation_summary='list faculty'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a faculty",
        operation_summary='retrieve faculty'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a faculty",
        operation_summary='update faculty'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a faculty",
        operation_summary='partial_update faculty'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a faculty",
        operation_summary='delete faculty'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class DepartmentViewSet(viewsets.ModelViewSet):
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
    
    @swagger_auto_schema(
        operation_description="create a department",
        operation_summary='create department'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all departments",
        operation_summary='list departments'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a department",
        operation_summary='retrieve department'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a department",
        operation_summary='update department'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a department",
        operation_summary='partial_update department'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a department",
        operation_summary='delete department'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class SpecializationViewSet(viewsets.ModelViewSet):
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
    
    @swagger_auto_schema(
        operation_description="create a specialization",
        operation_summary='create specialization'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all specializations",
        operation_summary='list specializations'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a specialization",
        operation_summary='retrieve specialization'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a specialization",
        operation_summary='update specialization'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a specialization",
        operation_summary='partial_update specialization'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a specialization",
        operation_summary='delete specialization'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class CourseViewSet(viewsets.ModelViewSet):
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
    
    @swagger_auto_schema(
        operation_description="create a course",
        operation_summary='create course'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all courses",
        operation_summary='list courses'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a course",
        operation_summary='retrieve course'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a course",
        operation_summary='update course'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a course",
        operation_summary='partial_update course'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a course",
        operation_summary='delete course'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class LevelViewSet(viewsets.ModelViewSet):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.LevelFilter
    
    @swagger_auto_schema(
        operation_description="create a level",
        operation_summary='create level'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all levels",
        operation_summary='list levels'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a level",
        operation_summary='retrieve level'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a level",
        operation_summary='update level'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a level",
        operation_summary='partial_update level'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a level",
        operation_summary='delete level'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    
    @swagger_auto_schema(
        operation_description="create a semester",
        operation_summary='create semester'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all semesters",
        operation_summary='list semesters'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a semester",
        operation_summary='retrieve semester'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a semester",
        operation_summary='update semester'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a semester",
        operation_summary='partial_update semester'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a semester",
        operation_summary='delete semester'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    
    @swagger_auto_schema(
        operation_description="create a session",
        operation_summary='create session'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all sessions",
        operation_summary='list sessions'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a session",
        operation_summary='retrieve session'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a session",
        operation_summary='update session'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a session",
        operation_summary='partial_update session'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a session",
        operation_summary='delete session'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class RecommendedCoursesViewSet(viewsets.ModelViewSet):
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
    
    @swagger_auto_schema(
        operation_description="create a recommended course",
        operation_summary='create recommended course'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all recommended courses",
        operation_summary='list recommended courses'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a recommended course",
        operation_summary='retrieve recommended course'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a recommended course",
        operation_summary='update recommended course'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a recommended course",
        operation_summary='partial_update recommended course'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a recommended course",
        operation_summary='delete recommended course'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)
