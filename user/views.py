from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions
from user import serializers, models
from core import permissions as cpermissions

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDept
        )
    ]


class ManageUserApiView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrieve and return the authenticated user"""
        return self.request.user


class StaffViewSet(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDeptOrReadOnly
        )
    ]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDeptOrReadOnly
        )
    ]


class BiodataViewSet(viewsets.ModelViewSet):
    queryset = models.Biodata.objects.all()
    serializer_class = serializers.BiodataSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDept
            | cpermissions.IsStudent
        )
    ]


class AcademicDataViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicData.objects.all()
    serializer_class = serializers.AcademicDataSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDept
        )
    ]


class AcademicHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicHistory.objects.all()
    serializer_class = serializers.AcademicHistorySerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDept
            | cpermissions.IsStudent
        )
    ]


class HealthDataViewSet(viewsets.ModelViewSet):
    queryset = models.HealthData.objects.all()
    serializer_class = serializers.HealthDataSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDept
            | cpermissions.IsStudent
        )
    ]


class FamilyDataViewSet(viewsets.ModelViewSet):
    queryset = models.FamilyData.objects.all()
    serializer_class = serializers.FamilyDataSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsBursar
            | cpermissions.IsITDept
            | cpermissions.IsStudent
        )
    ]


class CourseRegistrationViewSet(viewsets.ModelViewSet):
    queryset = models.CourseRegistration.objects.all()
    serializer_class = serializers.CourseRegistrationSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser
            | cpermissions.IsStudent
            | cpermissions.IsITDept
        )
    ]
