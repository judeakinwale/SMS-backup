from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from assessment import models, serializers


QUESTION_URL = reverse('assessment:question-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def question_detail_url(question_id):
    """return url for the question detail"""
    return reverse('assessment:question-detail', args=[question_id])


def sample_quiz(supervisor, **kwargs):
    """create and return a sample quiz"""
    defaults = {'name': 'Sample Quiz'}
    defaults.update(kwargs)
    return models.Quiz.objects.create(supervisor=supervisor, **defaults)


def sample_question(quiz, **kwargs):
    """create and return a sample question"""
    defaults = {'label': 'Sample Question Label'}
    defaults.update(kwargs)
    return models.Question.objects.create(quiz=quiz, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicQuestionApiTest(TestCase):
    """test public access to the question api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(QUESTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQuestionApiTest(TestCase):
    """test authenticated access to the question api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.quiz = sample_quiz(supervisor=self.user)

    def tearDown(self):
        pass

    def test_retrieve_question(self):
        """test retrieving a list of questions"""
        sample_question(quiz=self.quiz)
        question = models.Question.objects.all()
        serializer = serializers.QuestionSerializer(question, many=True, context=serializer_context)

        res = self.client.get(QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    # # TODO:
    # def test_question_limited_to_quiz(self):
    #     """test that question from a specified quiz is returned"""
    #     pass

    def test_retrieve_question_detail(self):
        """test retrieving a question's detail"""
        question = sample_question(quiz=self.quiz)
        serializer = serializers.QuestionSerializer(question, context=serializer_context)

        url = question_detail_url(question_id=question.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_question(self):
        """test creating a question"""
        quiz_serializer = serializers.QuizSerializer(self.quiz, context=serializer_context)
        payload = {
            'quiz': quiz_serializer.data['url'],
            'label': 'Test label 2',
        }

        res = self.client.post(QUESTION_URL, payload)

        question = models.Question.objects.get(id=res.data['id'])
        question_serializer = serializers.QuestionSerializer(question, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, question, question_serializer)

    def test_partial_update_question(self):
        """test partially updating a question's detail using patch"""
        question = sample_question(quiz=self.quiz)
        quiz = sample_quiz(supervisor=self.user)
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
        payload = {
            'quiz': quiz_serializer.data['url'],
            'label': 'An updated label'
        }

        url = question_detail_url(question.id)
        res = self.client.patch(url, payload)

        question.refresh_from_db()
        question_serializer = serializers.QuestionSerializer(question, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, question, question_serializer)

    def test_full_update_question(self):
        """test updating a question's detail using put"""
        question = sample_question(quiz=self.quiz, label='label2')
        quiz = sample_quiz(supervisor=self.user)
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
        payload = {
            'quiz': quiz_serializer.data['url'],
            'label': 'Test label 3',
            'order': 1,
        }

        url = question_detail_url(question.id)
        res = self.client.put(url, payload)

        question.refresh_from_db()
        question_serializer = serializers.QuestionSerializer(question, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, question, question_serializer)

    def test_create_question_with_answers(self):
        """test creating a question with answers attached"""
        quiz = sample_quiz(supervisor=self.user)
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
        payload = {
            'quiz': quiz_serializer.data['url'],
            'label': 'Test label 3',
            'answer_set': [
                {'text': 'Question 1', },
                {'text': 'Question 2', },
                {'text': 'Question 3', },
            ],
        }

        res = self.client.post(QUESTION_URL, payload, format='json')

        models.Question.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.data['answer_set'], [])

    def test_partial_update_question_with_questions_and_answers(self):
        """test updating a question with answers attached using patch"""
        question = sample_question(quiz=self.quiz)
        payload = {
            'label': 'Test Question 2',
            'answer_set': [
                {'text': 'Answer 1', },
                {'text': 'Answer 2', },
                {'text': 'Answer 3', },
            ],
        }

        url = question_detail_url(question.id)
        res = self.client.patch(url, payload, format='json')

        question.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data['answer_set'], [])
        # self.assertNotEqual(res.data['question_set'][0]['answer_set'], [])

    def test_full_update_question_with_questions_and_answers(self):
        """test updating a question with answers attached using put"""
        question = sample_question(quiz=self.quiz, label='label2')
        quiz = sample_quiz(supervisor=self.user)
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
        payload = {
            'quiz': quiz_serializer.data['url'],
            'label': 'Test Question 3',
            'answer_set': [
                {'text': 'Answer 1', },
                {'text': 'Answer 2', },
                {'text': 'Answer 3', },
            ],
        }

        url = question_detail_url(question.id)
        res = self.client.put(url, payload, format='json')

        question.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data['answer_set'], [])
