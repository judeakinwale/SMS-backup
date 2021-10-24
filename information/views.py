# from django.shortcuts import render
from rest_framework import viewsets, permissions
from information import models, serializers, filters
from core import permissions as cpermissions

# Create your views here.


class InformationViewSet(viewsets.ModelViewSet):
    queryset = models.Information.objects.all()
    serializer_class = serializers.InformationSerializer
    permission_classes = [
        # permissions.IsAuthenticated & (
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
        # )
    ]
    filterset_class = filters.InformationFilter

    def perform_create(self, serializer):
        return serializer.save(source=self.request.user)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.NoticeFilter

    def perform_create(self, serializer):
        return serializer.save(source=self.request.user)


class InformationImageViewSet(viewsets.ModelViewSet):
    queryset = models.InformationImage.objects.all()
    serializer_class = serializers.InformationImageSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.InformationImageFilter


class ScopeViewSet(viewsets.ModelViewSet):
    queryset = models.Scope.objects.all()
    serializer_class = serializers.ScopeSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
