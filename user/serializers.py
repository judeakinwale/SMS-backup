from rest_framework import serializers
from django.contrib.auth import get_user_model
from user import models
from academics import models as amodels


class AcademicDataSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the AcademicData model"""

    student = serializers.HyperlinkedRelatedField(queryset=models.Student.objects.all(), view_name='user:student-detail')

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

    biodata = serializers.HyperlinkedRelatedField(queryset=models.Biodata.objects.all(), view_name='user:biodata-detail', required=False)

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

    biodata = serializers.HyperlinkedRelatedField(queryset=models.Biodata.objects.all(), view_name='user:biodata-detail', required=False)

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

    biodata = serializers.HyperlinkedRelatedField(queryset=models.Biodata.objects.all(), view_name='user:biodata-detail', required=False)

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

    user = serializers.HyperlinkedRelatedField(queryset=get_user_model().objects.all(), view_name='user:user-detail')
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
        # if validated_data['academic_history'] == "" or []:
        #     academic_history = models.AcademicHistory.objects.create(biodata=biodata)
        if 'health_data' in validated_data:
            health_data_data = validated_data.pop('health_data')
        # if validated_data['health_data'] == "" or []:
        #     health_data= models.HealthData.objects.create(biodata=biodata)
        if 'family_data' in validated_data:
            family_data_data = validated_data.pop('family_data')
        # if validated_data['family_data'] == "" or []:
        #     family_data = models.FamilyData.objects.create(biodata=biodata)
        
        biodata = super().create(validated_data)
        # academic_history = biodata.academic_history.add(**academic_history_data)
        # if academic_history_data:

        try:
            academic_history = models.AcademicHistory.objects.create(biodata=biodata, **academic_history_data)
        except:
            pass
        # if health_data_data:

        try:
            health_data= models.HealthData.objects.create(biodata=biodata, **health_data_data)
        except:
            pass
        # if family_data_data:

        try:
            family_data = models.FamilyData.objects.create(biodata=biodata, **family_data_data)
        except:
            pass
        # print(validated_data)
        return biodata


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the User model"""
    
    # biodata = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # biodata = serializers.HyperlinkedRelatedField(many=True, queryset=models.Biodata, required=False, allow_null=True, view_name='user:biodata-list')
    biodata = BiodataSerializer(allow_null=True, required=False)
    # biodata = BiodataSerializer(many=True)

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
            'password' : {'write_only': True, 'min_length': 5},
        }

    def create(self, validated_data):
        """create a new user with an encrypted password, a related biodata and return the user"""
        if 'biodata' not in validated_data or validated_data['biodata'] == '':
            user = get_user_model().objects.create_user(**validated_data)
        else:
            biodata_data = validated_data.pop('biodata')
            user = get_user_model().objects.create_user(**validated_data)
            # biodata = user.biodata.set(**biodata_data)
            biodata = models.Biodata.objects.create(user=user, **biodata_data)

        if user.is_staff == True:
            staff = models.Staff.objects.create(user=user)
        else:
            student = models.Student.objects.create(user=user)
            academic_data = models.AcademicData.objects.create(student=student)

        # print(biodata.user)
        return user

    def update(self, instance, validated_data):
        """update a user, correctly setting the password and return it"""
        password = validated_data.pop('password')
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Staff model"""

    user = serializers.HyperlinkedRelatedField(queryset=get_user_model().objects.filter(is_staff=True), view_name='user:user-detail')

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

    user = serializers.HyperlinkedRelatedField(queryset=get_user_model().objects.all(), view_name='user:user-detail')
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

    course = serializers.HyperlinkedRelatedField(queryset=amodels.Course.objects.all(), view_name='academics:course-detail')
    student = serializers.HyperlinkedRelatedField(queryset=models.Student.objects.all(), view_name='user:student-detail')
    # academic_data = AcademicDataSerializer(allow_null=True, required=False)

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
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView)


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

