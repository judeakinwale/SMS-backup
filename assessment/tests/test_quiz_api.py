from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from assessment import models, serializers


QUIZ_URL = reverse('assessment:quiz-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def quiz_detail_url(quiz_id):
    """return url for the quiz detail"""
    return reverse('assessment:quiz-detail', args=[quiz_id])


def sample_quiz(supervisor, **kwargs):
    """create and return a sample quiz"""
    defaults = {'name': 'Sample Quiz'}
    defaults.update(kwargs)
    return models.Quiz.objects.create(supervisor=supervisor, **defaults)


# def sample_quiz_image(quiz, **kwargs):
#     """create and return a sample quiz image"""
#     defaults = {}
#     defaults.update(kwargs)
#     return models.QuizImage.create(quiz=quiz, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicQuizApiTest(TestCase):
    """test public access to the quiz api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(QUIZ_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateQuizApiTest(TestCase):
    """test authenticated access to the quiz api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        # self.quiz = sample_quiz(supervisor=self.user)

    def tearDown(self):
        pass

    def test_retrieve_quiz(self):
        """test retrieving a list of quizs"""
        sample_quiz(supervisor=self.user)
        quiz = models.Quiz.objects.all()
        serializer = serializers.QuizSerializer(quiz, many=True, context=serializer_context)

        res = self.client.get(QUIZ_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # # TODO:
    # def test_quiz_limited_to_supervisor(self):
    #     """test that quiz from a specified supervisor is returned"""
    #     sample_quiz(supervisor=self.user)
    #     user2 = get_user_model().objects.create_user(
    #         'test2@test.com',
    #         'testpass2'
    #     )
    #     quiz = sample_quiz(supervisor=user2, name='Test Quiz 3')

    #     quizzes = models.Quiz.objects.filter(supervisor=self.user)
    #     serializer = serializers.QuizSerializer(quizzes, many=True, context=serializer_context)
        
    #     res = self.client.get(QUIZ_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
    #     self.assertEqual(len(res.data), 1)

    # def test_retrieve_quiz_detail(self):
    #     """test retrieving a quiz's detail"""
    #     quiz = sample_quiz(supervisor=self.user)
    #     serializer = serializers.QuizSerializer(quiz, context=serializer_context)
        
    #     url = quiz_detail_url(quiz_id=quiz.id)
    #     res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_quiz(self):
        """test creating a quiz"""
        payload = {
            'supervisor': self.user.id,
            'name': 'Test name 2',
        }

        res = self.client.post(QUIZ_URL, payload)

        quiz = models.Quiz.objects.get(id=res.data['id'])
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, quiz, quiz_serializer)

    def test_partial_update_quiz(self):
        """test partially updating a quiz's detail using patch"""
        quiz = sample_quiz(supervisor=self.user)
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
        payload = {
            'supervisor': self.user.id,
            'name': 'An updated name'
        }

        url = quiz_detail_url(quiz.id)
        res = self.client.patch(url, payload)

        quiz.refresh_from_db()
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, quiz, quiz_serializer)

    def test_full_update_quiz(self):
        """test updating a quiz's detail using put"""
        quiz = sample_quiz(supervisor=self.user)
        payload = {
            'supervisor': self.user.id,
            'name': 'Test name 3',
        }

        url = quiz_detail_url(quiz.id)
        res = self.client.put(url, payload)

        quiz.refresh_from_db()
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, quiz, quiz_serializer)

    def test_create_quiz_with_questions(self):
        """test creating a quiz with questions attached"""
        payload = {
            'supervisor': self.user.id,
            'name': 'Test quiz 4',
            'question_set': [
                {'label': 'Test label 2',},
                {'label': 'Test label 3',},
            ],
        }

        res = self.client.post(QUIZ_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.data['question_set'], [])

    def test_create_quiz_with_questions_and_answers(self):
        """test creating a quiz with questions attached and answers attached to the questions"""
        payload = {
            'supervisor': self.user.id,
            'name': 'Test quiz 4',
            'question_set': [
                {
                    'label': 'Test label 2',
                    'answer_set': [
                        {'text': 'Question 1',},
                        {'text': 'Question 2',},
                        {'text': 'Question 3',},
                    ],
                },
                {
                    'label': 'Test label 3',
                    'answer_set': [
                        {'text': 'Question 1',},
                        {'text': 'Question 2',},
                        {'text': 'Question 3',},
                    ],
                },
            ],
        }

        res = self.client.post(QUIZ_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.data['question_set'], [])
        self.assertNotEqual(res.data['question_set'][0]['answer_set'], [])

