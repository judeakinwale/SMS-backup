from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers


BIODATA_URL = reverse('user:biodata-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def biodata_detail_url(biodata_id):
    """return url for the biodata detail"""
    return reverse('user:biodata-detail', args=[biodata_id])


def sample_biodata(user, **kwargs):
    """create and return sample biodata"""
    return models.Biodata.objects.create(user=user, **kwargs)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicBiodataApiTest(TestCase):
    """test public access to the biodata api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(BIODATA_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateBiodataApiTest(TestCase):
    """test authenticated access to the biodata api"""

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

    def test_retrieve_biodata(self):
        """test retrieving a list of biodata"""
        sample_biodata(user=self.user)
        biodata = models.Biodata.objects.all()
        serializer = serializers.BiodataSerializer(biodata, many=True, context=serializer_context)

        res = self.client.get(BIODATA_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_biodata_not_limited_to_user(self):
        """test that biodatas from all users is returned"""
        sample_biodata(user=self.user)
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass2'
        )
        sample_biodata(user=user2)

        biodata = models.Biodata.objects.all()
        serializer = serializers.BiodataSerializer(biodata, many=True, context=serializer_context)

        res = self.client.get(BIODATA_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
        self.assertEqual(len(res.data['results']), 2)

    def test_retrieve_biodata_detail(self):
        """test retrieving a biodata's detail"""
        biodata = sample_biodata(user=self.user)
        serializer = serializers.BiodataSerializer(biodata, context=serializer_context)

        url = biodata_detail_url(biodata_id=biodata.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_biodata(self):
        """test creating a biodata"""
        payload = {
            'user': self.serializer.data['url'],
        }

        res = self.client.post(BIODATA_URL, payload)

        biodata = models.Biodata.objects.get(id=res.data['id'])
        biodata_serializer = serializers.BiodataSerializer(biodata, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, biodata, biodata_serializer)

    def test_partial_update_biodata(self):
        """test partially updating a biodata's detail using patch"""
        biodata = sample_biodata(user=self.user)

        payload = {
            # 'user': self.serializer.data['url'],
            'phone_no_1': '012347893',
        }

        url = biodata_detail_url(biodata.id)
        res = self.client.patch(url, payload)

        biodata.refresh_from_db()
        biodata_serializer = serializers.BiodataSerializer(biodata, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, biodata, biodata_serializer)

    def test_full_update_biodata(self):
        """test updating a biodata's detail using put"""
        biodata = sample_biodata(user=self.user)

        payload = {
            'user': self.serializer.data['url'],
        }

        url = biodata_detail_url(biodata.id)
        res = self.client.put(url, payload)

        biodata.refresh_from_db()
        biodata_serializer = serializers.BiodataSerializer(biodata, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, biodata, biodata_serializer)
