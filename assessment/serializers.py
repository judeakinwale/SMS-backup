from django.contrib.auth import get_user_model
from rest_framework import serializers
from assessment import models
from academics import models as amodels


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Grade model"""

    # quiz = serializers.HyperlinkedRelatedField(
    #     queryset=models.Quiz.objects.all(),
    #     view_name='assessment:quiz-detail',
    # )

    class Meta:
        model = models.Grade
        fields = [
            'id',
            'url',
            # 'quiz',
            'score',
            'max_score',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:grade-detail'}
        }


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Answer model"""

    question = serializers.HyperlinkedRelatedField(
        queryset=models.Question.objects.all(),
        view_name='assessment:question-detail',
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.Answer
        fields = [
            'id',
            'url',
            'question',
            'text',
            'is_correct',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:answer-detail'}
        }


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Question model"""

    quiz = serializers.HyperlinkedRelatedField(
        queryset=models.Quiz.objects.all(),
        view_name='assessment:quiz-detail',
        allow_null=True,
        required=False,
    )
    answer_set = AnswerSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = models.Question
        fields = [
            'id',
            'url',
            'quiz',
            'label',
            'answer_set',
            'order',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:question-detail'}
        }

    def create(self, validated_data):
        """create a question and create attached quesions, if specified in answer_set"""
        if 'answer_set' not in validated_data:
            question = super().create(validated_data)
        else:
            answer_set_data = validated_data.pop('answer_set')
            question = super().create(validated_data)
            for data in answer_set_data:
                data['question'] = question
                answer = models.Answer.objects.create(**data)
        
        return question


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Quiz model"""

    supervisor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    question_set = QuestionSerializer(many=True, allow_null=True, required=False)
    course = serializers.HyperlinkedRelatedField(queryset=amodels.Course.objects.all(), view_name='academics:course-detail', allow_null=True, required=False)
    # grade = GradeSerializer(allow_null=True, required=False)
    grade = serializers.HyperlinkedRelatedField(queryset=models.Grade.objects.all(), view_name='assessment:grade-detail',  allow_null=True, required=False)

    class Meta:
        model = models.Quiz
        fields = [
            'id',
            'url',
            'supervisor',
            'course',
            'name',
            'score',
            'max_score',
            'grade',
            'question_set',
            'description',
            'is_active',
            'is_completed',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:quiz-detail'}
        }

    def create(self, validated_data):
        """create a quiz and create attached quesions, if specified in question_set"""
        try:
            grade_data = validated_data.pop('grade')
        except:
            pass

        if 'question_set' not in validated_data:
            quiz = super().create(validated_data)
        else:
            question_set_data = validated_data.pop('question_set')
            quiz = super().create(validated_data)
            for question_data in question_set_data:
                question_data['quiz'] = quiz

                if 'answer_set' not in question_data:
                    question = models.Question.objects.create(**question_data)
                else:
                    answer_set_data = question_data.pop('answer_set')
                    # print(f"\n question_data : {question_data} \n")
                    question = models.Question.objects.create(**question_data)
                    # print(f"\n answer_set_data : {answer_set_data} \n")
                    for answer_data in answer_set_data:
                        # print(f"\n answer_data : {answer_data} \n")
                        answer_data['question'] = question
                        answer = models.Answer.objects.create(**answer_data)
                        # print(f"\n answer : {answer} \n")

        try:
            grade = models.Grade.objects.create(grade_data)
            quiz.grade = grade   
            quiz.save()
        except:
            pass

        return quiz


class QuizTakerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the QuizTaker model"""

    student = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    quiz = serializers.HyperlinkedRelatedField(
        queryset=models.Quiz.objects.all(),
        view_name='assessment:quiz-detail',
        allow_null=True,
        required=False,
    )
    grade = serializers.HyperlinkedRelatedField(
        queryset=models.Grade.objects.all(),
        view_name='assessment:grade-detail',
        allow_null=True,
        required=False,
    )
    score = serializers.SerializerMethodField()

    class Meta:
        model = models.QuizTaker
        fields = [
            'id',
            'url',
            'student',
            'quiz',
            'grade',
            'score',
            'completed',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:quiztaker-detail'}
        }

    def get_score(self, obj):
        return obj.get_score()


class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Response model"""

    quiz_taker = serializers.HyperlinkedRelatedField(
        queryset=models.QuizTaker.objects.all(),
        view_name='assessment:quiztaker-detail',
    )
    question = serializers.HyperlinkedRelatedField(
        queryset=models.Question.objects.all(),
        view_name='assessment:question-detail',
    )
    answer = serializers.HyperlinkedRelatedField(
        queryset=models.Answer.objects.all(),
        view_name='assessment:answer-detail',
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.Response
        fields = [
            'id',
            'url',
            'quiz_taker',
            'question',
            'answer',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:response-detail'}
        }


