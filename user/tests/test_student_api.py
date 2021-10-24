from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers


STUDENT_URL = reverse('user:student-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def student_detail_url(student_id):
    """return url for the student detail"""
    return reverse('user:student-detail', args=[student_id])


def sample_student(user, **kwargs):
    """create and return sample student"""
    return models.Student.objects.create(user=user, **kwargs)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicStudentApiTest(TestCase):
    """test public access to the student api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_not_required(self):
        """test that authentication is required"""
        res = self.client.get(STUDENT_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateStudentApiTest(TestCase):
    """test authenticated access to the student api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.serializer = serializers.UserSerializer(self.user, context=serializer_context)
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_student(self):
        """test retrieving a list of student"""
        sample_student(user=self.user)
        student = models.Student.objects.all()
        serializer = serializers.StudentSerializer(student, many=True, context=serializer_context)

        res = self.client.get(STUDENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_student_not_limited_to_user(self):
        """test that students from all users is returned"""
        sample_student(user=self.user)
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass2'
        )
        sample_student(user=user2)

        student = models.Student.objects.all()
        serializer = serializers.StudentSerializer(student, many=True, context=serializer_context)

        res = self.client.get(STUDENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
        self.assertEqual(len(res.data['results']), 2)

    def test_retrieve_student_detail(self):
        """test retrieving a student's detail"""
        student = sample_student(user=self.user)
        serializer = serializers.StudentSerializer(student, context=serializer_context)

        url = student_detail_url(student_id=student.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_student(self):
        """test creating a student"""
        payload = {
            'user': self.serializer.data['url'],
            'student_id': 'S 1034',
        }

        res = self.client.post(STUDENT_URL, payload)

        student = models.Student.objects.get(id=res.data['id'])
        student_serializer = serializers.StudentSerializer(student, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, student, student_serializer)

    def test_partial_update_student(self):
        """test partially updating a student's detail using patch"""
        student = sample_student(user=self.user)

        payload = {
            'student_id': 'S 1034',
        }

        url = student_detail_url(student.id)
        res = self.client.patch(url, payload)

        student.refresh_from_db()
        student_serializer = serializers.StudentSerializer(student, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, student, student_serializer)

    def test_full_update_student(self):
        """test updating a student's detail using put"""
        student = sample_student(user=self.user)

        payload = {
            'user': self.serializer.data['url'],
            'student_id': 'S 1034',
        }

        url = student_detail_url(student.id)
        res = self.client.put(url, payload)

        student.refresh_from_db()
        student_serializer = serializers.StudentSerializer(student, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, student, student_serializer)
