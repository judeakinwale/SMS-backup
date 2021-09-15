from django.contrib.auth import get_user_model
from rest_framework import serializers
from academics import models


class FacultySerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Faculty model"""

    dean = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        view_name='user:user-detail',
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.Faculty
        fields = [
            'id',
            'url',
            'name',
            'code',
            'description',
            'dean',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:faculty-detail'}
        }


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Department model"""

    faculty = serializers.HyperlinkedRelatedField(
        queryset=models.Faculty.objects.all(),
        view_name='academics:faculty-detail',
    )
    head = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        view_name='user:user-detail',
        allow_null=True,
        required=False
    )

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
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:department-detail'}
        }


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Programme model"""

    department = serializers.HyperlinkedRelatedField(
        queryset=models.Department.objects.all(),
        view_name='academics:department-detail',
    )
    max_level = serializers.HyperlinkedRelatedField(
        queryset=models.Level.objects.all(),
        view_name='academics:level-detail',
    )

    class Meta:
        model = models.Programme
        fields = [
            'id',
            'url',
            'department',
            'name',
            'code',
            'max_level',
            'description',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:programme-detail'}
        }


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Course model"""

    programme = serializers.HyperlinkedRelatedField(
        queryset=models.Programme.objects.all(),
        view_name='academics:programme-detail',
    )
    coordinator = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        view_name='user:user-detail',
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.Course
        fields = [
            'id',
            'url',
            'programme',
            'name',
            'code',
            'description',
            'coordinator',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:course-detail'}
        }


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
