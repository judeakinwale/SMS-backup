from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user import models


CREATE_USER_URL = reverse('user:user-list')
TOKEN_URL = reverse('user:token_obtain_pair')
ACCOUNT_URL = reverse('user:account')


def user_detail_url(user_id):
    """url for a user detail view"""
    return reverse('user:user-detail', args=[user_id])


def sample_biodata(user, **kwargs):
    """create and return sample biodata"""
    return models.Biodata.objects.create(user=user, **kwargs)


class PublicUserApiTests(TestCase):
    """test the user api (public)"""

    def setUp(self):
        self.client = APIClient()
        self.payload_full = {
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'testpass',
        }
        self.payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123',
        }

    def test_create_token_for_users(self):
        """test that a token is created for the user"""
        get_user_model().objects.create_user(**self.payload)
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """test that a token is not created if invalid credentials are provided"""
        get_user_model().objects.create_user(**self.payload)
        payload = self.payload
        payload['password'] = 'wrongpass'
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        """test token is not created if user does not exist"""
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_field(self):
        """test email and password are required to generate a token"""
        res = self.client.post(TOKEN_URL, {'email': 'ma@il.co', 'password': ''})

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_users_unauthorized(self):
        """test that authentication is required to view user details"""
        res = self.client.get(ACCOUNT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """test the user api requests that require authentication"""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email='testuser@gmail.com',
            password='testuserpass',
            first_name='test',
            last_name='user 2',
        )
        self.payload_full = {
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'testpass',
        }
        self.payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123',
        }
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_Valid_user_sucess(self):
        """test creating a user with a valid payload is successful"""
        payload = {
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'testpass',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        # print("\n1\n")
        # print(res.data)

        user = get_user_model().objects.get(id=res.data['id'], email=res.data['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_retrieve_profile_successful(self):
        """test retrieving the account page for an authenticated user"""
        res = self.client.get(ACCOUNT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['first_name'], self.user.first_name)
        self.assertEqual(res.data['last_name'], self.user.last_name)
        self.assertEqual(res.data['email'], self.user.email)

    def test_create_existing_user_fails(self):
        """test creating a user that already exists fails"""
        get_user_model().objects.create_user(**self.payload_full)
        res = self.client.post(CREATE_USER_URL, self.payload_full)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test creating new user fails if password is not more than 5 characters"""
        payload = self.payload_full
        payload['password'] = 'pw'

        res = self.client.post(CREATE_USER_URL, payload)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_post_account_not_allowed(self):
        """test that POST is not allowed on the account url"""
        res = self.client.post(ACCOUNT_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test updating the user profile for an authenticated user"""
        payload = {
            'first_name': 'name 2',
            'last_name': 'new',
            'password': 'newpass123',
        }
        res = self.client.patch(ACCOUNT_URL, payload)
        # print(res.data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_with_attached_biodata(self):
        """test creating a user with a biodata attached"""
        payload = {
            'email': 'test@gmail.com',
            'first_name': 'name 3',
            'last_name': 'user',
            'password': 'testpass',
            'biodata': {
                'phone_no_1': '01234765',
            },
        }

        res = self.client.post(CREATE_USER_URL, payload, format='json')

        user = get_user_model().objects.get(id=res.data['id'], email=res.data['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertNotEqual(res.data['biodata'], [])

    def test_partial_update_user_with_attached_biodata(self):
        """test updating a user with a biodata attached using patch"""
        user = get_user_model().objects.create_user(**self.payload_full)
        payload = {
            'first_name': 'test',
            'last_name': 'user',
            'password': 'testpass',
            'biodata': {
                'phone_no_1': '01234765',
            },
        }

        url = user_detail_url(user.id)
        res = self.client.patch(url, payload, format='json')
        # print("update using patch")
        # print(res.data)

        user.refresh_from_db()
        self.assertEqual(user.first_name, payload['first_name'])
        self.assertEqual(user.last_name, payload['last_name'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res.data)
        self.assertNotEqual(res.data['biodata'], [])

    def test_full_update_user_with_attached_biodata(self):
        """test updating a user with a biodata attached using put"""
        user = get_user_model().objects.create_user(**self.payload_full)
        biodata = sample_biodata(user)
        payload = {
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'testpass',
            'biodata': {
                'phone_no_1': '01234765',
            },
        }

        url = user_detail_url(user.id)
        res = self.client.put(url, payload, format='json')
        # print("update using put")
        # print(res.data)

        user.refresh_from_db()
        self.assertEqual(user.first_name, payload['first_name'])
        self.assertEqual(user.last_name, payload['last_name'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res.data)
        self.assertNotEqual(res.data['biodata'], [])
