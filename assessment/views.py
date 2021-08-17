from django.shortcuts import render
from rest_framework import viewsets, permissions
from core import permissions as cpermissions
from assessment import models, serializers

# Create your views here.


class QuizViewSet(viewsets.ModelViewSet):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    # permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]
    permission_classes = [
        permissions.IsAuthenticated &
        permissions.IsAdminUser | 
        cpermissions.IsITDept 
        # cpermissions.IsOwner | 
        # cpermissions.IsHead
    ]

    def perform_create(self, serializer):
        return serializer.save(supervisor=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        permissions.IsAdminUser | 
        cpermissions.IsITDept 
        # cpermissions.IsOwner | 
        # cpermissions.IsHead
    ]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        permissions.IsAdminUser | 
        cpermissions.IsITDept 
        # cpermissions.IsOwner |
        # cpermissions.IsHead
    ]

class QuizTakerViewSet(viewsets.ModelViewSet):
    queryset = models.QuizTaker.objects.all()
    serializer_class = serializers.QuizTakerSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        permissions.IsAdminUser |
        cpermissions.IsITDept 
        # cpermissions.IsOwner |
        # cpermissions.IsHead |
        # cpermissions.IsStudent
    ]

    def perform_create(self, serializer):
        return serializer.save(student=self.request.user)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        permissions.IsAdminUser |
        cpermissions.IsITDept 
        # cpermissions.IsOwner |
        # cpermissions.IsHead |
        # cpermissions.IsStudent
    ]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        permissions.IsAdminUser |
        cpermissions.IsITDept 
        # cpermissions.IsOwner |
        # cpermissions.IsHead |
        # cpermissions.IsStudent |
        # cpermissions.IsLecturer
    ]
