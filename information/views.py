from rest_framework import viewsets, permissions
from rest_framework import status, views, response
from information import models, serializers, filters, utils
from core import permissions as cpermissions
from core import mixins
from academics import models as amodels
from drf_yasg.utils import no_body, swagger_auto_schema

# Create your views here.


class InformationViewSet(
    mixins.swagger_documentation_factory("information", "an", "information"),
    viewsets.ModelViewSet
    ):
    """Viewset for the information endpoint with generated swagger documentation"""
    queryset = models.Information.objects.all()
    serializer_class = serializers.InformationSerializer
    permission_classes = [
        cpermissions.IsStaff
        or cpermissions.IsSuperUserOrReadOnly
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.InformationFilter

    def perform_create(self, serializer):
        if 'source' not in serializer.validated_data:
            serializer.validated_data['source'] = self.request.user
        return super().perform_create(serializer)


class NoticeViewSet(mixins.swagger_documentation_factory("notice"), viewsets.ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    permission_classes = [
        cpermissions.IsStaff
        or cpermissions.IsSuperUserOrReadOnly
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.NoticeFilter

    def perform_create(self, serializer):
        if 'source' not in serializer.validated_data:
            serializer.validated_data['source'] = self.request.user
        return super().perform_create(serializer)


class InformationImageViewSet(mixins.swagger_documentation_factory("information image", "an"), viewsets.ModelViewSet):
    queryset = models.InformationImage.objects.all()
    serializer_class = serializers.InformationImageSerializer
    permission_classes = [
        cpermissions.IsStaff
        or cpermissions.IsSuperUserOrReadOnly
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.InformationImageFilter


class ScopeViewSet(mixins.swagger_documentation_factory("scope"), viewsets.ModelViewSet):
    queryset = models.Scope.objects.all()
    serializer_class = serializers.ScopeSerializer
    permission_classes = [
        cpermissions.IsStaff
        or cpermissions.IsSuperUserOrReadOnly
        or cpermissions.IsITDeptOrReadOnly
    ]
