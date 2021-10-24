from rest_framework import viewsets, permissions
from core import permissions as cpermissions
from assessment import models, serializers, filters

# Create your views here.


class QuizViewSet(viewsets.ModelViewSet):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsLecturer
        | cpermissions.IsHead
    ]
    filterset_class = filters.QuizFilter

    def perform_create(self, serializer):
        return serializer.save(supervisor=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsLecturer
        | cpermissions.IsHead
    ]
    filterset_class = filters.QuestionFilter


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsLecturer
        | cpermissions.IsHead
    ]
    filterset_class = filters.AnswerFilter


class QuizTakerViewSet(viewsets.ModelViewSet):
    queryset = models.QuizTaker.objects.all()
    serializer_class = serializers.QuizTakerSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsLecturer
        | cpermissions.IsStudent
    ]
    filterset_class = filters.QuizTakerFilter

    def perform_create(self, serializer):
        return serializer.save(student=self.request.user)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsStudent
    ]
    filterset_class = filters.ResponseFilter


class GradeViewSet(viewsets.ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsLecturerOrReadOnly
    ]
