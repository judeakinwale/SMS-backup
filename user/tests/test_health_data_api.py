from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers


HEALTH_DATA_URL = reverse('user:healthdata-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def health_data_detail_url(health_data_id):
    """return url for the health_data detail"""
    return reverse('user:healthdata-detail', args=[health_data_id])


def sample_biodata(user, **kwargs):
    """create and return sample biodata"""
    return models.Biodata.objects.create(user=user, **kwargs)


def sample_health_data(biodata, **kwargs):
    """create and return sample health_data"""
    return models.HealthData.objects.create(biodata=biodata, **kwargs)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicHealthDataApiTest(TestCase):
    """test public access to the health_data api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(HEALTH_DATA_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHealthDataApiTest(TestCase):
    """test authenticated access to the health_data api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.biodata = sample_biodata(user=self.user)
        self.serializer = serializers.BiodataSerializer(self.biodata, context=serializer_context)
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_health_data(self):
        """test retrieving a list of health_data"""
        sample_health_data(biodata=self.biodata)
        health_data = models.HealthData.objects.all()
        serializer = serializers.HealthDataSerializer(health_data, many=True, context=serializer_context)

        res = self.client.get(HEALTH_DATA_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_health_data_detail(self):
        """test retrieving a health_data's detail"""
        health_data = sample_health_data(biodata=self.biodata)
        serializer = serializers.HealthDataSerializer(health_data, context=serializer_context)

        url = health_data_detail_url(health_data_id=health_data.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_health_data(self):
        """test creating a health_data"""
        payload = {
            'biodata': self.serializer.data['url'],
            'diabetes': True,
        }

        res = self.client.post(HEALTH_DATA_URL, payload)

        health_data = models.HealthData.objects.get(id=res.data['id'])
        health_data_serializer = serializers.HealthDataSerializer(health_data, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, health_data, health_data_serializer)

    def test_partial_update_health_data(self):
        """test partially updating a health_data's detail using patch"""
        health_data = sample_health_data(biodata=self.biodata)

        payload = {
            'diabetes': True,
        }

        url = health_data_detail_url(health_data.id)
        res = self.client.patch(url, payload)

        health_data.refresh_from_db()
        health_data_serializer = serializers.HealthDataSerializer(health_data, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, health_data, health_data_serializer)

    def test_full_update_health_data(self):
        """test updating a health_data's detail using put"""
        health_data = sample_health_data(biodata=self.biodata)

        payload = {
            'biodata': self.serializer.data['url'],
            'diabetes': True,
        }

        url = health_data_detail_url(health_data.id)
        res = self.client.put(url, payload)

        health_data.refresh_from_db()
        health_data_serializer = serializers.HealthDataSerializer(health_data, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, health_data, health_data_serializer)
