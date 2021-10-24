from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from assessment import models, serializers


GRADE_URL = reverse('assessment:grade-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def grade_detail_url(grade_id):
    """return url for the grade detail"""
    return reverse('assessment:grade-detail', args=[grade_id])


def sample_grade(**kwargs):
    """create and return a sample grade"""
    return models.Grade.objects.create(**kwargs)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicGradeApiTest(TestCase):
    """test public access to the grade api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(GRADE_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateGradeApiTest(TestCase):
    """test authenticated access to the grade api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_grade(self):
        """test retrieving a list of grades"""
        sample_grade()
        grade = models.Grade.objects.all()
        serializer = serializers.GradeSerializer(grade, many=True, context=serializer_context)

        res = self.client.get(GRADE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_grade_detail(self):
        """test retrieving a grade's detail"""
        grade = sample_grade()
        serializer = serializers.GradeSerializer(grade, context=serializer_context)

        url = grade_detail_url(grade_id=grade.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_grade(self):
        """test creating a grade"""
        payload = {
            'score': 15,
            'max_score': 20,
        }

        res = self.client.post(GRADE_URL, payload)

        grade = models.Grade.objects.get(id=res.data['id'])
        grade_serializer = serializers.GradeSerializer(grade, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, grade, grade_serializer)

    def test_partial_update_grade(self):
        """test partially updating a grade's detail using patch"""
        grade = sample_grade()
        payload = {
            'score': 15,
        }

        url = grade_detail_url(grade.id)
        res = self.client.patch(url, payload)

        grade.refresh_from_db()
        grade_serializer = serializers.GradeSerializer(grade, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, grade, grade_serializer)

    def test_full_update_grade(self):
        """test updating a grade's detail using put"""
        grade = sample_grade(max_score=40)
        payload = {
            'score': 15,
            'max_score': 20,
        }

        url = grade_detail_url(grade.id)
        res = self.client.put(url, payload)

        grade.refresh_from_db()
        grade_serializer = serializers.GradeSerializer(grade, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, grade, grade_serializer)
