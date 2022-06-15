from django.contrib.auth import get_user_model
from rest_framework import serializers
from assessment import models, utils
from academics import models as amodels
from user import models as umodels


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Grade model"""
    
    value = serializers.ReadOnlyField(source='get_value')
    grade = serializers.ReadOnlyField(source='get_grade')

    class Meta:
        model = models.Grade
        fields = [
            'id',
            'url',
            'score',
            'max_score',
            'value',
            'grade',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:grade-detail'}
        }


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Answer model"""

    question = serializers.PrimaryKeyRelatedField(
        queryset=models.Question.objects.all(),
        allow_null=True, required=False,
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
            'url': {'view_name': 'assessment:answer-detail'},
            'is_correct': {'write_only': True}
        }


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Question model"""

    quiz = serializers.PrimaryKeyRelatedField(
        queryset=models.Quiz.objects.all(),
        allow_null=True, required=False,
    )
    answer_set = AnswerSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = models.Question
        fields = [
            'id',
            'url',
            'quiz',
            'label',
            'file',
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
                models.Answer.objects.create(**data)

        return question

    def update(self, instance, validated_data):
        # if 'answer_set' not in validated_data:
        #     question = super().update(instance, validated_data)
        # else:
        #     answers = (instance.answer_set).all()
        #     list_answers = list(answers)
        #     answer_set_data = validated_data.pop('answer_set')
        #     question = super().update(instance, validated_data)
        #     if list_answers == []:
        #         for data in answer_set_data:
        #             data['question'] = question
        #             models.Answer.objects.create(**data)
        #     else:
        #         n = 0
        #         for data in answer_set_data:
        #             try:
        #                 answer = answers[n]
        #                 answer.question = data.get('question', answer.question)
        #                 answer.text = data.get('text', answer.text)
        #                 answer.is_correct = data.get('is_correct', answer.is_correct)
        #                 answer.save()
        #             except Exception:
        #                 data['question'] = question
        #                 models.Answer.objects.create(**data)
            
        question = None            
        try:
            if "answer_set" not in validated_data:
                raise Exception("No answers provided")
            answers_data = validated_data.pop('answer_set')
            question = super().update(instance, validated_data)
            for answer_data in answers_data:
                nested_data = answer_data
                nested_data["question"] = question
                answers = None
                try:
                    answers = models.Answer.objects.filter(**nested_data)
                    answer, created = models.Answer.objects.get_or_create(**nested_data)
                except Exception as e:
                    if not answers:
                        raise Exception(f"Error during answer creation: {e}")
                    raise Exception(e)
        except Exception as e:
            print(f"There was an exception updating answers: {e}")
            question = super().update(instance, validated_data) if not question else question

        return question


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Quiz model"""

    # supervisor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    supervisor = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        allow_null=True, required=False,
    )
    question_set = QuestionSerializer(many=True, allow_null=True, required=False)
    course = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Course.objects.all(),
        allow_null=True, required=False,
    )

    class Meta:
        model = models.Quiz
        fields = [
            'id',
            'url',
            'supervisor',
            'course',
            'name',
            'max_score',
            'question_set',
            'description',
            'timer',
            'is_active',
            'is_completed',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:quiz-detail'}
        }

    def create(self, validated_data):
        """create a quiz and create attached quesions, if specified in question_set"""

        if 'question_set' not in validated_data:
            print("No questions provided")
            quiz = super().create(validated_data)
        else:
            question_set_data = validated_data.pop('question_set')
            quiz = super().create(validated_data)
            for question_data in question_set_data:
                question_data['quiz'] = quiz

                if 'answer_set' not in question_data:
                    print("No answers provided")
                    question = models.Question.objects.create(**question_data)
                else:
                    answer_set_data = question_data.pop('answer_set')
                    question = models.Question.objects.create(**question_data)
                    for answer_data in answer_set_data:
                        answer_data['question'] = question
                        models.Answer.objects.create(**answer_data)
        
        try:
            # # create a notice for the test, which sends a mail to all relevant students
            # # requires request
            # utils.create_scoped_student_assessment_notice(self.request, quiz, _type="test")
            # create quiztaker instances for relevant students, registering them for the test
            utils.register_assessment_takers(quiz)
        except Exception as e:
            print(f"An exception occurred while creating a notice or registering students: {e}")

        return quiz

    def update(self, instance, validated_data):

        # if ('question_set' not in validated_data) or validated_data['question_set'] == []:
        #     quiz = super().update(instance, validated_data)
        # else:
        #     questions = (instance.question_set).all()
        #     list_questions = list(questions)
        #     question_set_data = validated_data.pop('question_set')
        #     quiz = super().update(instance, validated_data)

        #     if list_questions == []:
        #         for question_data in question_set_data:
        #             question_data['quiz'] = quiz

        #             if ('answer_set' not in question_data) or question_data['answer_set'] == []:
        #                 question = models.Question.objects.create(**question_data)
        #                 print(question)
        #             else:
        #                 answer_set_data = question_data.pop('answer_set')
        #                 list_answer = list(answer_set_data)
        #                 question = models.Question.objects.create(**question_data)

        #                 for answer_data in answer_set_data:
        #                     answer_data['question'] = question
        #                     models.Answer.objects.create(**answer_data)
        #     else:
        #         n = 0

        #         for question_data in question_set_data:
        #             try:
        #                 question = questions[n]
        #                 n += 1

        #                 answers = question.answer_set.all()

        #                 if ('answer_set' not in question_data) or validated_data['answer_set'] == []:
        #                     question.label = question_data.get('question', question.label)
        #                     question.order = question_data.get('is_correct', question.order)
        #                     question.save()
        #                 else:
        #                     answer_set_data = question_data.pop('answer_set')
        #                     list_answer = list(answer_set_data)
        #                     question.label = question_data.get('question', question.label)
        #                     question.order = question_data.get('is_correct', question.order)
        #                     question.save()

        #                     if list_answer == []:
        #                         for answer_data in answer_set_data:
        #                             answer_data['question'] = question
        #                             models.Answer.objects.create(**answer_data)
        #                     else:
        #                         n = 0

        #                         for answer_data in answer_set_data:
        #                             try:
        #                                 answer = answers[n]
        #                                 answer.question = answer_data.get('question', answer.question)
        #                                 answer.text = answer_data.get('text', answer.text)
        #                                 answer.is_correct = answer_data.get('is_correct', answer.is_correct)
        #                                 answer.save()
        #                             except Exception:
        #                                 answer_data['question'] = question
        #                                 models.Answer.objects.create(**answer_data)
        #             except Exception:
        #                 question_data['quiz'] = quiz

        #                 if ('answer_set' not in question_data) or question_data['answer_set'] == []:
        #                     question = models.Question.objects.create(**question_data)
        #                     print(question)
        #                 else:
        #                     answer_set_data = question_data.pop('answer_set')
        #                     list_answer = list(answer_set_data)
        #                     question = models.Question.objects.create(**question_data)

        #                     for answer_data in answer_set_data:
        #                         answer_data['question'] = question
        #                         models.Answer.objects.create(**answer_data)
        
        try:
            if 'question_set' not in validated_data:
                raise Exception("No questions provided")    
            question_set_data = validated_data.pop('question_set')
            quiz = super().update(instance, validated_data)
            for question_data in question_set_data:
                nested_data = question_data
                nested_data["quiz"] = quiz
                questions = None
                try:
                    if "answer_set" not in nested_data:
                        raise Exception("No answers provided in nested question")
                    answer_set_data = nested_data.pop("answer_set")
                    
                    questions = models.Question.objects.filter(**nested_data)
                    question, created = models.Question.objects.get_or_create(**nested_data)
                    
                    for answer_data in answer_set_data:
                        nested_data = answer_data
                        nested_data["question"] = question
                        answers = None
                        try:
                            print(nested_data)
                            answers = models.Answer.objects.filter(**nested_data)
                            answer, created = models.Answer.objects.get_or_create(**nested_data)
                        except Exception as e:
                            if not answers:
                                raise Exception(f"Error during answer creation: {e}")
                            raise Exception(e)
                except Exception as e:
                    if not questions:
                        raise Exception(f"Error during question creation: {e}")
                    raise Exception(e)
        except  Exception as e:
            print(f"There was an exception updating the quiz: {e}")
            quiz = super().update(instance, validated_data) if not quiz else quiz

        try:
            # # create a notice for the test, which sends a mail to all relevant students
            # # requires request
            # utils.create_scoped_student_assessment_notice(self.request, quiz, _type="test")
            # create quiztaker instances for relevant students, registering them for the test
            utils.register_assessment_takers(quiz, _type="test")
        except Exception as e:
            print(f"An exception occurred while creating a notice or registering students: {e}")
        
        return quiz


class QuizTakerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the QuizTaker model"""

    # student = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    student = serializers.PrimaryKeyRelatedField(
        # queryset=get_user_model().objects.all(),
        queryset=umodels.Student.objects.all(),
        allow_null=True, required=False,
    )
    quiz = serializers.PrimaryKeyRelatedField(
        queryset=models.Quiz.objects.all(),
        allow_null=True, required=False,
    )
    grade = serializers.PrimaryKeyRelatedField(
        queryset=models.Grade.objects.all(),
        allow_null=True, required=False,
    )
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
        
        
class QuizTakerResponseSerializer(QuizTakerSerializer):
    """serializer for the QuizTaker model"""

    quiz = QuizSerializer(read_only=True)
    grade = GradeSerializer(read_only=True)


class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Response model"""

    quiz_taker = serializers.PrimaryKeyRelatedField(
        queryset=models.QuizTaker.objects.all(),
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=models.Question.objects.all(),
    )
    answer = serializers.PrimaryKeyRelatedField(
        queryset=models.Answer.objects.all(),
        allow_null=True, required=False,
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


class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Assignment model"""

    course = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Course.objects.all(),
        allow_null=True, required=False,
    )

    class Meta:
        model = models.Assignment
        fields = [
            'id',
            'url',
            'title',
            'question',
            # 'answer',
            'course',
            'file',
            'max_score',
            'due_date',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:assignment-detail'}
        }
        
    def create(self, validated_data):
        assignment = super().create(validated_data)
        try:
            # # create a notice for the test, which sends a mail to all relevant students
            # # requires request
            # utils.create_scoped_student_assessment_notice(self.request, assignment, _type="test")
            # create assignmenttaker instances for relevant students, registering them for the test
            utils.register_assessment_takers(assignment, _type="test")
        except Exception as e:
            print(f"An exception occurred while creating a notice or registering students: {e}")
        return assignment
    
    def update(self, instance, validated_data):
        assignment = super().update(instance, validated_data)
        try:
            # # create a notice for the test, which sends a mail to all relevant students
            # # requires request
            # utils.create_scoped_student_assessment_notice(self.request, assignment, _type="test")
            # create assignmenttaker instances for relevant students, registering them for the test
            utils.register_assessment_takers(assignment, _type="test")
        except Exception as e:
            print(f"An exception occurred while creating a notice or registering students: {e}")
        return assignment


class AssignmentTakerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the AssignmentTaker model"""

    # student = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    student = serializers.PrimaryKeyRelatedField(
        # queryset=get_user_model().objects.all(),
        queryset=umodels.Student.objects.all(),
        allow_null=True, required=False,
    )
    assignment = serializers.PrimaryKeyRelatedField(
        queryset=models.Assignment.objects.all(),
        allow_null=True, required=False,
    )
    grade = serializers.PrimaryKeyRelatedField(
        queryset=models.Grade.objects.all(),
        allow_null=True, required=False,
    )
    is_passed = serializers.ReadOnlyField()

    class Meta:
        model = models.AssignmentTaker
        fields = [
            'id',
            'url',
            'student',
            'assignment',
            'grade',
            'score',
            'is_passed',
            'completed',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:assignmenttaker-detail'}
        }
        
        
class AssignmentTakerResponseSerializer(AssignmentTakerSerializer):
    """serializer for the AssignmentTaker model"""

    assignment = AssignmentSerializer(read_only=True)
    grade = GradeSerializer(read_only=True)


class AssignmentResponseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the AssignmentResponse model"""

    assignment_taker = serializers.PrimaryKeyRelatedField(
        queryset=models.AssignmentTaker.objects.all(),
    )
    assignment = serializers.PrimaryKeyRelatedField(
        queryset=models.Assignment.objects.all(),
    )

    class Meta:
        model = models.AssignmentResponse
        fields = [
            'id',
            'url',
            'assignment_taker',
            'assignment',
            'answer',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:assignmentresponse-detail'}
        }


