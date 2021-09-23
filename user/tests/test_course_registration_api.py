from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers
from academics import models as amodels
from academics import serializers as aserializers


COURSE_REGISTRATION_URL = reverse('user:courseregistration-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def course_registration_detail_url(course_registration_id):
    """return url for the course_registration detail"""
    return reverse('user:courseregistration-detail', args=[course_registration_id])


def sample_student(user, **kwargs):
    """create and return sample student"""
    return models.Student.objects.create(user=user, **kwargs)


def sample_faculty(**kwargs):
    """create and return a sample faculty"""
    defaults = {'name': 'Faculty 1'}
    defaults.update(kwargs)
    return amodels.Faculty.objects.create(**defaults)


def sample_department(faculty, **kwargs):
    """create and return a sample department"""
    defaults = {'name': 'Specialization 1'}
    defaults.update(kwargs)
    return amodels.Department.objects.create(faculty=faculty, **defaults)


def sample_level(**kwargs):
    """create and return a sample level"""
    defaults = {'code': 100}
    defaults.update(**kwargs)
    return amodels.Level.objects.create(**defaults)


def sample_specialization(department, max_level, **kwargs):
    """create and return a sample specialization"""
    defaults = {
        'name': 'Specialization 1',
    }
    defaults.update(kwargs)
    return amodels.Specialization.objects.create(department=department, max_level=max_level, **defaults)


def sample_course(specialization, **kwargs):
    """create and return a sample course"""
    defaults = {
        'name': 'Course 1',
    }
    defaults.update(kwargs)
    return amodels.Course.objects.create(specialization=specialization, **defaults)


def sample_course_registration(course, student, **kwargs):
    """create and return sample course_registration"""
    return models.CourseRegistration.objects.create(course=course, student=student, **kwargs)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicCourseRegistrationApiTest(TestCase):
    """test public access to the course_registration api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(COURSE_REGISTRATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCourseRegistrationApiTest(TestCase):
    """test authenticated access to the course_registration api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        # Create sample faculty, department, level and specialization
        self.faculty = sample_faculty()
        self.department = sample_department(faculty=self.faculty)
        self.level = sample_level()
        self.specialization = sample_specialization(department=self.department, max_level=self.level)
        self.course = sample_course(specialization=self.specialization)
        self.student = sample_student(user=self.user)
        self.course_serializer = aserializers.CourseSerializer(self.course, context=serializer_context)
        self.student_serializer = serializers.StudentSerializer(self.student, context=serializer_context)
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_course_registration(self):
        """test retrieving a list of course_registration"""
        sample_course_registration(course=self.course, student=self.student)
        course_registration = models.CourseRegistration.objects.all()
        serializer = serializers.CourseRegistrationSerializer(
            course_registration,
            many=True,
            context=serializer_context
        )

        res = self.client.get(COURSE_REGISTRATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_course_registration_detail(self):
        """test retrieving a course_registration's detail"""
        course_registration = sample_course_registration(course=self.course, student=self.student)
        serializer = serializers.CourseRegistrationSerializer(
            course_registration,
            context=serializer_context
        )

        url = course_registration_detail_url(course_registration_id=course_registration.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_course_registration(self):
        """test creating a course_registration"""
        payload = {
            'course': self.course_serializer.data['url'],
            'student': self.student_serializer.data['url'],
            'is_active': False,
        }

        res = self.client.post(COURSE_REGISTRATION_URL, payload)

        course_registration = models.CourseRegistration.objects.get(id=res.data['id'])
        course_registration_serializer = serializers.CourseRegistrationSerializer(
            course_registration,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, course_registration, course_registration_serializer)

    def test_partial_update_course_registration(self):
        """test partially updating a course_registration's detail using patch"""
        course_registration = sample_course_registration(course=self.course, student=self.student)

        payload = {
            'is_active': False,
        }

        url = course_registration_detail_url(course_registration.id)
        res = self.client.patch(url, payload)

        course_registration.refresh_from_db()
        course_registration_serializer = serializers.CourseRegistrationSerializer(
            course_registration,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, course_registration, course_registration_serializer)

    def test_full_update_course_registration(self):
        """test updating a course_registration's detail using put"""
        course_registration = sample_course_registration(course=self.course, student=self.student)
        course = sample_course(specialization=self.specialization, name='Course 21')
        serializer = aserializers.CourseSerializer(course, context=serializer_context)

        payload = {
            'course': serializer.data['url'],
            'student': self.student_serializer.data['url'],
            'is_active': False,
        }

        url = course_registration_detail_url(course_registration.id)
        res = self.client.put(url, payload)

        course_registration.refresh_from_db()
        course_registration_serializer = serializers.CourseRegistrationSerializer(
            course_registration,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, course_registration, course_registration_serializer)
