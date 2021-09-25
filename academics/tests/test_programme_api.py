from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


SPECIALIZATION_URL = reverse('academics:specialization-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def specialization_detail_url(specialization_id):
    """return url for the specialization detail"""
    return reverse('academics:specialization-detail', args=[specialization_id])


def sample_faculty(**kwargs):
    """create and return a sample faculty"""
    defaults = {'name': 'Faculty 1'}
    defaults.update(kwargs)
    return models.Faculty.objects.create(**defaults)


def sample_department(faculty, **kwargs):
    """create and return a sample department"""
    defaults = {'name': 'Department 1'}
    defaults.update(kwargs)
    return models.Department.objects.create(faculty=faculty, **defaults)


def sample_level(**kwargs):
    """create and return a sample level"""
    defaults = {'code': 100}
    defaults.update(**kwargs)
    return models.Level.objects.create(**defaults)


def sample_specialization(department, max_level, **kwargs):
    """create and return a sample specialization"""
    defaults = {
        'name': 'Specialization 1',
        'max_level': max_level,
    }
    defaults.update(kwargs)
    return models.Specialization.objects.create(department=department, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicSpecializationApiTest(TestCase):
    """test public access to the specialization api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(SPECIALIZATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSpecializationApiTest(TestCase):
    """test authenticated access to the specialization api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.faculty = sample_faculty()
        self.department = sample_department(faculty=self.faculty)
        self.level = sample_level()

    def test_retrieve_specialization(self):
        """test retrieving a list of specializations"""
        sample_specialization(department=self.department, max_level=self.level)
        specialization = models.Specialization.objects.all()
        serializer = serializers.SpecializationSerializer(
            specialization,
            many=True,
            context=serializer_context
        )

        res = self.client.get(SPECIALIZATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_specialization_detail(self):
        """test retrieving a specialization's detail"""
        specialization = sample_specialization(department=self.department, max_level=self.level)
        serializer = serializers.SpecializationSerializer(specialization, context=serializer_context)

        url = specialization_detail_url(specialization_id=specialization.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_specialization(self):
        """test creating a specialization"""
        department = sample_department(faculty=self.faculty, name='Department 2')
        department_serializer = serializers.DepartmentSerializer(department, context=serializer_context)
        level_serializer = serializers.LevelSerializer(self.level, context=serializer_context)
        payload = {
            'department': department_serializer.data['url'],
            'name': 'Specialization 2',
            'max_level': level_serializer.data['url'],
            'description': 'some description text',
        }

        res = self.client.post(SPECIALIZATION_URL, payload)

        specialization = models.Specialization.objects.get(id=res.data['id'])
        specialization_serializer = serializers.SpecializationSerializer(
            specialization,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, specialization, specialization_serializer)

    def test_partial_update_specialization(self):
        """test partially updating a specialization's detail using patch"""
        specialization = sample_specialization(department=self.department, max_level=self.level)
        payload = {
            'description': 'some description text',
        }

        url = specialization_detail_url(specialization.id)
        res = self.client.patch(url, payload)

        specialization.refresh_from_db()
        specialization_serializer = serializers.SpecializationSerializer(
            specialization,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, specialization, specialization_serializer)

    def test_full_update_specialization(self):
        """test updating a specialization's detail using put"""
        specialization = sample_specialization(department=self.department, max_level=self.level)
        department = sample_department(faculty=self.faculty, name='Department 3')
        department_serializer = serializers.DepartmentSerializer(department, context=serializer_context)
        level_serializer = serializers.LevelSerializer(self.level, context=serializer_context)
        payload = {
            'department': department_serializer.data['url'],
            'name': 'Specialization 3',
            'max_level': level_serializer.data['url'],
            'description': 'some description text',
        }

        url = specialization_detail_url(specialization.id)
        res = self.client.put(url, payload)

        specialization.refresh_from_db()
        specialization_serializer = serializers.SpecializationSerializer(
            specialization,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, specialization, specialization_serializer)
