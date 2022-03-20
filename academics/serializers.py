from django.contrib.auth import get_user_model
from rest_framework import serializers
from academics import models
from assessment.serializers import QuizSerializer
# from user.serializers import UserSerializer


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Level model"""

    class Meta:
        model = models.Level
        fields = [
            'id',
            'url',
            'code',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:level-detail'}
        }


class SemesterSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Semester model"""

    class Meta:
        model = models.Semester
        fields = [
            'id',
            'url',
            'semester',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:semester-detail'}
        }


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Session model"""

    class Meta:
        model = models.Session
        fields = [
            'id',
            'url',
            'year',
            'is_current',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:session-detail'}
        }


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Course model"""

    specialization = serializers.PrimaryKeyRelatedField(
        queryset=models.Specialization.objects.all(),
        # view_name='academics:specialization-detail',
    )
    coordinator = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        # view_name='user:user-detail',
        allow_null=True,
        required=False,
    )
    quizzes = QuizSerializer(source='course_set', many=True, read_only=True)

    class Meta:
        model = models.Course
        fields = [
            'id',
            'url',
            'specialization',
            'name',
            'code',
            'description',
            'coordinator',
            'quizzes',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:course-detail'}
        }


class RecommendedCoursesSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the RecommendedCourses model"""

    specialization = serializers.PrimaryKeyRelatedField(
        queryset=models.Specialization.objects.all(),
        # view_name='academics:specialization-detail',
        # allow_null=True,
        # required=False,
    )
    course = serializers.PrimaryKeyRelatedField(
        # many=True,
        queryset=models.Course.objects.all(),
        # view_name='academics:course-detail',
        allow_null=True,
        required=False,
    )
    # courses = CourseSerializer(read_only=True, many=True)
    semester = serializers.PrimaryKeyRelatedField(
        queryset=models.Semester.objects.all(),
        # view_name='academics:semester-detail',
        # allow_null=True,
        # required=False,
    )
    level = serializers.PrimaryKeyRelatedField(
        queryset=models.Level.objects.all(),
        # view_name='academics:level-detail',
        # allow_null=True,
        # required=False,
    )

    class Meta:
        model = models.RecommendedCourses
        fields = [
            'id',
            'url',
            'specialization',
            'course',
            'semester',
            'level',
            'is_compulsory',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:recommendedcourses-detail'}
        }
        depth = 1


class SpecializationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Specialization model"""

    department = serializers.PrimaryKeyRelatedField(
        queryset=models.Department.objects.all(),
        # view_name='academics:department-detail',
    )
    max_level = serializers.PrimaryKeyRelatedField(
        queryset=models.Level.objects.all(),
        # view_name='academics:level-detail',
    )
    # courses = CourseSerializer(source='course_set', many=True, read_only=True)
    # recommended_courses = RecommendedCoursesSerializer(many=True, read_only=True)
    # direct_recommended_courses = RecommendedCoursesSerializer(many=True, read_only=True)

    class Meta:
        model = models.Specialization
        fields = [
            'id',
            'url',
            'department',
            'name',
            'code',
            'max_level',
            'description',
            # 'courses',
            # 'recommended_courses',
            # 'direct_recommended_courses',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:specialization-detail'}
        }


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Department model"""

    faculty = serializers.PrimaryKeyRelatedField(
        queryset=models.Faculty.objects.all(),
        # view_name='academics:faculty-detail',
    )
    head = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        # view_name='user:user-detail',
        allow_null=True,
        required=False
    )
    specializations = SpecializationSerializer(source='specialization_set', many=True, read_only=True)

    class Meta:
        model = models.Department
        fields = [
            'id',
            'url',
            'faculty',
            'name',
            'code',
            'description',
            'head',
            'specializations',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:department-detail'}
        }


class FacultySerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Faculty model"""

    dean = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        # view_name='user:user-detail',
        allow_null=True,
        required=False,
    )
    departments = DepartmentSerializer(source='department_set', many=True, read_only=True)

    class Meta:
        model = models.Faculty
        fields = [
            'id',
            'url',
            'name',
            'code',
            'description',
            'dean',
            'departments',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:faculty-detail'}
        }


class RecommendedCoursesResponseSerializer(RecommendedCoursesSerializer):
    """serializer for the RecommendedCourses model"""

    specialization = SpecializationSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    # courses = CourseSerializer(read_only=True, many=True)
    semester = SemesterSerializer(read_only=True)
    level = LevelSerializer(read_only=True)


class SpecializationResponseSerializer(SpecializationSerializer):
    """serializer for the Specialization model"""

    department = DepartmentSerializer(read_only=True)
    max_level = LevelSerializer(read_only=True)
    courses = CourseSerializer(source='course_set', many=True, read_only=True)
    recommended_courses = RecommendedCoursesResponseSerializer(many=True, read_only=True)
    direct_recommended_courses = RecommendedCoursesResponseSerializer(many=True, read_only=True)

    class Meta(SpecializationSerializer.Meta):
        additional_fields = [
            'courses',
            'recommended_courses',
            'direct_recommended_courses',
        ]
        fields = SpecializationSerializer.Meta.fields + additional_fields


class CourseResponseSerializer(CourseSerializer):
    """serializer for the Course model"""

    specialization = SpecializationSerializer(read_only=True)


class DepartmentResponseSerializer(DepartmentSerializer):
    """serializer for the Department model"""

    faculty = FacultySerializer(read_only=True)
