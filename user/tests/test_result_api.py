from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from user import models, serializers
from academics import models as amodels
from academics import serializers as aserializers
from datetime import datetime


RESULT_URL = reverse('user:result-list')

year_string = f"{datetime.today().year}"

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def result_detail_url(result_id):
    """return url for the result detail"""
    return reverse('user:result-detail', args=[result_id])


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
    defaults = {
        'name': 'Specialization 1',
        'faculty': faculty,
    }
    defaults.update(kwargs)
    return amodels.Department.objects.create(**defaults)


def sample_level(**kwargs):
    """create and return a sample level"""
    defaults = {'code': 400}
    defaults.update(**kwargs)
    return amodels.Level.objects.create(**defaults)


def sample_specialization(department, max_level, **kwargs):
    """create and return a sample specialization"""
    defaults = {
        'name': 'Specialization 1',
        'department': department,
        'max_level': max_level,
    }
    defaults.update(kwargs)
    return amodels.Specialization.objects.create(**defaults)


def sample_course(specialization, **kwargs):
    """create and return a sample course"""
    defaults = {
        'name': 'Course 1',
        'specialization': specialization,
    }
    defaults.update(kwargs)
    return amodels.Course.objects.create(**defaults)


def sample_result(score, course, student, **kwargs):
    """create and return sample result"""
    defaults = {
        'score': score,
        'course': course,
        'student': student,
    }
    defaults.update(kwargs)
    return models.Result.objects.create(**defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicResultApiTest(TestCase):
    """test public access to the result api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(RESULT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateResultApiTest(TestCase):
    """test authenticated access to the result api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.serializer = serializers.UserSerializer(self.user, context=serializer_context)
        self.score = 75
        self.faculty = sample_faculty()
        self.department = sample_department(faculty=self.faculty)
        self.level = sample_level()
        self.specialization = sample_specialization(department=self.department, max_level=self.level)
        self.course = sample_course(specialization=self.specialization)
        self.student = sample_student(user=self.user)
        self.semester = amodels.Semester.objects.create(semester=1)
        self.session = amodels.Session.objects.create(year=year_string)
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_result(self):
        """test retrieving a list of result"""
        sample_result(score=70, course=self.course, student=self.student)
        result = models.Result.objects.all()
        serializer = serializers.ResultSerializer(result, many=True, context=serializer_context)

        res = self.client.get(RESULT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    # def test_result_not_limited_to_user(self):
    #     """test that results from all users is returned"""
    #     sample_result(score=70, course=self.course, student=self.student)
    #     user2 = get_user_model().objects.create_user(
    #         'test2@test.com',
    #         'testpass2'
    #     )
    #     sample_result(user=user2)

    #     result = models.Result.objects.all()
    #     serializer = serializers.ResultSerializer(result, many=True, context=serializer_context)

    #     res = self.client.get(RESULT_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['results'], serializer.data)
    #     self.assertEqual(len(res.data['results']), 2)

    def test_retrieve_result_detail(self):
        """test retrieving a result's detail"""
        result = sample_result(score=70, course=self.course, student=self.student)
        serializer = serializers.ResultSerializer(result, context=serializer_context)

        url = result_detail_url(result_id=result.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_result(self):
        """test creating a result"""
        course_serializer = aserializers.CourseSerializer(self.course, context=serializer_context)
        student_serializer = serializers.StudentSerializer(self.student, context=serializer_context)
        semester_serializer = aserializers.SemesterSerializer(self.semester, context=serializer_context)
        session_serializer = aserializers.SessionSerializer(self.session, context=serializer_context)
        payload = {
            "score": self.score,
            "course": course_serializer.data['url'],
            "student": student_serializer.data['url'],
            "semester": semester_serializer.data['url'],
            "session": session_serializer.data['url'],
        }

        res = self.client.post(RESULT_URL, payload)

        result = models.Result.objects.get(id=res.data['id'])
        result_serializer = serializers.ResultSerializer(result, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, result, result_serializer)

    def test_partial_update_result(self):
        """test partially updating a result's detail using patch"""
        result = sample_result(score=70, course=self.course, student=self.student)

        payload = {
            'score': 85,
        }

        url = result_detail_url(result.id)
        res = self.client.patch(url, payload)

        result.refresh_from_db()
        result_serializer = serializers.ResultSerializer(result, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, result, result_serializer)

    def test_full_update_result(self):
        """test updating a result's detail using put"""
        result = sample_result(score=55, course=self.course, student=self.student)

        course_serializer = aserializers.CourseSerializer(self.course, context=serializer_context)
        student_serializer = serializers.StudentSerializer(self.student, context=serializer_context)
        semester_serializer = aserializers.SemesterSerializer(self.semester, context=serializer_context)
        session_serializer = aserializers.SessionSerializer(self.session, context=serializer_context)

        payload = {
            "score": self.score,
            "course": course_serializer.data['url'],
            "student": student_serializer.data['url'],
            "semester": semester_serializer.data['url'],
            "session": session_serializer.data['url'],
        }

        url = result_detail_url(result.id)
        res = self.client.put(url, payload)

        result.refresh_from_db()
        result_serializer = serializers.ResultSerializer(result, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, result, result_serializer)
