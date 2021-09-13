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
        """create a question and create attached answers, if specified in answer_set"""
        if 'answer_set' not in validated_data:
            question = super().create(validated_data)
        else:
            answer_set_data = validated_data.pop('answer_set')
            question = super().create(validated_data)
            for data in answer_set_data:
                data['question'] = question
                answer = models.Answer.objects.create(**data)
        
        return question

    def update(self, instance, validated_data):
        if 'answer_set' not in validated_data:
            question = super().update(instance, validated_data)
        else:
            answers = (instance.answer_set).all()
            list_answers = list(answers)
            answer_set_data = validated_data.pop('answer_set')
            question = super().update(instance, validated_data)
            # print(list_answers)
            if list_answers == []:
                for data in answer_set_data:
                    data['question'] = question
                    models.Answer.objects.create(**data)
            else:
                n = 0
                for data in answer_set_data:
                    try:
                        # data['question'] = question
                        # answer = models.Answer.objects.create(**data)
                        # answer = answers.pop(0)
                        answer = answers[n]
                        answer.question = data.get('question', answer.question) 
                        answer.text = data.get('text', answer.text) 
                        answer.is_correct = data.get('is_correct', answer.is_correct)
                        answer.save()
                    except:
                        data['question'] = question
                        models.Answer.objects.create(**data)
        
        return question
        # return super().update(instance, validated_data)


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Quiz model"""

    supervisor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    question_set = QuestionSerializer(many=True, allow_null=True, required=False)
    course = serializers.HyperlinkedRelatedField(queryset=amodels.Course.objects.all(), view_name='academics:course-detail', allow_null=True, required=False)
    # grade = GradeSerializer(allow_null=True, required=False)
    # grade = serializers.HyperlinkedRelatedField(queryset=models.Grade.objects.all(), view_name='assessment:grade-detail',  allow_null=True, required=False)

    class Meta:
        model = models.Quiz
        fields = [
            'id',
            'url',
            'supervisor',
            'course',
            'name',
            # 'score',
            'max_score',
            # 'grade',
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
        # try:
        #     grade_data = validated_data.pop('grade')
        # except:
        #     pass

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

        # try:
        #     grade = models.Grade.objects.create(grade_data)
        #     quiz.grade = grade   
        #     quiz.save()
        # except:
        #     pass

        # print(quiz)
        return quiz

    def update(self, instance, validated_data):

        if ('question_set' not in validated_data) or validated_data['question_set'] == []:
            quiz = super().update(instance, validated_data)
        else:
            questions = (instance.question_set).all()
            list_questions = list(questions)
            # print(questions)
            question_set_data = validated_data.pop('question_set')
            quiz = super().update(instance, validated_data)

            if list_questions == []:
                for question_data in question_set_data:
                    question_data['quiz'] = quiz
                    # print(f"{question_data}")

                    if ('answer_set' not in question_data) or question_data['answer_set'] == []:
                        question = models.Question.objects.create(**question_data)
                        print(question)
                    # elif question_data['answer_set'] == []:
                    #     answers = question_data.pop('answer_set')
                    #     question = models.Question.objects.create(**question_data)
                    #     print(question)
                    else:
                        answer_set_data = question_data.pop('answer_set')
                        list_answer = list(answer_set_data)
                        question = models.Question.objects.create(**question_data)

                        for answer_data in answer_set_data:
                                answer_data['question'] = question
                                models.Answer.objects.create(**answer_data)

                        # n = 0

                        # if list_answer == []:
                        #     for answer_data in answer_set_data:
                        #         answer_data['question'] = question
                        #         models.Answer.objects.create(**answer_data)
                        # else:
                        #     n = 0

                        #     for answer_data in answer_set_data:
                        #         # answer = answers.pop(0)
                        #         # answer = answers[n]
                        #         # print(f"\n answer_data : {answer_data} \n")
                        #         # answer_data['question'] = question
                        #         # answer = models.Answer.objects.create(**answer_data)
                        #         answer.question = answer_data.get('question', answer.question) 
                        #         answer.text = answer_data.get('text', answer.text) 
                        #         answer.is_correct = answer_data.get('is_correct', answer.is_correct)
                        #         answer.save()

                       


                        # question.label = question_data.get('question', question.label) 
                        # # question.answer_set = question_data.get('text', question.answer_set) 
                        # question.order = question_data.get('is_correct', question.order)
                        # question.save()


                        # if ('answer_set' not in question_data) or question_data['answer_set'] == []:
                        #     question.label = question_data.get('question', question.label) 
                        #     # question.answer_set = question_data.get('text', question.answer_set) 
                        #     question.order = question_data.get('is_correct', question.order)
                        #     question.save()
                        #     # question = models.Question.objects.create(**question_data)
                        # else:
                        #     answer_set_data = question_data.pop('answer_set')
                        #     list_answer = list(answer_set_data)
                        #     # print(f"\n question_data : {question_data} \n")
                        #     question.label = question_data.get('question', question.label) 
                        #     # question.answer_set = question_data.get('text', question.answer_set) 
                        #     question.order = question_data.get('is_correct', question.order)
                        #     question.save()
                        #     # question = models.Question.objects.create(**question_data)
                        #     # print(f"\n answer_set_data : {answer_set_data} \n")

                        #     if list_answer == []:
                        #         for answer_data in answer_set_data:
                        #             answer_data['question'] = question
                        #             models.Answer.objects.create(**answer_data)
                        #     else:
                        #         n = 0

                        #         for answer_data in answer_set_data:
                        #             # answer = answers.pop(0)
                        #             answer = answers[n]
                        #             # print(f"\n answer_data : {answer_data} \n")
                        #             # answer_data['question'] = question
                        #             # answer = models.Answer.objects.create(**answer_data)
                        #             answer.question = answer_data.get('question', answer.question) 
                        #             answer.text = answer_data.get('text', answer.text) 
                        #             answer.is_correct = answer_data.get('is_correct', answer.is_correct)
                        #             answer.save()
                        
            else:

                n = 0

                for question_data in question_set_data:
                    try:
                        # print(questions)
                        # question_data['quiz'] = quiz
                        
                        # if len(questions) > 1:
                        #     # question = questions
                        #     question = questions.pop(0)
                        # else:
                        #     question = questions

                        question = questions[n]
                        n += 1

                        # print(question)
                        # print(question.label)
                        answers = question.answer_set.all()


                        # question.label = question_data.get('question', question.label) 
                        # # question.answer_set = question_data.get('text', question.answer_set) 
                        # question.order = question_data.get('is_correct', question.order)
                        # question.save()


                        if ('answer_set' not in question_data) or validated_data['answer_set'] == []:
                            question.label = question_data.get('question', question.label) 
                            # question.answer_set = question_data.get('text', question.answer_set) 
                            question.order = question_data.get('is_correct', question.order)
                            question.save()
                            # question = models.Question.objects.create(**question_data)
                        else:
                            answer_set_data = question_data.pop('answer_set')
                            list_answer = list(answer_set_data)
                            # print(f"\n question_data : {question_data} \n")
                            question.label = question_data.get('question', question.label) 
                            # question.answer_set = question_data.get('text', question.answer_set) 
                            question.order = question_data.get('is_correct', question.order)
                            question.save()
                            # question = models.Question.objects.create(**question_data)
                            # print(f"\n answer_set_data : {answer_set_data} \n")

                            if list_answer == []:
                                for answer_data in answer_set_data:
                                    answer_data['question'] = question
                                    models.Answer.objects.create(**answer_data)
                            else:
                                n = 0

                                for answer_data in answer_set_data:
                                    try:
                                        # answer = answers.pop(0)
                                        answer = answers[n]
                                        # print(f"\n answer_data : {answer_data} \n")
                                        # answer_data['question'] = question
                                        # answer = models.Answer.objects.create(**answer_data)
                                        answer.question = answer_data.get('question', answer.question) 
                                        answer.text = answer_data.get('text', answer.text) 
                                        answer.is_correct = answer_data.get('is_correct', answer.is_correct)
                                        answer.save()
                                        # print(f"\n answer : {answer} \n")
                                    except:
                                        answer_data['question'] = question
                                        models.Answer.objects.create(**answer_data)
                    except:
                        question_data['quiz'] = quiz
                        # print(f"{question_data}")

                        if ('answer_set' not in question_data) or question_data['answer_set'] == []:
                            question = models.Question.objects.create(**question_data)
                            print(question)
                        # elif question_data['answer_set'] == []:
                        #     answers = question_data.pop('answer_set')
                        #     question = models.Question.objects.create(**question_data)
                        #     print(question)
                        else:
                            answer_set_data = question_data.pop('answer_set')
                            list_answer = list(answer_set_data)
                            question = models.Question.objects.create(**question_data)

                            for answer_data in answer_set_data:
                                    answer_data['question'] = question
                                    models.Answer.objects.create(**answer_data)


        # try:
        #     grade = models.Grade.objects.create(grade_data)
        #     quiz.grade = grade   
        #     quiz.save()
        # except:
        #     pass
        # print(quiz)
        return quiz
        # return super().update(instance, validated_data)


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
    # score = serializers.SerializerMethodField()
    score = serializers.ReadOnlyField()

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

    # def get_score(self, obj):
    #     return obj.get_score()


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


