from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions
from user import serializers, models, filters
from core import permissions as cpermissions
from core import utils

from drf_yasg.utils import no_body, swagger_auto_schema

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
    ]
    filterset_class = filters.UserFilter

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            # print(f"user serializer: {user.email} \n\n")
            # print(f"user serializer data: {serializer.data} \n\n")
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

    @swagger_auto_schema(operation_description="create a user and an optional biodata",
                         operation_summary='create user and optional biodata')
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="list a user and an optional biodata",
                         operation_summary='list user and optional biodata')
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="retrieve a user and an optional biodata",
                         operation_summary='retrieve user and optional biodata')
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="update a user and an optional biodata",
                         operation_summary='update user and update or create optional biodata')
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="update a user and an optional biodata",
                         operation_summary='partial_update user and update or create optional biodata')
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="update a user and an optional biodata",
                         operation_summary='delete user')
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
    
    # @swagger_auto_schema(operation_description="create a user",
    #                      operation_summary='create user')
    # def create(self, request, *args, **kwargs):
    #     """create method docstring"""
    #     return super().create(request, *args, **kwargs)
    
    # @swagger_auto_schema(operation_description="list a user",
    #                      operation_summary='list user')
    # def list(self, request, *args, **kwargs):
    #     """list method docstring"""
    #     return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="retrieve authenticated user details",
                         operation_summary='retrieve authenticated user details (account)')
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="update authenticated user details and update or create biodata",
                         operation_summary='update authenticated user details (account) and update or create biodata')
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="partial update authenticated user details and update or create biodata",
                         operation_summary='partial update authenticated user details (account) and update or create biodata')
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(operation_description="update a user and an optional biodata",
    #                      operation_summary='delete user')
    # def destroy(self, request, *args, **kwargs):
    #     """destroy method docstring"""
    #     return super().destroy(request, *args, **kwargs)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsStaff
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.StaffFilter


class CourseAdviserViewSet(viewsets.ModelViewSet):
    queryset = models.CourseAdviser.objects.all()
    serializer_class = serializers.CourseAdviserSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.CourseAdviserFilter


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsStudent
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.StudentFilter


class BiodataViewSet(viewsets.ModelViewSet):
    queryset = models.Biodata.objects.all()
    serializer_class = serializers.BiodataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.BiodataFilter
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    


class ResultViewSet(viewsets.ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.ResultFilter


class AcademicDataViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicData.objects.all()
    serializer_class = serializers.AcademicDataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.AcademicDataFilter


class AcademicHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicHistory.objects.all()
    serializer_class = serializers.AcademicHistorySerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStudent
    ]
    filterset_class = filters.AcademicHistoryFilter


class HealthDataViewSet(viewsets.ModelViewSet):
    queryset = models.HealthData.objects.all()
    serializer_class = serializers.HealthDataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStudent
    ]
    filterset_class = filters.HealthDataFilter


class FamilyDataViewSet(viewsets.ModelViewSet):
    queryset = models.FamilyData.objects.all()
    serializer_class = serializers.FamilyDataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsBursar
        | cpermissions.IsITDept
        | cpermissions.IsStudent
    ]
    filterset_class = filters.FamilyDataFilter


class CourseRegistrationViewSet(viewsets.ModelViewSet):
    queryset = models.CourseRegistration.objects.all()
    serializer_class = serializers.CourseRegistrationSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStudent
        | cpermissions.IsITDept
    ]
    filterset_class = filters.CourseRegistrationFilter

    def perform_create(self, serializer):
        try:
            student = models.Student.objects.get(user=self.request.user)
            registration = serializer.save(student=student)
        except Exception:
            registration = serializer.save()
        return registration
