from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers
from datetime import datetime


FAMILY_DATA_URL = reverse('user:familydata-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def family_data_detail_url(family_data_id):
    """return url for the family_data detail"""
    return reverse('user:familydata-detail', args=[family_data_id])


def sample_biodata(user, **kwargs):
    """create and return sample biodata"""
    return models.Biodata.objects.create(user=user, **kwargs)


def sample_family_data(biodata, **kwargs):
    """create and return sample family_data"""
    return models.FamilyData.objects.create(biodata=biodata, **kwargs)


# def sample_family_data_image(family_data, **kwargs):
#     """create and return a sample family_data image"""
#     defaults = {
#         'description': 'sample family_data image'
#     }
#     defaults.update(kwargs)
#     return models.FamilyDataImage.create(family_data=family_data, **defaults)



def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicFamilyDataApiTest(TestCase):
    """test public access to the family_data api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(FAMILY_DATA_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateFamilyDataApiTest(TestCase):
    """test authenticated access to the family_data api"""

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

    def test_retrieve_family_data(self):
        """test retrieving a list of family_data"""
        sample_family_data(biodata=self.biodata)
        family_data = models.FamilyData.objects.all()
        serializer = serializers.FamilyDataSerializer(family_data, many=True, context=serializer_context)

        res = self.client.get(FAMILY_DATA_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_family_data_limited_to_user(self):
    #     """test that academic_histories are for a specified user and biodata """
    #     sample_family_data(biodata=self.biodata)
    #     user2 = get_user_model().objects.create_user(
    #         'test2@test.com',
    #         'testpass2'
    #     )
    #     biodata2 = sample_biodata(user=user2)
    #     sample_family_data(biodata=biodata2)

    #     family_data = models.FamilyData.objects.all()
    #     serializer = serializers.FamilyDataSerializer(family_data, many=True, context=serializer_context)
        
    #     res = self.client.get(FAMILY_DATA_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
    #     self.assertEqual(len(res.data), 2)

    def test_retrieve_family_data_detail(self):
        """test retrieving a family_data's detail"""
        family_data = sample_family_data(biodata=self.biodata)
        serializer = serializers.FamilyDataSerializer(family_data, context=serializer_context)
        
        url = family_data_detail_url(family_data_id=family_data.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_family_data(self):
        """test creating a family_data"""
        payload = {
            'biodata': self.serializer.data['url'],
            'guardian_full_name': 'Test Guardian',
        }

        res = self.client.post(FAMILY_DATA_URL, payload)

        family_data = models.FamilyData.objects.get(id=res.data['id'])
        family_data_serializer = serializers.FamilyDataSerializer(family_data, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, family_data, family_data_serializer)

    def test_partial_update_family_data(self):
        """test partially updating a family_data's detail using patch"""
        family_data = sample_family_data(biodata=self.biodata)

        payload = {
            # 'biodata': self.serializer.data['url'],
            'guardian_full_name': 'Test Guardian',
        }

        url = family_data_detail_url(family_data.id)
        res = self.client.patch(url, payload)

        family_data.refresh_from_db()
        family_data_serializer = serializers.FamilyDataSerializer(family_data, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, family_data, family_data_serializer)

    def test_full_update_family_data(self):
        """test updating a family_data's detail using put"""
        family_data = sample_family_data(biodata=self.biodata)
        
        payload = {
            'biodata': self.serializer.data['url'],
            'guardian_full_name': 'Test Guardian',
        }

        url = family_data_detail_url(family_data.id)
        res = self.client.put(url, payload)

        family_data.refresh_from_db()
        family_data_serializer = serializers.FamilyDataSerializer(family_data, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, family_data, family_data_serializer)
