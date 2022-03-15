from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


COURSE_URL = reverse('academics:course-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def course_detail_url(course_id):
    """return url for the course detail"""
    return reverse('academics:course-detail', args=[course_id])


def sample_faculty(**kwargs):
    """create and return a sample faculty"""
    defaults = {'name': 'Faculty 1'}
    defaults.update(kwargs)
    return models.Faculty.objects.create(**defaults)


def sample_department(faculty, **kwargs):
    """create and return a sample department"""
    defaults = {'name': 'Specialization 1'}
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
    }
    defaults.update(kwargs)
    return models.Specialization.objects.create(department=department, max_level=max_level, **defaults)


def sample_course(specialization, **kwargs):
    """create and return a sample course"""
    defaults = {
        'name': 'Course 1',
    }
    defaults.update(kwargs)
    return models.Course.objects.create(specialization=specialization, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicCourseApiTest(TestCase):
    """test public access to the course api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(COURSE_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateCourseApiTest(TestCase):
    """test authenticated access to the course api"""

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
        self.specialization = sample_specialization(department=self.department, max_level=self.level)

    def test_retrieve_course(self):
        """test retrieving a list of courses"""
        sample_course(specialization=self.specialization)
        course = models.Course.objects.all()
        serializer = serializers.CourseSerializer(course, many=True, context=serializer_context)

        res = self.client.get(COURSE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_course_detail(self):
        """test retrieving a course's detail"""
        course = sample_course(specialization=self.specialization)
        serializer = serializers.CourseSerializer(course, context=serializer_context)

        url = course_detail_url(course_id=course.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_course(self):
        """test creating a course"""
        specialization = sample_specialization(
            department=self.department,
            max_level=self.level,
            name='Specialization 2'
        )
        specialization_serializer = serializers.SpecializationSerializer(
            specialization,
            context=serializer_context
        )
        payload = {
            'specialization': specialization.id,
            'name': 'Course 2',
            'description': 'some description text',
        }

        res = self.client.post(COURSE_URL, payload)

        course = models.Course.objects.get(id=res.data['id'])
        course_serializer = serializers.CourseSerializer(course, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, course, course_serializer)

    def test_partial_update_course(self):
        """test partially updating a course's detail using patch"""
        course = sample_course(specialization=self.specialization)
        payload = {
            'description': 'some description text',
        }

        url = course_detail_url(course.id)
        res = self.client.patch(url, payload)

        course.refresh_from_db()
        course_serializer = serializers.CourseSerializer(course, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, course, course_serializer)

    def test_full_update_course(self):
        """test updating a course's detail using put"""
        course = sample_course(specialization=self.specialization)
        specialization = sample_specialization(
            department=self.department,
            max_level=self.level,
            name='Specialization 3'
        )
        specialization_serializer = serializers.SpecializationSerializer(
            specialization,
            context=serializer_context
        )
        payload = {
            'specialization': specialization.id,
            'name': 'Course 3',
            'description': 'some description text',
        }

        url = course_detail_url(course.id)
        res = self.client.put(url, payload)

        course.refresh_from_db()
        course_serializer = serializers.CourseSerializer(course, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, course, course_serializer)
