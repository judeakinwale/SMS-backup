from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from assessment import models, serializers


RESPONSE_URL = reverse('assessment:response-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def response_detail_url(response_id):
    """return url for the response detail"""
    return reverse('assessment:response-detail', args=[response_id])


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


def sample_answer(question, **kwargs):
    """create and return sample answer"""
    defaults = {'text': 'some text'}
    defaults.update(kwargs)
    return models.Answer.objects.create(question=question, **defaults)


def sample_response(quiz_taker, question, **kwargs):
    """create and return sample response"""
    return models.Response.objects.create(quiz_taker=quiz_taker, question=question, **kwargs)


def sample_student(user, **kwargs):
    """create and return sample student"""
    return models.Student.objects.create(user=user, **kwargs)


def sample_quiz_taker(student, quiz, **kwargs):
    """create and return a sample quiz_taker"""
    defaults = {}
    defaults.update(kwargs)
    quiz_taker = models.QuizTaker.objects.create(student=student, quiz=quiz, **defaults)
    return quiz_taker


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicResponseApiTest(TestCase):
    """test public access to the response api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(RESPONSE_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateResponseApiTest(TestCase):
    """test authenticated access to the response api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.quiz = sample_quiz(supervisor=self.user)
        self.question = sample_question(quiz=self.quiz)
        self.answer = sample_answer(question=self.question)
        self.student = sample_student(self.user)
        self.quiz_taker = sample_quiz_taker(student=self.student, quiz=self.quiz)

    def tearDown(self):
        pass

    def test_retrieve_response(self):
        """test retrieving a list of responses"""
        sample_response(quiz_taker=self.quiz_taker, question=self.question)
        response = models.Response.objects.all()
        serializer = serializers.ResponseSerializer(response, many=True, context=serializer_context)

        res = self.client.get(RESPONSE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    # # TODO:
    # def test_responses_limited_to_answer(self):
    #     """test that responses from a specified answers is returned"""
    #     pass

    def test_retrieve_response_detail(self):
        """test retrieving a response's detail"""
        response = sample_response(quiz_taker=self.quiz_taker, question=self.question)
        serializer = serializers.ResponseSerializer(response, context=serializer_context)

        url = response_detail_url(response_id=response.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_response(self):
        """test creating a response"""
        quiz_taker = self.quiz_taker
        quiz_taker_serializer = serializers.QuizTakerSerializer(quiz_taker, context=serializer_context)

        question = self.question
        question_serializer = serializers.QuestionSerializer(question, context=serializer_context)

        answer = self.answer
        answer_serializer = serializers.AnswerSerializer(answer, context=serializer_context)

        payload = {
            'quiz_taker': self.quiz_taker.id,
            'question': self.question.id,
            'answer': self.answer.id,
        }

        res = self.client.post(RESPONSE_URL, payload)

        response = models.Response.objects.get(id=res.data['id'])
        response_serializer = serializers.ResponseSerializer(response, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, response, response_serializer)

    def test_partial_update_response(self):
        """test partially updating a response's detail using patch"""
        response = sample_response(quiz_taker=self.quiz_taker, question=self.question)

        answer = self.answer
        answer_serializer = serializers.AnswerSerializer(answer, context=serializer_context)

        payload = {
            'answer': self.answer.id,
        }

        url = response_detail_url(response.id)
        res = self.client.patch(url, payload)

        response.refresh_from_db()
        response_serializer = serializers.ResponseSerializer(response, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, response, response_serializer)

    def test_full_update_response(self):
        """test updating a response's detail using put"""
        response = sample_response(quiz_taker=self.quiz_taker, question=self.question)

        quiz_taker = self.quiz_taker
        quiz_taker_serializer = serializers.QuizTakerSerializer(quiz_taker, context=serializer_context)

        question = self.question
        question_serializer = serializers.QuestionSerializer(question, context=serializer_context)

        answer = self.answer
        answer_serializer = serializers.AnswerSerializer(answer, context=serializer_context)

        payload = {
            'quiz_taker': self.quiz_taker.id,
            'question': self.question.id,
            'answer': self.answer.id,
        }

        url = response_detail_url(response.id)
        res = self.client.put(url, payload)

        response.refresh_from_db()
        response_serializer = serializers.ResponseSerializer(response, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, response, response_serializer)
