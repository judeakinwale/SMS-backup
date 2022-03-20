# from django.shortcuts import render
from rest_framework import viewsets, permissions
from information import models, serializers, filters
from core import permissions as cpermissions

from drf_yasg.utils import no_body, swagger_auto_schema

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
        try:
            user = self.request.data['source']
            return super().perform_create(serializer)
        except Exception:
            return serializer.save(source=self.request.user)
    
    @swagger_auto_schema(
        operation_description="create a information",
        operation_summary='create information'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all information",
        operation_summary='list information'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a information",
        operation_summary='retrieve information'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a information",
        operation_summary='update information'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a information",
        operation_summary='partial_update information'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a information",
        operation_summary='delete information'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.NoticeFilter

    def perform_create(self, serializer):
        try:
            user = self.request.data['source']
            return super().perform_create(serializer)
        except Exception:
            return serializer.save(source=self.request.user)
    
    @swagger_auto_schema(
        operation_description="create a notice",
        operation_summary='create notice'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all notices",
        operation_summary='list notices'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a notice",
        operation_summary='retrieve notice'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a notice",
        operation_summary='update notice'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a notice",
        operation_summary='partial_update notice'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a notice",
        operation_summary='delete notice'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class InformationImageViewSet(viewsets.ModelViewSet):
    queryset = models.InformationImage.objects.all()
    serializer_class = serializers.InformationImageSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.InformationImageFilter
    
    @swagger_auto_schema(
        operation_description="create an information image",
        operation_summary='create information image'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all information images",
        operation_summary='list information images'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve an information image",
        operation_summary='retrieve information image'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update an information image",
        operation_summary='update information image'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update an information image",
        operation_summary='partial_update information image'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete an information image",
        operation_summary='delete information image'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class ScopeViewSet(viewsets.ModelViewSet):
    queryset = models.Scope.objects.all()
    serializer_class = serializers.ScopeSerializer
    permission_classes = [
        cpermissions.IsSuperUserOrReadOnly
        | cpermissions.IsITDeptOrReadOnly
    ]
    
    @swagger_auto_schema(
        operation_description="create a scope",
        operation_summary='create scope'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all scopes",
        operation_summary='list scopes'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a scope",
        operation_summary='retrieve scope'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a scope",
        operation_summary='update scope'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a scope",
        operation_summary='partial_update scope'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a scope",
        operation_summary='delete scope'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)
