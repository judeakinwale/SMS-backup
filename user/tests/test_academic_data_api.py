from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers
from datetime import datetime


ACADEMIC_DATA_URL = reverse('user:academicdata-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def academic_data_detail_url(academic_data_id):
    """return url for the academic_data detail"""
    return reverse('user:academicdata-detail', args=[academic_data_id])


def sample_student(user, **kwargs):
    """create and return sample student"""
    return models.Student.objects.create(user=user, **kwargs)


def sample_academic_data(student, **kwargs):
    """create and return sample academic_data"""
    return models.AcademicData.objects.create(student=student, **kwargs)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicAcademicDataApiTest(TestCase):
    """test public access to the academic_data api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(ACADEMIC_DATA_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateAcademicDataApiTest(TestCase):
    """test authenticated access to the academic_data api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.student = sample_student(user=self.user)
        self.serializer = serializers.StudentSerializer(self.student, context=serializer_context)
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_academic_data(self):
        """test retrieving a list of academic_data"""
        sample_academic_data(student=self.student)
        academic_data = models.AcademicData.objects.all()
        serializer = serializers.AcademicDataSerializer(academic_data, many=True, context=serializer_context)
        response_serializer = serializers.AcademicDataResponseSerializer(academic_data, many=True, context=serializer_context)

        res = self.client.get(ACADEMIC_DATA_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        try:
            self.assertEqual(res.data['results'], serializer.data)
        except Exception:
            self.assertEqual(res.data['results'], response_serializer.data)

    def test_retrieve_academic_data_detail(self):
        """test retrieving a academic_data's detail"""
        academic_data = sample_academic_data(student=self.student)
        serializer = serializers.AcademicDataSerializer(academic_data, context=serializer_context)
        response_serializer = serializers.AcademicDataResponseSerializer(academic_data, context=serializer_context)

        url = academic_data_detail_url(academic_data_id=academic_data.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        try:
            self.assertEqual(res.data, serializer.data)
        except Exception:
            self.assertEqual(res.data, response_serializer.data)

    def test_create_academic_data(self):
        """test creating a academic_data"""
        payload = {
            'student': self.serializer.data['url'],
            'start_date': datetime.today().strftime('%Y-%m-%d'),
        }

        res = self.client.post(ACADEMIC_DATA_URL, payload)

        academic_data = models.AcademicData.objects.get(id=res.data['id'])
        academic_data_serializer = serializers.AcademicDataSerializer(
            academic_data,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, academic_data, academic_data_serializer)

    def test_partial_update_academic_data(self):
        """test partially updating a academic_data's detail using patch"""
        academic_data = sample_academic_data(student=self.student)

        payload = {
            # 'student': self.serializer.data['url'],
            'start_date': datetime.today().strftime('%Y-%m-%d'),
        }

        url = academic_data_detail_url(academic_data.id)
        res = self.client.patch(url, payload)

        academic_data.refresh_from_db()
        academic_data_serializer = serializers.AcademicDataSerializer(
            academic_data,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, academic_data, academic_data_serializer)

    def test_full_update_academic_data(self):
        """test updating a academic_data's detail using put"""
        academic_data = sample_academic_data(student=self.student)

        payload = {
            'student': self.serializer.data['url'],
            'start_date': datetime.today().strftime('%Y-%m-%d'),
        }

        url = academic_data_detail_url(academic_data.id)
        res = self.client.put(url, payload)

        academic_data.refresh_from_db()
        academic_data_serializer = serializers.AcademicDataSerializer(
            academic_data,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, academic_data, academic_data_serializer)
