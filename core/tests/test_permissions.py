from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from core import permissions
from user import models as umodels
import user


CREATE_USER_URL = reverse('user:user-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}



class PermissionTest(TestCase):
    """Test custom permissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_payload = {
            'email': 'staff@email.com',
            'password': '00000000',
        }
        self.staff_payload = {
            'email': 'staff@email.com',
            'password': '00000000',
            'is_staff': True,
        }
        self.superuser_payload = {
            'email': 'staff@email.com',
            'password': '00000000',
            'is_staff': True,
            'is_superuser': True,
        }
        self.superuser = get_user_model().objects.create_superuser(
            email='superuser1@gmail.com',
            password='superuser1pass',
        )
        self.client.force_authenticate(self.superuser)

    # def test_IsOwnerOrReadOnly(self):
    
    #     res = self.client.post(CREATE_USER_URL, self.user_payload)

    #     user = get_user_model().objects.get(id=res.data['id'])
    #     pass

    def test_IsSuperUser(self):
        """test the IsSuperUser permission"""
        request.user = self.superuser
        permission = permissions.IsSuperUser().has_permission(request, None)

        self.assertTrue(permission)

    def test_IsStaffOrReadOnly(self):        
        """test the IsStaffOrReadOnly permission"""
        res = self.client.post(CREATE_USER_URL, self.staff_payload)

        user = get_user_model().objects.get(id=res.data['id'])
        request.user = user
        
        permission = permissions.IsStaff().has_permission(request, None)

        self.assertTrue(permission)

    def test_IsITDept(self):
        """test the IsITDept permission"""
        res = self.client.post(CREATE_USER_URL, self.staff_payload)

        user = get_user_model().objects.get(id=res.data['id'])
        request.user = user

        staff = umodels.Staff.objects.get(user=user)        
        staff.is_IT = True
        staff.save()

        permission = permissions.IsITDept().has_permission(request, None)

        self.assertTrue(permission)

    def test_IsBursar(self):
        """test the IsBursar permission"""
        res = self.client.post(CREATE_USER_URL, self.staff_payload)

        user = get_user_model().objects.get(id=res.data['id'])
        request.user = user

        staff = umodels.Staff.objects.get(user=user)        
        staff.is_bursar = True
        staff.save()

        permission = permissions.IsBursar().has_permission(request, None)

        self.assertTrue(permission)

    def test_IsLecturer(self):
        """test the IsLecturer permission"""
        res = self.client.post(CREATE_USER_URL, self.staff_payload)

        user = get_user_model().objects.get(id=res.data['id'])
        request.user = user

        staff = umodels.Staff.objects.get(user=user)        
        staff.is_lecturer = True
        staff.save()

        permission = permissions.IsLecturer().has_permission(request, None)

        self.assertTrue(permission)

    def test_IsHead(self):
        """test the IsHead permission"""
        res = self.client.post(CREATE_USER_URL, self.staff_payload)

        user = get_user_model().objects.get(id=res.data['id'])
        request.user = user

        staff = umodels.Staff.objects.get(user=user)        
        staff.is_head_of_department = True
        staff.save()

        permission = permissions.IsHead().has_permission(request, None)

        self.assertTrue(permission)

    def test_IsDean(self):
        """test the IsDean permission"""
        res = self.client.post(CREATE_USER_URL, self.staff_payload)

        user = get_user_model().objects.get(id=res.data['id'])
        request.user = user

        staff = umodels.Staff.objects.get(user=user)        
        staff.is_dean_of_faculty = True
        staff.save()

        permission = permissions.IsDean().has_permission(request, None)

        self.assertTrue(permission)

    def test_IsStudent(self):
        """test the IsStudent permission"""
        res = self.client.post(CREATE_USER_URL, self.user_payload)

        user = get_user_model().objects.get(id=res.data['id'])
        request.user = user

        student = umodels.Student.objects.create(user=user)        

        permission = permissions.IsStudent().has_permission(request, None)

        self.assertTrue(permission)
    
