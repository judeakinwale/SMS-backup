from django_filters import rest_framework as filters
from assessment import models


class QuizFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Quiz
        fields = {
            'supervisor__first_name': ['icontains'],
            'supervisor__email': ['icontains'],
            'supervisor__last_name': ['icontains'],
            'course__name': ['icontains'],
            'course__code': ['exact'],
            'name': ['icontains'],
            'timer': ['exact'],
            'is_active': ['exact'],
            'is_completed': ['exact'],
        }


class QuestionFilter(filters.FilterSet):
    # label = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Question
        fields = {
            'quiz__name': ['icontains'],
            'label': ['icontains'],
        }


class AnswerFilter(filters.FilterSet):

    class Meta:
        model = models.Answer
        fields = {
            'question__label': ['icontains'],
            'text': ['icontains'],
            'is_correct': ['exact'],
        }


class QuizTakerFilter(filters.FilterSet):

    class Meta:
        model = models.QuizTaker
        fields = {
            # 'student__matric_no': ['icontains'],
            # 'student__user__email': ['icontains'],
            'quiz__name': ['icontains'],
            'completed': ['exact'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class ResponseFilter(filters.FilterSet):

    class Meta:
        model = models.Response
        fields = {
            # 'quiz_taker_student_matric_no': ['icontains'],
            'question__label': ['icontains'],
            # 'answer': ['icontains'],
        }


class AssignmentFilter(filters.FilterSet):
    # label = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Assignment
        fields = {
            'title': ['icontains'],
            'question': ['icontains'],
        }


class AssignmentTakerFilter(filters.FilterSet):

    class Meta:
        model = models.AssignmentTaker
        fields = {
            # 'student__matric_no': ['icontains'],
            # 'student__user__email': ['icontains'],
            # 'quiz__name': ['icontains'],
            # 'completed': ['exact'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class AssignmentResponseFilter(filters.FilterSet):

    class Meta:
        model = models.AssignmentResponse
        fields = {
            # 'quiz_taker_student_matric_no': ['icontains'],
            # 'question__label': ['icontains'],
            # 'answer': ['icontains'],
        }

