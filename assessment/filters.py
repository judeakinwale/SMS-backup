from django_filters import rest_framework as filters
from assessment import models


class QuizFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Quiz
        fields = {
            'supervisor__id': ['exact'],
            'course__id': ['exact'],
            'supervisor__first_name': ['icontains'],
            'supervisor__email': ['icontains', 'exact'],
            'supervisor__last_name': ['icontains'],
            'course__name': ['icontains'],
            'course__code': ['exact'],
            'name': ['icontains'],
            'timer': ['exact'],
            'is_active': ['exact'],
            'is_completed': ['exact'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class QuestionFilter(filters.FilterSet):
    # label = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Question
        fields = {
            'quiz__name': ['icontains'],
            'label': ['icontains'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class AnswerFilter(filters.FilterSet):

    class Meta:
        model = models.Answer
        fields = {
            'question__label': ['icontains'],
            'text': ['icontains'],
            'is_correct': ['exact'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class QuizTakerFilter(filters.FilterSet):

    class Meta:
        model = models.QuizTaker
        fields = {
            'quiz__id': ['exact'],
            'student__id': ['exact'],
            'student__matric_no': ['icontains', 'exact'],
            'student__user__email': ['icontains', 'exact'],
            'quiz__name': ['icontains', 'exact'],
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
            'timestamp': ['exact', 'lt', 'gt'],
        }


class AssignmentFilter(filters.FilterSet):
    # label = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Assignment
        fields = {
            'supervisor__id': ['exact'],
            'course__id': ['exact'],
            'supervisor__first_name': ['icontains'],
            'supervisor__email': ['icontains', 'exact'],
            'supervisor__last_name': ['icontains'],
            'course__name': ['icontains'],
            'course__code': ['exact'],
            'title': ['icontains'],
            'question': ['icontains'],
            'is_active': ['exact'],
            'is_completed': ['exact'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class AssignmentTakerFilter(filters.FilterSet):

    class Meta:
        model = models.AssignmentTaker
        fields = {
            'assignment__id': ['exact'],
            'student__id': ['exact'],
            'student__matric_no': ['icontains', 'exact'],
            'student__user__email': ['icontains', 'exact'],
            'assignment__title': ['icontains', 'exact'],
            'completed': ['exact'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class AssignmentResponseFilter(filters.FilterSet):

    class Meta:
        model = models.AssignmentResponse
        fields = {
            # 'quiz_taker_student_matric_no': ['icontains'],
            # 'question__label': ['icontains'],
            # 'answer': ['icontains'],
            'timestamp': ['exact', 'lt', 'gt'],
        }

