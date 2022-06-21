from rest_framework import viewsets, permissions
from rest_framework import status, views, response
from core import permissions as cpermissions
from core import mixins
from assessment import models, serializers, filters, utils
from academics import models as amodels

from drf_yasg.utils import no_body, swagger_auto_schema
from datetime import datetime

# Create your views here.


class QuizViewSet(mixins.swagger_documentation_factory("Quiz","a","Quizzes"), viewsets.ModelViewSet):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStaff
        | cpermissions.IsITDept
        | cpermissions.IsLecturer
        | cpermissions.IsHeadOrReadOnly
    ]
    filterset_class = filters.QuizFilter

    def perform_create(self, serializer):
        if 'supervisor' not in serializer.validated_data:
            serializer.validated_data['supervisor'] = self.request.user

        # confirm the authenticated user has permission to create a test for the course
        if self.request.user.is_superuser:
            return super().perform_create(serializer)
        
        course = serializer.validated_data['course']
        supervisor = serializer.validated_data['supervisor']
        if supervisor != course.coordinator:
            raise Exception(f"Not authorized to create a test for course with id {course.id}")
        
        return super().perform_create(serializer)


class QuestionViewSet(mixins.swagger_documentation_factory("question"), viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStaff
        | cpermissions.IsITDept
        | cpermissions.IsLecturer
        | cpermissions.IsHeadOrReadOnly
    ]
    filterset_class = filters.QuestionFilter


class AnswerViewSet(mixins.swagger_documentation_factory("answer", "an"), viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStaff
        | cpermissions.IsITDept
        | cpermissions.IsLecturer
        | cpermissions.IsHeadOrReadOnly
    ]
    filterset_class = filters.AnswerFilter


class QuizTakerViewSet(mixins.swagger_documentation_factory("quiz taker"), viewsets.ModelViewSet):
    queryset = models.QuizTaker.objects.all()
    serializer_class = serializers.QuizTakerSerializer
    serializer_action_classes = {
        'list': serializers.QuizTakerResponseSerializer,
        'retrieve': serializers.QuizTakerResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStaff
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsLecturer
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.QuizTakerFilter
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        if "student" not in serializer.validated_data:
            try:
                serializer.validated_data["student"] = self.request.user.student_set.all().first()
            except Exception as e:
                print(f'An exception occurred: {e}')
                raise Exception(f"Student not specified for quiz taker")
        return super().perform_create(serializer)


class ResponseViewSet(mixins.swagger_documentation_factory("response"), viewsets.ModelViewSet):
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.ResponseFilter
    
    def perform_create(self, serializer):
        quiz = serializer.validated_data["quiz"]
        quiz_taker = serializer.validated_data["quiz_taker"]
        # # raise exception if current day is past the due date
        # if datetime.today().date() > quiz.due_date:
        #     raise Exception("You are unable to submit this quiz. the due date is past.")
        # raise exception if quiz has been submitted
        if quiz_taker.completed:
            raise Exception("You have submitted this quiz")
        # raise exception if authenticated user is not authorized
        if quiz_taker.student.user != request.user and  not request.user.is_superuser:
            raise Exception("You are not authorized to submit a response to this quiz")
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        print("starting perform create function")
        quiz = serializer.validated_data.get("quiz", instance.quiz)
        quiz_taker = serializer.validated_data.get("quiz_taker", instance.quiz_taker)
        # # raise exception if current day is past the due date
        # if datetime.today().date() > quiz.due_date:
        #     raise Exception("You are unable to submit this quiz. the due date is past.")
        # raise exception if quiz has been submitted
        if quiz_taker.completed:
            raise Exception("You have submitted this quiz")
        # raise exception if authenticated user is not authorized
        if quiz_taker.student.user != request.user and  not request.user.is_superuser:
            raise Exception("You are not authorized to submit a response to this quiz")
        return super().perform_update(serializer)


class AssignmentViewSet(mixins.swagger_documentation_factory("assignment", "an"), viewsets.ModelViewSet):
    queryset = models.Assignment.objects.all()
    serializer_class = serializers.AssignmentSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStaff
        | cpermissions.IsITDept
        | cpermissions.IsLecturer
        | cpermissions.IsStudent
        | cpermissions.IsHeadOrReadOnly
    ]
    filterset_class = filters.AssignmentFilter
    
    def perform_create(self, serializer):
        if 'supervisor' not in serializer.validated_data:
            serializer.validated_data['supervisor'] = self.request.user

        # confirm the authenticated user has permission to create a test for the course
        if self.request.user.is_superuser:
            return super().perform_create(serializer)
        
        course = serializer.validated_data['course']
        supervisor = serializer.validated_data['supervisor']
        if supervisor != course.coordinator:
            raise Exception(f"Not authorized to create an assignment for course with id {course.id}")
        
        return super().perform_create(serializer)

class AssignmentTakerViewSet(mixins.swagger_documentation_factory("assignment taker", "an"), viewsets.ModelViewSet):
    queryset = models.AssignmentTaker.objects.all()
    serializer_class = serializers.AssignmentTakerSerializer
    serializer_action_classes = {
        'list': serializers.AssignmentTakerResponseSerializer,
        'retrieve': serializers.AssignmentTakerResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsStaff
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsLecturer
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.AssignmentTakerFilter
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        if "student" not in serializer.validated_data:
            try:
                serializer.validated_data["student"] = self.request.user.student_set.all().first()
            except Exception as e:
                print(f'An exception occurred: {e}')
                raise Exception(f"Student not specified for assignment taker")
        return super().perform_create(serializer)


class AssignmentResponseViewSet(mixins.swagger_documentation_factory("assignment response", "an"), viewsets.ModelViewSet):
    queryset = models.AssignmentResponse.objects.all()
    serializer_class = serializers.AssignmentResponseSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.AssignmentResponseFilter
    
    def perform_create(self, serializer):
        assignment = serializer.validated_data["assignment"]
        assignment_taker = serializer.validated_data["assignment_taker"]
        # raise exception if current day is past the due date
        if datetime.today().date() > assignment.due_date:
            raise Exception("You are unable to submit this assignment. the due date is past.")
        # raise exception if assignment has been submitted
        if assignment_taker.completed:
            raise Exception("You have submitted this assignment")
        # raise exception if authenticated user is not authorized
        if assignment_taker.student.user != request.user and  not request.user.is_superuser:
            raise Exception("You are not authorized to submit an answer to this assignment")
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        print("starting perform create function")
        assignment = serializer.validated_data.get("assignment", instance.assignment)
        assignment_taker = serializer.validated_data.get("assignment_taker", instance.assignment_taker)
        # raise exception if current day is past the due date
        if datetime.today().date() > assignment.due_date:
            raise Exception("You are unable to submit this assignment. the due date is past.")
        # raise exception if assignment has been submitted
        if assignment_taker.completed:
            raise Exception("You have submitted this assignment")
        # raise exception if authenticated user is not authorized
        if assignment_taker.student.user != request.user and  not request.user.is_superuser:
            raise Exception("You are not authorized to submit an answer to this assignment")
        return super().perform_update(serializer)


class GradeViewSet(mixins.swagger_documentation_factory("grade"), viewsets.ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsStaff
        | cpermissions.IsStudent
        | cpermissions.IsLecturerOrReadOnly
    ]
    