from rest_framework import serializers
from django.contrib.auth import get_user_model
from user import models
from academics import models as amodels

# For JWT and drf-yasg integration
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


class AcademicDataSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the AcademicData model"""

    student = serializers.HyperlinkedRelatedField(
        queryset=models.Student.objects.all(),
        view_name='user:student-detail'
    )

    class Meta:
        model = models.AcademicData
        fields = [
            'id',
            'url',
            'student',
            'programme',
            'start_date',
            'end_date',
            'qualification',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:academicdata-detail'},
        }


class AcademicHistorySerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the AcademicHistory model"""

    biodata = serializers.HyperlinkedRelatedField(
        queryset=models.Biodata.objects.all(),
        view_name='user:biodata-detail',
        required=False
    )

    class Meta:
        model = models.AcademicHistory
        fields = [
            'id',
            'url',
            'biodata',
            'institution',
            'start_date',
            'end_date',
            'qualification_earned',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:academichistory-detail'},
        }


class HealthDataSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the HealthData model"""

    biodata = serializers.HyperlinkedRelatedField(
        queryset=models.Biodata.objects.all(),
        view_name='user:biodata-detail',
        required=False
    )

    class Meta:
        model = models.HealthData
        fields = [
            'id',
            'url',
            'biodata',
            'blood_group',
            'genotype',
            'allergies',
            'diabetes',
            'STIs',
            'heart_disease',
            'disabilities',
            'respiratory_problems',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:healthdata-detail'},
        }


class FamilyDataSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the FamilyData model"""

    biodata = serializers.HyperlinkedRelatedField(
        queryset=models.Biodata.objects.all(),
        view_name='user:biodata-detail',
        required=False
    )

    class Meta:
        model = models.FamilyData
        fields = [
            'id',
            'url',
            'biodata',
            'next_of_kin_full_name',
            'next_of_kin_phone_no_1',
            'next_of_kin_phone_no_2',
            'next_of_kin_address',
            'guardian_full_name',
            'guardian_phone_no_1',
            'guardian_phone_no_2',
            'guardian_address',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:familydata-detail'},
        }


class BiodataSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Biodata model"""

    user = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.all(),
        view_name='user:user-detail',
        allow_null=True,
        required=False
    )
    academic_history = AcademicHistorySerializer(many=True, allow_null=True, required=False)
    health_data = HealthDataSerializer(allow_null=True, required=False)
    family_data = FamilyDataSerializer(allow_null=True, required=False)

    class Meta:
        model = models.Biodata
        fields = [
            'id',
            'url',
            'user',
            'marital_status',
            'gender',
            'religion',
            'birthday',
            'nationality',
            'state_of_origin',
            'local_govt',
            'permanent_address',
            'address',
            'phone_no_1',
            'phone_no_2',
            'profile_picture',
            'academic_history',
            'health_data',
            'family_data',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:biodata-detail'},
        }

    def create(self, validated_data):
        if 'academic_history' in validated_data:
            academic_history_data = validated_data.pop('academic_history')

        if 'health_data' in validated_data:
            health_data_data = validated_data.pop('health_data')

        if 'family_data' in validated_data:
            family_data_data = validated_data.pop('family_data')

        biodata = super().create(validated_data)

        try:
            models.AcademicHistory.objects.create(
                biodata=biodata,
                **academic_history_data
            )
        except:
            pass

        try:
            models.HealthData.objects.create(biodata=biodata, **health_data_data)
        except:
            pass

        try:
            models.FamilyData.objects.create(biodata=biodata, **family_data_data)
        except:
            pass

        return biodata

    def update(self, instance, validated_data):
        if 'academic_history' in validated_data:
            academic_history_data = validated_data.pop('academic_history')

        if 'health_data' in validated_data:
            health_data_data = validated_data.pop('health_data')

        if 'family_data' in validated_data:
            family_data_data = validated_data.pop('family_data')

        biodata = super().update(instance, validated_data)

        try:
            academic_history = instance.academic_history
            academic_history.institution = academic_history_data.get('institution', instance.institution)
            academic_history.start_date = academic_history_data.get('start_date', instance.start_date)
            academic_history.end_date = academic_history_data.get('end_date', instance.end_date)
            academic_history.save()
        except:
            pass

        try:
            health_data = instance.health_data
            health_data.blood_group = health_data_data.get('blood_group', instance.blood_group)
            health_data.genotype = health_data_data.get('genotype', instance.genotype)
            health_data.allergies = health_data_data.get('allergies', instance.allergies)
            health_data.diabetes = health_data_data.get('diabetes', instance.diabetes)
            health_data.STIs = health_data_data.get('STIs', instance.STIs)
            health_data.heart_disease = health_data_data.get('heart_disease', instance.heart_disease)
            health_data.disabilities = health_data_data.get('disabilities', instance.disabilities)
            health_data.respiratory_problems = health_data_data.get(
                'respiratory_problems',
                instance.respiratory_problems,
            )
            health_data.save()
        except:
            pass

        try:
            family_data = instance.family_data
            family_data.next_of_kin_full_name = family_data_data.get(
                'next_of_kin_full_name',
                instance.next_of_kin_full_name
            )
            family_data.next_of_kin_phone_no_1 = family_data_data.get(
                'next_of_kin_phone_no_1',
                instance.next_of_kin_phone_no_1
            )
            family_data.next_of_kin_phone_no_2 = family_data_data.get(
                'next_of_kin_phone_no_2',
                instance.next_of_kin_phone_no_2
            )
            family_data.next_of_kin_address = family_data_data.get(
                'next_of_kin_address',
                instance.next_of_kin_address
            )
            family_data.guardian_full_name = family_data_data.get(
                'guardian_full_name',
                instance.guardian_full_name
            )
            family_data.guardian_phone_no_1 = family_data_data.get(
                'guardian_phone_no_1',
                instance.guardian_phone_no_1
            )
            family_data.guardian_phone_no_2 = family_data_data.get(
                'guardian_phone_no_2',
                instance.guardian_phone_no_2
            )
            family_data.guardian_address = family_data_data.get(
                'guardian_address',
                instance.guardian_address
            )
            family_data.save()
        except:
            pass

        return biodata


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the User model"""

    biodata = BiodataSerializer(allow_null=True, required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'url',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'password',
            'biodata',
            'is_staff',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:user-detail'},
            'password': {'write_only': True, 'min_length': 5},
        }

    def create(self, validated_data):
        """create a new user with an encrypted password, a related biodata and return the user"""

        if 'biodata' not in validated_data or validated_data['biodata'] == '':
            user = get_user_model().objects.create_user(**validated_data)
        else:
            biodata_data = validated_data.pop('biodata')
            user = get_user_model().objects.create_user(**validated_data)
            models.Biodata.objects.create(user=user, **biodata_data)

        if user.is_staff is True:
            models.Staff.objects.create(user=user)
        else:
            student = models.Student.objects.create(user=user)
            models.AcademicData.objects.create(student=student)

        return user

    def update(self, instance, validated_data):
        """update a user, correctly setting the password and return it"""

        if 'biodata' not in validated_data or validated_data['biodata'] == []:
            password = validated_data.pop('password')
            user = super().update(instance, validated_data)
        else:
            biodata_data = validated_data.pop('biodata')
            password = validated_data.pop('password')
            user = super().update(instance, validated_data)

            try:
                biodata = models.Biodata.objects.get(user=user)
                # print("\nBiodata exists")
                biodata.marital_status = biodata_data.get('marital_status', instance.marital_status)
                biodata.gender = biodata_data.get('gender', instance.gender)
                biodata.religion = biodata_data.get('religion', instance.religion)
                biodata.birthday = biodata_data.get('birthday', instance.birthday)
                biodata.nationality = biodata_data.get('nationality', instance.nationality)
                biodata.state_of_origin = biodata_data.get('state_of_origin', instance.state_of_origin)
                biodata.local_govt = biodata_data.get('local_govt', instance.local_govt)
                biodata.permanent_address = biodata_data.get(
                    'permanent_address',
                    instance.permanent_address,
                )
                biodata.address = biodata_data.get('address', instance.address)
                biodata.phone_no_1 = biodata_data.get('phone_no_1', instance.phone_no_1)
                biodata.phone_no_2 = biodata_data.get('phone_no_2', instance.phone_no_2)
                biodata.profile_picture = biodata_data.get('profile_picture', instance.profile_picture)
                biodata.academic_history = biodata_data.get('academic_history', instance.academic_history)
                biodata.health_data = biodata_data.get('health_data', instance.health_data)
                biodata.family_data = biodata_data.get('family_data', instance.family_data)
                biodata.save()
            except:
                # print("\nBiodata doesn't exist")
                biodata = models.Biodata.objects.create(user=user, **biodata_data)

        if password:
            user.set_password(password)
            user.save()

        if user.is_staff is True:
            try:
                models.Staff.objects.get(user=user)
            except:
                models.Staff.objects.create(user=user)

        return user


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Staff model"""

    user = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        view_name='user:user-detail'
    )

    class Meta:
        model = models.Staff
        fields = [
            'id',
            'url',
            'user',
            'employee_id',
            'programme',
            'is_active',
            'is_lecturer',
            'is_bursar',
            'is_IT',
            'is_head_of_department',
            'is_dean_of_faculty',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:staff-detail'},
        }


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Student model"""

    user = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.all(),
        view_name='user:user-detail'
    )
    academic_data = AcademicDataSerializer(allow_null=True, required=False)

    class Meta:
        model = models.Student
        fields = [
            'id',
            'url',
            'user',
            'matric_no',
            'student_id',
            'academic_data',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:student-detail'},
        }


class CourseRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the CourseRegistration model"""

    course = serializers.HyperlinkedRelatedField(
        queryset=amodels.Course.objects.all(),
        view_name='academics:course-detail'
    )
    student = serializers.HyperlinkedRelatedField(
        queryset=models.Student.objects.all(),
        view_name='user:student-detail'
    )

    class Meta:
        model = models.CourseRegistration
        fields = [
            'id',
            'url',
            'course',
            'student',
            'session',
            'semester',
            'is_active',
            'is_completed',
            'is_passed',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:courseregistration-detail'},
        }


# Simple JWT integration with drf-yasg
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
