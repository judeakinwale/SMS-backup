from django.shortcuts import render
from rest_framework import generics, viewsets, authentication, permissions
from rest_framework.serializers import Serializer
from information import models, serializers
from core import permissions as cpermissions

# Create your views here.


class InformationViewSet(viewsets.ModelViewSet):
    queryset = models.Information.objects.all()
    serializer_class = serializers.InformationSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser |
            # cpermissions.IsOwner |
            cpermissions.IsITDeptOrReadOnly
        )
    ]

    def perform_create(self, serializer):
        return serializer.save(source=self.request.user)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser |
            # cpermissions.IsOwner |
            cpermissions.IsITDept
        )
    ]

    def perform_create(self, serializer):
        return serializer.save(source=self.request.user)


class InformationImageViewSet(viewsets.ModelViewSet):
    queryset = models.InformationImage.objects.all()
    serializer_class = serializers.InformationImageSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser |
            cpermissions.IsITDeptOrReadOnly
        )
    ]


class ScopeViewSet(viewsets.ModelViewSet):
    queryset = models.Scope.objects.all()
    serializer_class = serializers.ScopeSerializer
    permission_classes = [
        permissions.IsAuthenticated & (
            cpermissions.IsSuperUser |
            cpermissions.IsITDept
        )
    ]
