from rest_framework import viewsets, permissions
from core import permissions as cpermissions
from assessment import models, serializers, filters

from drf_yasg.utils import no_body, swagger_auto_schema

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
        try:
            user = self.request.data['supervisor']
            return super().perform_create(serializer)
        except Exception:
            return serializer.save(supervisor=self.request.user)
    
    @swagger_auto_schema(
        operation_description="create a quiz",
        operation_summary='create quiz'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all quizzes",
        operation_summary='list quizzes'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a quiz",
        operation_summary='retrieve quiz'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a quiz",
        operation_summary='update quiz'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a quiz",
        operation_summary='partial_update quiz'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a quiz",
        operation_summary='delete quiz'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


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
    
    @swagger_auto_schema(
        operation_description="create a question",
        operation_summary='create question'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all questions",
        operation_summary='list questions'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a question",
        operation_summary='retrieve question'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a question",
        operation_summary='update question'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a question",
        operation_summary='partial_update question'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a question",
        operation_summary='delete question'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


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
    
    @swagger_auto_schema(
        operation_description="create an answer",
        operation_summary='create answer'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all answers",
        operation_summary='list answers'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve an answer",
        operation_summary='retrieve answer'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update an answer",
        operation_summary='update answer'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update an answer",
        operation_summary='partial_update answer'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete an answer",
        operation_summary='delete answer'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class QuizTakerViewSet(viewsets.ModelViewSet):
    queryset = models.QuizTaker.objects.all()
    serializer_class = serializers.QuizTakerSerializer
    serializer_action_classes = {
        'list': serializers.QuizTakerResponseSerializer,
        'retrieve': serializers.QuizTakerResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsLecturer
        | cpermissions.IsStudent
    ]
    filterset_class = filters.QuizTakerFilter
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        # return serializer.save(student=self.request.user.student_set.all().first())
        return super().perform_create(serializer)
    
    @swagger_auto_schema(
        operation_description="create a quiz taker",
        operation_summary='create quiz taker'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all quiz takers",
        operation_summary='list quiz takers'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a quiz taker",
        operation_summary='retrieve quiz taker'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a quiz taker",
        operation_summary='update quiz taker'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a quiz taker",
        operation_summary='partial_update quiz taker'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a quiz taker",
        operation_summary='delete quiz taker'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


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
    
    @swagger_auto_schema(
        operation_description="create a response (question response)",
        operation_summary='create response (question response)'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all responses (question responses)",
        operation_summary='list responses (question responses)'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a response (question response)",
        operation_summary='retrieve response (question response)'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a response (question response)",
        operation_summary='update response (question response)'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a response (question response)",
        operation_summary='partial_update response (question response)'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a response (question response)",
        operation_summary='delete response (question response)'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsLecturerOrReadOnly
    ]
    
    @swagger_auto_schema(
        operation_description="create a grade",
        operation_summary='create grade'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all grades",
        operation_summary='list grades'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a grade",
        operation_summary='retrieve grade'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a grade",
        operation_summary='update grade'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a grade",
        operation_summary='partial_update grade'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a grade",
        operation_summary='delete grade'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)
