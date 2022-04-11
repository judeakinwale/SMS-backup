from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, permissions
from user import serializers, models, filters
from core import permissions as cpermissions
from core import utils

from django_rest_passwordreset.signals import reset_password_token_created
from drf_yasg.utils import no_body, swagger_auto_schema

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    serializer_action_classes = {
        'list': serializers.UserResponseSerializer,
        'retrieve': serializers.UserResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
    ]
    filterset_class = filters.UserFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            reciepients = [user.email, ]
            context = {
                "user": user,
                "school_name": "UNI",
                "login_url": "https://sms-lotus.herokuapp.com/api-auth/login/"
            }
            utils.send_account_creation_email(self.request, reciepients, context)
        except Exception as e:
            print(f"user creation email error: {e} \n")

        return user

    @swagger_auto_schema(
        operation_description="create a user and attached biodata",
        operation_summary='create user and attached biodata'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all users and attached biodata",
        operation_summary='list users and attached biodata'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a user and attached biodata",
        operation_summary='retrieve user and attached biodata'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a user and attached biodata",
        operation_summary='update user and update or create attached biodata'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a user and attached biodata",
        operation_summary='partial_update user and update or create attached biodata'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a user and attached biodata",
        operation_summary='delete user'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class ManageUserApiView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    queryset = get_user_model().objects.all()
    serializer_class = serializers.AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = filters.UserFilter

    def get_object(self):
        """retrieve and return the authenticated user"""
        return self.request.user
    
    @swagger_auto_schema(
        operation_description="retrieve authenticated user details",
        operation_summary='retrieve authenticated user details (account)'
    )
    def get(self, request, *args, **kwargs):
        """get method docstring"""
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update authenticated user details and update or create biodata",
        operation_summary='update authenticated user details (account) and update or create biodata'
    )
    def put(self, request, *args, **kwargs):
        """put method docstring"""
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial update authenticated user details and update or create biodata",
        operation_summary='partial update authenticated user details (account) and update or create biodata'
    )
    def patch(self, request, *args, **kwargs):
        """patch method docstring"""
        return super().patch(request, *args, **kwargs)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    serializer_action_classes = {
        'list': serializers.StaffResponseSerializer,
        'retrieve': serializers.StaffResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsStaff
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.StaffFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def perform_create(self, serializer):
        try:
            user = self.request.data.get("user")
            return super().perform_create(serializer)
        except Exception:
            serializer.save(user=self.request.user)
    
    @swagger_auto_schema(
        operation_description="create a staff and attached user",
        operation_summary='create staff and attached user'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all staff and attached user",
        operation_summary='list staff and attached user'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a staff and attached user",
        operation_summary='retrieve staff and attached user'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a staff and attached user",
        operation_summary='update staff and attached user'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a staff and attached user",
        operation_summary='partial_update staff and attached user'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a staff and attached user",
        operation_summary='delete staff'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class CourseAdviserViewSet(viewsets.ModelViewSet):
    queryset = models.CourseAdviser.objects.all()
    serializer_class = serializers.CourseAdviserSerializer
    serializer_action_classes = {
        'list': serializers.CourseAdviserResponseSerializer,
        'retrieve': serializers.CourseAdviserResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsHead
        | cpermissions.IsDean
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.CourseAdviserFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
    @swagger_auto_schema(
        operation_description="create a course adviser",
        operation_summary='create course adviser'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all course advisers",
        operation_summary='list all course advisers'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a course adviser",
        operation_summary='retrieve course adviser'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a course adviser",
        operation_summary='update course adviser'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a course adviser",
        operation_summary='partial_update course adviser'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a course adviser",
        operation_summary='delete course adviser'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    serializer_action_classes = {
        'list': serializers.StudentResponseSerializer,
        'retrieve': serializers.StudentResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsStudent
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.StudentFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def perform_create(self, serializer):
        try:
            user = self.request.data.get("user")
            return super().perform_create(serializer)
        except Exception:
            return serializer.save(user=self.request.user)
    
    @swagger_auto_schema(
        operation_description="create a student and attached user",
        operation_summary='create student and attached user'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all students and attached user",
        operation_summary='list all students and attached user'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a student and attached user",
        operation_summary='retrieve student and attached user'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a student and attached user",
        operation_summary='update student and attached user'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a student and attached user",
        operation_summary='partial_update student and attached user'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a student and attached user",
        operation_summary='delete student'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class BiodataViewSet(viewsets.ModelViewSet):
    queryset = models.Biodata.objects.all()
    serializer_class = serializers.BiodataSerializer
    serializer_action_classes = {
        'list': serializers.BiodataResponseSerializer,
        'retrieve': serializers.BiodataResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStaff
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.BiodataFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
    def perform_create(self, serializer):
        try:
            user = self.request.data.get("user")
            return super().perform_create(serializer)
        except Exception:
            serializer.save(user=self.request.user)
            
        
    @swagger_auto_schema(
        operation_description="create a biodata and attached academic data, health data and family data",
        operation_summary='create biodata and attached academic data, health data and family data'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all biodata and attached academic data, health data and family data",
        operation_summary='list all biodata and attached academic data, health data and family data'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a biodata and attached academic data, health data and family data",
        operation_summary='retrieve biodata and attached academic data, health data and family data'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a biodata and attached academic data, health data and family data",
        operation_summary='update biodata and attached academic data, health data and family data'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a biodata and attached academic data, health data and family data",
        operation_summary='partial_update biodata and attached academic data, health data and family data'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a biodata and attached academic data, health data and family data",
        operation_summary='delete biodata'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class ResultViewSet(viewsets.ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer
    serializer_action_classes = {
        'list': serializers.ResultResponseSerializer,
        'retrieve': serializers.ResultResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.ResultFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
    @swagger_auto_schema(
        operation_description="create a result for a course and attached student",
        operation_summary='create result for a course and attached student'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all results",
        operation_summary='list results'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a result for a course and attached student",
        operation_summary='retrieve result for a course and attached student'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a result for a course and attached student",
        operation_summary='update result for a course and attached student'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a result for a course and attached student",
        operation_summary='partial_update result for a course and attached student'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a result for a course and attached student",
        operation_summary='delete result'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class AcademicDataViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicData.objects.all()
    serializer_class = serializers.AcademicDataSerializer
    serializer_action_classes = {
        'list': serializers.AcademicDataResponseSerializer,
        'retrieve': serializers.AcademicDataResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsStaff
        | cpermissions.IsStudent
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.AcademicDataFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def perform_create(self, serializer):
        try:
            user = self.request.data.get("student")
            return super().perform_create(serializer)
        except Exception:
            serializer.save(student=self.request.user.student_set.all().first())
    
    @swagger_auto_schema(
        operation_description="create a academic_data",
        operation_summary='create academic_data'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all academic_data",
        operation_summary='list academic_data'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a academic_data",
        operation_summary='retrieve academic_data'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a academic_data",
        operation_summary='update academic_data'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a academic_data",
        operation_summary='partial_update academic_data'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a academic_data",
        operation_summary='delete academic_data'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class AcademicHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicHistory.objects.all()
    serializer_class = serializers.AcademicHistorySerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStaff
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.AcademicHistoryFilter
    
    def perform_create(self, serializer):
        try:
            biodata = self.request.data.get("biodata")
            return super().perform_create(serializer)
        except Exception:
            serializer.save(biodata=self.request.user.biodata)
    
    @swagger_auto_schema(
        operation_description="create a academic_history",
        operation_summary='create academic_history'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all academic_history",
        operation_summary='list academic_history'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a academic_history",
        operation_summary='retrieve academic_history'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a academic_history",
        operation_summary='update academic_history'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a academic_history",
        operation_summary='partial_update academic_history'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a academic_history",
        operation_summary='delete academic_history'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class HealthDataViewSet(viewsets.ModelViewSet):
    queryset = models.HealthData.objects.all()
    serializer_class = serializers.HealthDataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStaff
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.HealthDataFilter
    
    def perform_create(self, serializer):
        try:
            biodata = self.request.data.get("biodata")
            return super().perform_create(serializer)
        except Exception:
            serializer.save(biodata=self.request.user.biodata)
    
    @swagger_auto_schema(
        operation_description="create a health data",
        operation_summary='create health data'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all health data",
        operation_summary='list health data'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a health data",
        operation_summary='retrieve health data'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a health data",
        operation_summary='update health data'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a health data",
        operation_summary='partial_update health data'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a health data",
        operation_summary='delete health data'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class FamilyDataViewSet(viewsets.ModelViewSet):
    queryset = models.FamilyData.objects.all()
    serializer_class = serializers.FamilyDataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStaff
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.FamilyDataFilter
    
    def perform_create(self, serializer):
        try:
            biodata = self.request.data.get("biodata")
            return super().perform_create(serializer)
        except Exception:
            serializer.save(biodata=self.request.user.biodata)
    
    @swagger_auto_schema(
        operation_description="create a family data",
        operation_summary='create family data'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all family data",
        operation_summary='list family data'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a family data",
        operation_summary='retrieve family data'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a family data",
        operation_summary='update family data'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a family data",
        operation_summary='partial_update family data'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a family data",
        operation_summary='delete family data'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class CourseRegistrationViewSet(viewsets.ModelViewSet):
    queryset = models.CourseRegistration.objects.all()
    serializer_class = serializers.CourseRegistrationSerializer
    serializer_action_classes = {
        'list': serializers.CourseRegistrationSerializer,
        'retrieve': serializers.CourseRegistrationSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStudent
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.CourseRegistrationFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        try:
            student = self.request.data.get("student")
            return super().perform_create(serializer)
        except Exception:
            serializer.save(student=self.request.user.student_set.all().first())
    
    @swagger_auto_schema(
        operation_description="create a course registration",
        operation_summary='create course registration'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all course registrations",
        operation_summary='list course registration'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a course registration",
        operation_summary='retrieve course registration'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a course registration",
        operation_summary='update course registration'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a course registration",
        operation_summary='partial_update course registration'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a course registration",
        operation_summary='delete course registration'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # send an e-mail to the user
        print(reset_password_token.user)
        title="School Management Portal"
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.first_name,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}?token={}".format(
                instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
                reset_password_token.key)
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        # print("context set")
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            f"Password Reset for {title}",
            # message:
            email_plaintext_message,
            # from:   # "noreply@somehost.local"
            settings.EMAIL_HOST_USER,
            # to:
            [reset_password_token.user.email,],
        )
        print("message created")
        msg.attach_alternative(email_html_message, "text/html")
        print("html attached")
        msg.send()
        print("Forgot Password Mail successfully sent")
    except Exception as e:
        print(f"There was an error sending Forgot Password Mail: {e}")
