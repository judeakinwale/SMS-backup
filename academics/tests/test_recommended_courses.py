from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


RECOMMEDED_COURSES_URL = reverse('academics:recommendedcourses-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def recommended_courses_detail_url(recommended_courses_id):
    """return url for the recommended_courses detail"""
    return reverse('academics:recommendedcourses-detail', args=[recommended_courses_id])


def sample_faculty(**kwargs):
    """create and return a sample faculty"""
    defaults = {'name': 'Faculty 1'}
    defaults.update(kwargs)
    return models.Faculty.objects.create(**defaults)


def sample_department(faculty, **kwargs):
    """create and return a sample department"""
    defaults = {'name': 'Department 1'}
    defaults.update(kwargs)
    return models.Department.objects.create(faculty=faculty, **defaults)


def sample_level(**kwargs):
    """create and return a sample level"""
    defaults = {'code': 100}
    defaults.update(**kwargs)
    return models.Level.objects.create(**defaults)


def sample_max_level(**kwargs):
    """create and return a sample level"""
    defaults = {'code': 500}
    defaults.update(**kwargs)
    return models.Level.objects.create(**defaults)


def sample_specialization(department, max_level, **kwargs):
    """create and return a sample specialization"""
    defaults = {
        'name': 'Specialization 1',
        'max_level': max_level,
    }
    defaults.update(kwargs)
    return models.Specialization.objects.create(department=department, **defaults)


def sample_course(specialization, **kwargs):
    """create and return a sample course"""
    defaults = {
        'name': 'Course 1',
    }
    defaults.update(kwargs)
    return models.Course.objects.create(specialization=specialization, **defaults)


def sample_recommended_courses(specialization, semester, level, **kwargs):
    """create and return a sample recommended_courses"""
    defaults = {
        'level': level,
        'semester': semester,
    }
    defaults.update(kwargs)
    return models.RecommendedCourses.objects.create(specialization=specialization, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except Exception:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicRecommendedCoursesApiTest(TestCase):
    """test public access to the recommended_courses api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(RECOMMEDED_COURSES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecommendedCoursesApiTest(TestCase):
    """test authenticated access to the recommended_courses api"""

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
        self.max_level = sample_max_level()
        self.specialization = sample_specialization(department=self.department, max_level=self.max_level)
        self.course = sample_course(specialization=self.specialization)
        self.semester = models.Semester.objects.create(semester=1)

    def test_retrieve_recommended_courses(self):
        """test retrieving a list of recommended_coursess"""
        sample_recommended_courses(
            specialization=self.specialization,
            semester=self.semester,
            level=self.max_level
        )
        recommended_courses = models.RecommendedCourses.objects.all()
        serializer = serializers.RecommendedCoursesSerializer(
            recommended_courses,
            many=True,
            context=serializer_context
        )

        res = self.client.get(RECOMMEDED_COURSES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_recommended_courses_detail(self):
        """test retrieving a recommended_courses's detail"""
        recommended_courses = sample_recommended_courses(
            specialization=self.specialization,
            semester=self.semester,
            level=self.level
        )
        recommended_courses.courses.add(self.course)
        serializer = serializers.RecommendedCoursesSerializer(
            recommended_courses,
            context=serializer_context
        )

        url = recommended_courses_detail_url(recommended_courses_id=recommended_courses.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recommended_courses(self):
        """test creating a recommended_courses"""
        specialization_serializer = serializers.SpecializationSerializer(
            self.specialization,
            context=serializer_context
        )
        semester_serializer = serializers.SemesterSerializer(self.semester, context=serializer_context)
        course_serializer = serializers.CourseSerializer(self.course, context=serializer_context)
        level_serializer = serializers.LevelSerializer(self.level, context=serializer_context)
        payload = {
            'specialization': specialization_serializer.data['url'],
            'courses': [course_serializer.data['url'], ],
            'semester': semester_serializer.data['url'],
            'level': level_serializer.data['url'],
        }

        res = self.client.post(RECOMMEDED_COURSES_URL, payload)

        recommended_courses = models.RecommendedCourses.objects.get(id=res.data['id'])
        recommended_courses_serializer = serializers.RecommendedCoursesSerializer(
            recommended_courses,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, recommended_courses, recommended_courses_serializer)

    def test_partial_update_recommended_courses(self):
        """test partially updating a recommended_courses's detail using patch"""
        recommended_courses = sample_recommended_courses(
            specialization=self.specialization,
            semester=self.semester,
            level=self.max_level
        )
        level_serializer = serializers.LevelSerializer(self.level, context=serializer_context)
        payload = {
            'level': level_serializer.data['url'],
        }

        url = recommended_courses_detail_url(recommended_courses.id)
        res = self.client.patch(url, payload)

        recommended_courses.refresh_from_db()
        recommended_courses_serializer = serializers.RecommendedCoursesSerializer(
            recommended_courses,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, recommended_courses, recommended_courses_serializer)

    def test_full_update_recommended_courses(self):
        """test updating a recommended_courses's detail using put"""
        recommended_courses = sample_recommended_courses(
            specialization=self.specialization,
            semester=self.semester,
            level=self.max_level
        )

        specialization_serializer = serializers.SpecializationSerializer(
            self.specialization,
            context=serializer_context
        )
        semester_serializer = serializers.SemesterSerializer(self.semester, context=serializer_context)
        course_serializer = serializers.CourseSerializer(self.course, context=serializer_context)
        level_serializer = serializers.LevelSerializer(self.level, context=serializer_context)
        payload = {
            'specialization': specialization_serializer.data['url'],
            'courses': [course_serializer.data['url'], ],
            'semester': semester_serializer.data['url'],
            'level': level_serializer.data['url'],
        }

        url = recommended_courses_detail_url(recommended_courses.id)
        res = self.client.put(url, payload)

        recommended_courses.refresh_from_db()
        recommended_courses_serializer = serializers.RecommendedCoursesSerializer(
            recommended_courses,
            context=serializer_context
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, recommended_courses, recommended_courses_serializer)
