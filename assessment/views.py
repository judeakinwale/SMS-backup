from rest_framework import viewsets, permissions
from rest_framework import status, views, response
from core import permissions as cpermissions
from core import mixins
from assessment import models, serializers, filters, utils
from academics import models as amodels

from drf_yasg.utils import no_body, swagger_auto_schema

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
        course = amodels.Course.objects.get(id=int(self.request.data['course']))
        if (serializer.validated_data['supervisor'] != course.coordinator) or not self.request.user.is_superuser:
            raise Exception(f"Not authorized to create a test for course with id {course.id}")
        
        # send emails to students registered for the course
        utils.create_scoped_student_assessment_notice(request=request, assessment=assignment, _type="test")
    
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

        # confirm the authenticated user has permission to create an assignment for the course
        course = amodels.Course.objects.get(id=serializer.validated_data['course'])
        if (serializer.validated_data['supervisor'] != course.coordinator) or not self.request.user.is_superuser:
            raise Exception(f"Not authorized to create an assignment for course with id {course.id}")
        
        # send emails to students registered for the course 
        utils.create_scoped_student_assessment_notice(request=request, assessment=assignment)
    
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
    # filterset_class = filters.AssignmentTakerFilter
    
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


class AssignmentResponseViewSet(mixins.swagger_documentation_factory("assignment response", "an"), viewsets.ModelViewSet):
    queryset = models.AssignmentResponse.objects.all()
    serializer_class = serializers.AssignmentResponseSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        | cpermissions.IsITDept
        | cpermissions.IsHead
        | cpermissions.IsStudentOrReadOnly
    ]
    # filterset_class = filters.AssignmentResponseFilter


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
    