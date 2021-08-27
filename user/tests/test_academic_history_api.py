from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers
from datetime import datetime


ACADEMIC_HISTORY_URL = reverse('user:academichistory-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def academic_history_detail_url(academic_history_id):
    """return url for the academic_history detail"""
    return reverse('user:academichistory-detail', args=[academic_history_id])


def sample_biodata(user, **kwargs):
    """create and return sample biodata"""
    return models.Biodata.objects.create(user=user, **kwargs)


def sample_academic_history(biodata, **kwargs):
    """create and return sample academic_history"""
    return models.AcademicHistory.objects.create(biodata=biodata, **kwargs)


# def sample_academic_history_image(academic_history, **kwargs):
#     """create and return a sample academic_history image"""
#     defaults = {
#         'description': 'sample academic_history image'
#     }
#     defaults.update(kwargs)
#     return models.AcademicHistoryImage.create(academic_history=academic_history, **defaults)



def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicAcademicHistoryApiTest(TestCase):
    """test public access to the academic_history api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(ACADEMIC_HISTORY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAcademicHistoryApiTest(TestCase):
    """test authenticated access to the academic_history api"""

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

    def test_retrieve_academic_history(self):
        """test retrieving a list of academic_history"""
        sample_academic_history(biodata=self.biodata)
        academic_history = models.AcademicHistory.objects.all()
        serializer = serializers.AcademicHistorySerializer(academic_history, many=True, context=serializer_context)

        res = self.client.get(ACADEMIC_HISTORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_academic_history_limited_to_user(self):
    #     """test that academic_histories are for a specified user and biodata """
    #     sample_academic_history(biodata=self.biodata)
    #     user2 = get_user_model().objects.create_user(
    #         'test2@test.com',
    #         'testpass2'
    #     )
    #     biodata2 = sample_biodata(user=user2)
    #     sample_academic_history(biodata=biodata2)

    #     academic_history = models.AcademicHistory.objects.all()
    #     serializer = serializers.AcademicHistorySerializer(academic_history, many=True, context=serializer_context)
        
    #     res = self.client.get(ACADEMIC_HISTORY_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
    #     self.assertEqual(len(res.data), 2)

    def test_retrieve_academic_history_detail(self):
        """test retrieving a academic_history's detail"""
        academic_history = sample_academic_history(biodata=self.biodata)
        serializer = serializers.AcademicHistorySerializer(academic_history, context=serializer_context)
        
        url = academic_history_detail_url(academic_history_id=academic_history.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_academic_history(self):
        """test creating a academic_history"""
        payload = {
            'biodata': self.serializer.data['url'],
            'start_date': datetime.today().strftime('%Y-%m-%d'),
        }

        res = self.client.post(ACADEMIC_HISTORY_URL, payload)

        academic_history = models.AcademicHistory.objects.get(id=res.data['id'])
        academic_history_serializer = serializers.AcademicHistorySerializer(academic_history, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, academic_history, academic_history_serializer)

    def test_partial_update_academic_history(self):
        """test partially updating a academic_history's detail using patch"""
        academic_history = sample_academic_history(biodata=self.biodata)

        payload = {
            # 'biodata': self.serializer.data['url'],
            'start_date': datetime.today().strftime('%Y-%m-%d'),
        }

        url = academic_history_detail_url(academic_history.id)
        res = self.client.patch(url, payload)

        academic_history.refresh_from_db()
        academic_history_serializer = serializers.AcademicHistorySerializer(academic_history, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, academic_history, academic_history_serializer)

    def test_full_update_academic_history(self):
        """test updating a academic_history's detail using put"""
        academic_history = sample_academic_history(biodata=self.biodata)
        
        payload = {
            'biodata': self.serializer.data['url'],
            'start_date': datetime.today().strftime('%Y-%m-%d'),
        }

        url = academic_history_detail_url(academic_history.id)
        res = self.client.put(url, payload)

        academic_history.refresh_from_db()
        academic_history_serializer = serializers.AcademicHistorySerializer(academic_history, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, academic_history, academic_history_serializer)
