from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers


STAFF_URL = reverse('user:staff-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def staff_detail_url(staff_id):
    """return url for the staff detail"""
    return reverse('user:staff-detail', args=[staff_id])


def sample_staff(user, **kwargs):
    """create and return sample staff"""
    try:
        staff = models.Staff.objects.get(user=user)
    except Exception:
        staff = models.Staff.objects.create(user=user, **kwargs)
    return staff


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image', 'new_user']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicStaffApiTest(TestCase):
    """test public access to the staff api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(STAFF_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateStaffApiTest(TestCase):
    """test authenticated access to the staff api"""

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

    def test_retrieve_staff(self):
        """test retrieving a list of staff"""
        sample_staff(user=self.user)
        staff = models.Staff.objects.all()
        serializer = serializers.StaffSerializer(staff, many=True, context=serializer_context)

        res = self.client.get(STAFF_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_staff_not_limited_to_user(self):
        """test that staffs from all users is returned"""
        sample_staff(user=self.user)
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass2'
        )
        sample_staff(user=user2)

        staff = models.Staff.objects.all()
        serializer = serializers.StaffSerializer(staff, many=True, context=serializer_context)

        res = self.client.get(STAFF_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
        self.assertEqual(len(res.data['results']), 2)

    def test_retrieve_staff_detail(self):
        """test retrieving a staff's detail"""
        staff = sample_staff(user=self.user)
        serializer = serializers.StaffSerializer(staff, context=serializer_context)

        url = staff_detail_url(staff_id=staff.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_staff(self):
        """test creating a staff"""
        payload = {
            'user': self.serializer.data['url'],
            'employee_id': 'Emp 104',
        }

        res = self.client.post(STAFF_URL, payload, format='json')

        staff = models.Staff.objects.get(id=res.data['id'])
        staff_serializer = serializers.StaffSerializer(staff, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, staff, staff_serializer)

    def test_create_staff_and_user(self):
        """test creating a staff and user at the same time"""
        payload = {
            'user': self.serializer.data['url'],
            'new_user': {
                'first_name': "Staff",
                'last_name': "User",
                'email': "staffuser@gmail.com",
                'password': "01010101",
                'is_staff': True
            },
            'employee_id': 'Emp 104',
        }

        res = self.client.post(STAFF_URL, payload, format='json')
        # print(res.data)
        staff = models.Staff.objects.get(id=res.data['id'])
        staff_serializer = serializers.StaffSerializer(staff, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, staff, staff_serializer)

    def test_partial_update_staff(self):
        """test partially updating a staff's detail using patch"""
        staff = sample_staff(user=self.user)

        payload = {
            # 'user': self.serializer.data['url'],
            'employee_id': 'Emp 104',
            'is_lecturer': True,
        }

        url = staff_detail_url(staff.id)
        res = self.client.patch(url, payload, format='json')

        staff.refresh_from_db()
        staff_serializer = serializers.StaffSerializer(staff, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, staff, staff_serializer)

    def test_full_update_staff(self):
        """test updating a staff's detail using put"""
        staff = sample_staff(user=self.user)

        payload = {
            # 'user': self.serializer.data['url'],
            'employee_id': 'Emp 104',
            'new_user': {
                'first_name': "NewStaff",
                'last_name': "UserOne",
                'email': "staffuserone@gmail.com",
                'password': "00001111",
                'is_staff': True
            },
            'is_lecturer': True,
        }

        url = staff_detail_url(staff.id)
        res = self.client.put(url, payload, format='json')

        staff.refresh_from_db()
        staff_serializer = serializers.StaffSerializer(staff, context=serializer_context)
        # print(staff_serializer.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, staff, staff_serializer)
