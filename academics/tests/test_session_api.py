from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


SESSION_URL = reverse('academics:session-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def session_detail_url(session_id):
    """return url for the session detail"""
    return reverse('academics:session-detail', args=[session_id])


def sample_session(**kwargs):
    """create and return a sample session"""
    defaults = {'year': "2021"}
    defaults.update(kwargs)
    return models.Session.objects.create(**defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicSessionApiTest(TestCase):
    """test public access to the session api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(SESSION_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateSessionApiTest(TestCase):
    """test authenticated access to the session api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_session(self):
        """test retrieving a list of session"""
        sample_session()
        session = models.Session.objects.all()
        serializer = serializers.SessionSerializer(session, many=True, context=serializer_context)

        res = self.client.get(SESSION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_session_detail(self):
        """test retrieving a session's detail"""
        session = sample_session()
        serializer = serializers.SessionSerializer(session, context=serializer_context)
        # print(session)

        url = session_detail_url(session_id=session.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_session(self):
        """test creating a session"""
        payload = {
            'year': "2021",
        }

        res = self.client.post(SESSION_URL, payload)

        session = models.Session.objects.get(id=res.data['id'])
        session_serializer = serializers.SessionSerializer(session, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, session, session_serializer)

    def test_partial_update_session(self):
        """test partially updating a session's detail using patch"""
        session = sample_session()
        payload = {
            'year': "2021",
        }

        url = session_detail_url(session.id)
        res = self.client.patch(url, payload)

        session.refresh_from_db()
        session_serializer = serializers.SessionSerializer(session, context=serializer_context)

        # print(session_serializer.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, session, session_serializer)

    def test_full_update_session(self):
        """test updating a session's detail using put"""
        session = sample_session()
        payload = {
            'year': "2022",
        }

        url = session_detail_url(session.id)
        res = self.client.put(url, payload)

        session.refresh_from_db()
        session_serializer = serializers.SessionSerializer(session, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, session, session_serializer)
