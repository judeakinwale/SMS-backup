from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from user import serializers, models

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]

    def perform_create(self, serializer):
        # print(serializer.data)
        print(models.Biodata.objects.filter(user=self.request.user))
        return super().perform_create(serializer)


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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]


class BiodataViewSet(viewsets.ModelViewSet):
    queryset = models.Biodata.objects.all()
    serializer_class = serializers.BiodataSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]


class AcademicDataViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicData.objects.all()
    serializer_class = serializers.AcademicDataSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]


class AcademicHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicHistory.objects.all()
    serializer_class = serializers.AcademicHistorySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]


class HealthDataViewSet(viewsets.ModelViewSet):
    queryset = models.HealthData.objects.all()
    serializer_class = serializers.HealthDataSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]


class FamilyDataViewSet(viewsets.ModelViewSet):
    queryset = models.FamilyData.objects.all()
    serializer_class = serializers.FamilyDataSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser]
    