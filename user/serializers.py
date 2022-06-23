from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from dateutil.relativedelta import relativedelta
from user import models, setup
from academics import models as amodels
from academics import serializers as aserializers
from assessment import serializers as qserializers
from information import serializers as iserializers

# For JWT and drf-yasg integration
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


class BaseUserSerializer(serializers.HyperlinkedModelSerializer):
    """base serializer for the User model"""

    specialization = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Specialization.objects.all(),
        allow_null=True,
        required=False,
    )
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'url',
            'first_name',
            'middle_name',
            'last_name',
            'full_name',
            'email',
            'specialization',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
        ]
        optional_fields = [
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:user-detail'},
            'password': {'write_only': True, 'min_length': 5, 'required': False, 'allow_null': True},
        }


class BaseStaffSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Staff model"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        allow_null=True,
        required=False,
    )
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Specialization.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.Staff
        fields = [
            'id',
            'url',
            'user',
            'employee_id',
            'specialization',
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
        optional_fields = [
            'employee_id',
        ]


class BaseStudentSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Student model"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        allow_null=True,
        required=False,
    )
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Specialization.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.Student
        fields = [
            'id',
            'url',
            'user',
            'matric_no',
            'student_id',
            'specialization',
            'is_active',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:student-detail'},
        }
        optional_fields = [
            'matric_no',
            'student_id',
        ]


class AcademicDataSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the AcademicData model"""

    student = serializers.PrimaryKeyRelatedField(
        queryset=models.Student.objects.all(),
    )
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Specialization.objects.all(),
        allow_null=True,
        required=False,
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Department.objects.all(),
        allow_null=True,
        required=False,
    )
    level = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Level.objects.all(),
        allow_null=True,
        required=False,
    )
    semester = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Semester.objects.all(),
        allow_null=True,
        required=False,
    )
    session = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Session.objects.all(),
        allow_null=True,
        required=False,
    )
    gpa = serializers.ReadOnlyField(source='get_gpa')
    cgpa = serializers.ReadOnlyField(source='get_cgpa')

    class Meta:
        model = models.AcademicData
        fields = [
            'id',
            'url',
            'student',
            'specialization',
            'start_date',
            'end_date',
            'qualification',
            'department',
            'gpa',
            'cgpa',
            'level',
            'semester',
            'session',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:academicdata-detail'},
        }
        
    def create(self, validated_data):
        
        try:
            student = models.student.objects.get(id=validated_data['student'])
            if student.user.specialization:
                print("student.user.specialization:")
                print(student.user.specialization)
            validated_data['specialization'] = validated_data.get('specialization', student.user.specialization)
            validated_data['department'] = validated_data.get('department', student.user.specialization.department)
            
            # print("student.user.specialization:")
            # print(student.user.specialization)
        except Exception:
            # validated_data.update(specialization=student.user.specialization)
            # print("student.user.specialization:")
            # print(student.user.specialization)
            pass
        # print(datetime.today().year)
        try:
            validated_data['level'] = validated_data.get('level', amodels.Level.objects.create())
            
            print(validated_data['level'])
        except Exception:
            validated_data['level'] = validated_data.get('level', amodels.Level.objects.get(code=100))
            
        try:
            validated_data['session'] = validated_data.get('session', amodels.Session.objects.create())
            
            print(validated_data['session'])
        except Exception:
            validated_data['session'] = validated_data.get('session', amodels.Session.objects.get(year=str(datetime.today().year)))
            
        try:
            validated_data['start_date'] = validated_data.get('start_date', datetime.today().date())
            if validated_data['start_date'].year != datetime.today().year:
                diff = int(validated_data['session']) - int(validated_data['start_date'].year)
            
            print(validated_data['start_date'])
        except Exception:
            # validated_data['start_date'] = validated_data.get('start_date', amodels.Session.objects.get(year=str(datetime.today().year)))
            pass
        
        try:
            print(validated_data['specialization'].max_level.code)
            years = validated_data['specialization'].max_level.code / 100
            print(years)
            validated_data['end_date'] = validated_data['start_date'] + relativedelta(years=years) -relativedelta(months=3)
            
            print(validated_data['end_date'])
        except Exception:
            pass
        
        try:
            academic_data = super().create(validated_data)
        except Exception:
            academic_data = models.AcademicData.objects.create(**validated_data)
            
        return academic_data


class AcademicHistorySerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the AcademicHistory model"""

    biodata = serializers.PrimaryKeyRelatedField(
        queryset=models.Biodata.objects.all(),
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

    biodata = serializers.PrimaryKeyRelatedField(
        queryset=models.Biodata.objects.all(),
        allow_null=True,
        required=False,
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

    biodata = serializers.PrimaryKeyRelatedField(
        queryset=models.Biodata.objects.all(),
        allow_null=True,
        required=False,
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


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Result model"""

    course = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Course.objects.all(),
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=models.Student.objects.all(),
    )
    semester = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Semester.objects.all(),
        allow_null=True,
        required=False,
    )
    session = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Session.objects.all(),
        allow_null=True,
        required=False,
    )
    value = serializers.ReadOnlyField(source='get_value')
    grade = serializers.ReadOnlyField(source='get_grade')

    class Meta:
        model = models.Result
        fields = [
            'id',
            'url',
            'score',
            'course',
            'student',
            'value',
            'grade',
            'semester',
            'session',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:result-detail'},
        }


class ResultResponseSerializer(ResultSerializer):
    """serializer for the Result model"""

    course = aserializers.CourseSerializer(read_only=True)
    student = BaseStudentSerializer(read_only=True)
    semester = aserializers.SemesterSerializer(read_only=True)
    session = aserializers.SessionSerializer(read_only=True)


class CourseRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the CourseRegistration model"""

    course = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Course.objects.all(),
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=models.Student.objects.all(),
        allow_null=True,
        required=False,
    )
    session = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Session.objects.all(),
        allow_null=True,
        required=False,
    )
    semester = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Semester.objects.all(),
        allow_null=True,
        required=False,
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
        
    def create(self, validated_data):
        registration = None
        try:
            registration, created = models.CourseRegistration.objects.get_or_create(**validated_data)
            if not created:
                raise Exception("This course registration exists")
        except Exception as e:
            print(f"There was an exception creating course registration: {e}")
            raise Exception("This course is already registered")
        return registration


class CourseRegistrationResponseSerializer(CourseRegistrationSerializer):
    """serializer for the CourseRegistration model"""

    course = aserializers.CourseSerializer(read_only=True)
    student = BaseStudentSerializer(read_only=True)
    session = aserializers.SessionSerializer(read_only=True)
    semester = aserializers.SemesterSerializer(read_only=True)


class CourseAdviserSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the CourseAdviser model"""

    staff = serializers.PrimaryKeyRelatedField(
        queryset=models.Staff.objects.filter(is_active=True),
    )
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Specialization.objects.all(),
        allow_null=True,
        required=False,
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Department.objects.all(),
        allow_null=True,
        required=False,
    )
    level = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Level.objects.all(),
    )
    semester = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Semester.objects.all(),
        allow_null=True,
        required=False,
    )
    session = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Session.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.CourseAdviser
        fields = [
            'id',
            'url',
            'staff',
            'specialization',
            'department',
            'level',
            'semester',
            'session',
        ]
        extra_kwargs = {
            'url': {'view_name': 'user:courseadviser-detail'},
        }


class BiodataSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Biodata model"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
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
            'user': {'default': serializers.CurrentUserDefault()}
        }

    def create(self, validated_data):
        if 'academic_history' in validated_data:
            academic_history_data_list = validated_data.pop('academic_history')

        if 'health_data' in validated_data:
            health_data_data = validated_data.pop('health_data')

        if 'family_data' in validated_data:
            family_data_data = validated_data.pop('family_data')

        try:
            biodata = super().create(validated_data)
        except Exception:
            biodata = models.Biodata.objects.create(**validated_data)

        try:
            for academic_history_data in academic_history_data_list:
                academic_history_data['biodata'] = biodata
                models.AcademicHistory.objects.create(**academic_history_data)
        except Exception:
            pass

        try:
            health_data_data['biodata'] = biodata
            models.HealthData.objects.create(**health_data_data)
        except Exception:
            pass

        try:
            family_data_data['biodata'] = biodata
            models.FamilyData.objects.create(**family_data_data)
        except Exception:
            pass

        return biodata

    def update(self, instance, validated_data):
        if 'academic_history' in validated_data:
            academic_history_data_list = validated_data.pop('academic_history')

        if 'health_data' in validated_data:
            health_data_data = validated_data.pop('health_data')

        if 'family_data' in validated_data:
            family_data_data = validated_data.pop('family_data')

        biodata = super().update(instance, validated_data)

        # try:
        #     academic_history = instance.academic_history
        #     academic_history.institution = academic_history_data.get('institution', academic_history.institution)
        #     academic_history.start_date = academic_history_data.get('start_date', academic_history.start_date)
        #     academic_history.end_date = academic_history_data.get('end_date', academic_history.end_date)
        #     academic_history.save()
        # except Exception:
        #     pass
        
        try:
            nested_serializer = self.fields['academic_history']
            
            for academic_history_data in academic_history_data_list:
                nested_data = academic_history_data
                nested_data.update(biodata=biodata)
                try:
                    # nested_instance = instance.academic_history

                    # if nested_instance:
                    #     academic_history = nested_serializer.update(nested_instance, nested_data)
                    # else:
                    #     nested_data.update(biodata=biodata)
                    #     academic_history = nested_serializer.create(nested_data)
                    academic_history, created = models.AcademicHistory.objects.get_or_create(**nested_data)
                except Exception:
                    nested_data.update(biodata=biodata)
                    try:
                        academic_history = nested_serializer.create(nested_data)
                    except Exception:
                        academic_history = models.AcademicHistory.objects.create(**nested_data)
        except  Exception as e:
            # print(e)
            pass

        # try:
        #     health_data = instance.health_data
        #     health_data.blood_group = health_data_data.get('blood_group', health_data.blood_group)
        #     health_data.genotype = health_data_data.get('genotype', health_data.genotype)
        #     health_data.allergies = health_data_data.get('allergies', health_data.allergies)
        #     health_data.diabetes = health_data_data.get('diabetes', health_data.diabetes)
        #     health_data.STIs = health_data_data.get('STIs', health_data.STIs)
        #     health_data.heart_disease = health_data_data.get('heart_disease', health_data.heart_disease)
        #     health_data.disabilities = health_data_data.get('disabilities', health_data.disabilities)
        #     health_data.respiratory_problems = health_data_data.get(
        #         'respiratory_problems',
        #         health_data.respiratory_problems,
        #     )
        #     health_data.save()
        # except Exception:
        #     pass
        
        try:
            nested_data = health_data_data
                
            nested_serializer = self.fields['health_data']
            try:
                nested_instance = instance.health_data

                if nested_instance:
                    health_data = nested_serializer.update(nested_instance, nested_data)
                else:
                    nested_data.update(biodata=biodata)
                    health_data = nested_serializer.create(nested_data)
                    
            except Exception:
                nested_data.update(biodata=biodata)
                try:
                    health_data = nested_serializer.create(nested_data)
                except Exception:
                    health_data = models.HealthData.objects.create(**nested_data)
                # health_data = models.HealthData.objects.create(**nested_data)
        except  Exception as e:
            # print(e)
            pass

        # try:
        #     family_data = instance.family_data
        #     family_data.next_of_kin_full_name = family_data_data.get(
        #         'next_of_kin_full_name',
        #         instance.next_of_kin_full_name
        #     )
        #     family_data.next_of_kin_phone_no_1 = family_data_data.get(
        #         'next_of_kin_phone_no_1',
        #         instance.next_of_kin_phone_no_1
        #     )
        #     family_data.next_of_kin_phone_no_2 = family_data_data.get(
        #         'next_of_kin_phone_no_2',
        #         instance.next_of_kin_phone_no_2
        #     )
        #     family_data.next_of_kin_address = family_data_data.get(
        #         'next_of_kin_address',
        #         instance.next_of_kin_address
        #     )
        #     family_data.guardian_full_name = family_data_data.get(
        #         'guardian_full_name',
        #         instance.guardian_full_name
        #     )
        #     family_data.guardian_phone_no_1 = family_data_data.get(
        #         'guardian_phone_no_1',
        #         instance.guardian_phone_no_1
        #     )
        #     family_data.guardian_phone_no_2 = family_data_data.get(
        #         'guardian_phone_no_2',
        #         instance.guardian_phone_no_2
        #     )
        #     family_data.guardian_address = family_data_data.get(
        #         'guardian_address',
        #         instance.guardian_address
        #     )
        #     family_data.save()
        # except Exception:
        #     pass
        
        try:
            nested_data = family_data_data
                
            nested_serializer = self.fields['family_data']
            try:
                nested_instance = instance.family_data

                if nested_instance:
                    family_data = nested_serializer.update(nested_instance, nested_data)
                else:
                    nested_data.update(biodata=biodata)
                    family_data = nested_serializer.create(nested_data)
            except Exception:
                nested_data.update(biodata=biodata)
                try:
                    family_data = nested_serializer.create(nested_data)
                except Exception:
                    family_data = models.FamilyData.objects.create(**nested_data)
        except  Exception as e:
            # print(e)
            pass

        return biodata


class BiodataResponseSerializer(BiodataSerializer):
    """serializer for the Biodata model"""

    user = BaseUserSerializer(read_only=True)


class UserSerializer(BaseUserSerializer):
    """serializer for the User model"""

    biodata = BiodataSerializer(allow_null=True, required=False)
    staff = BaseStaffSerializer(source='staff_set', many=True, read_only=True)
    student = BaseStudentSerializer(source='student_set', many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        additional_fields = [
            'biodata',
            'staff',
            'student',
        ]
        fields = BaseUserSerializer.Meta.fields + additional_fields

    def create(self, validated_data):
        """create a new user with an encrypted password, a related biodata and return the user"""

        # if 'biodata' not in validated_data or validated_data['biodata'] == '':
        #     user = get_user_model().objects.create_user(**validated_data)
        # else:
        #     biodata_data = validated_data.pop('biodata')
        #     user = get_user_model().objects.create_user(**validated_data)
        #     models.Biodata.objects.create(user=user, **biodata_data)

        # if user.is_staff is True and len(user.staff_set.all()) == 0:
        #     models.Staff.objects.create(user=user)
        # # elif len(user.student_set.all) == 0:
        # #     student = models.Student.objects.create(user=user)
        # #     models.AcademicData.objects.create(student=student)
        
        try:
            nested_data = validated_data.pop('biodata')
            user = get_user_model().objects.create_user(**validated_data)
            # print(f"\n\n{user.check_password(validated_data['password'])}\n\n")
            nested_data.update(user=user)
            nested_serializer = self.fields['biodata']
            # biodata = models.Biodata.objects.create(**nested_data, user=user)
            try:
                biodata = nested_serializer.create(nested_data)
                print("Biodata created using biodata serializer", f"biodata: {biodata}")
            except Exception as e:
                biodata = models.Biodata.objects.create(**nested_data)
                print(f"biodata: {biodata}")
            # validated_data['biodata'] = biodata
            # return user
        except  Exception as e:
            # print(e)
            user = get_user_model().objects.create_user(**validated_data)
            
        if user.is_staff is True and len(user.staff_set.all()) == 0:
            models.Staff.objects.create(user=user)
        else:
            models.Student.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        """update a user, correctly setting the password and return it"""

        # if 'biodata' not in validated_data or validated_data['biodata'] == []:
        #     password = validated_data.pop('password')
        #     user = super().update(instance, validated_data)
        # else:
        #     biodata_data = validated_data.pop('biodata')
        #     password = validated_data.pop('password')
        #     user = super().update(instance, validated_data)

        #     try:
        #         biodata = models.Biodata.objects.get(user=user)
        #         # print("\nBiodata exists")
        #         biodata.marital_status = biodata_data.get('marital_status', biodata.marital_status)
        #         biodata.gender = biodata_data.get('gender', biodata.gender)
        #         biodata.religion = biodata_data.get('religion', biodata.religion)
        #         biodata.birthday = biodata_data.get('birthday', biodata.birthday)
        #         biodata.nationality = biodata_data.get('nationality', biodata.nationality)
        #         biodata.state_of_origin = biodata_data.get('state_of_origin', biodata.state_of_origin)
        #         biodata.local_govt = biodata_data.get('local_govt', biodata.local_govt)
        #         biodata.permanent_address = biodata_data.get(
        #             'permanent_address',
        #             biodata.permanent_address,
        #         )
        #         biodata.address = biodata_data.get('address', biodata.address)
        #         biodata.phone_no_1 = biodata_data.get('phone_no_1', biodata.phone_no_1)
        #         biodata.phone_no_2 = biodata_data.get('phone_no_2', biodata.phone_no_2)
        #         biodata.profile_picture = biodata_data.get('profile_picture', biodata.profile_picture)
        #         biodata.academic_history = biodata_data.get('academic_history', biodata.academic_history)
        #         biodata.health_data = biodata_data.get('health_data', biodata.health_data)
        #         biodata.family_data = biodata_data.get('family_data', biodata.family_data)
        #         biodata.save()
        #     except Exception:
        #         # print("\nBiodata doesn't exist")
        #         biodata = models.Biodata.objects.create(user=user, **biodata_data)

        # if password:
        #     user.set_password(password)
        #     user.save()

        # if user.is_staff is True:
        #     try:
        #         models.Staff.objects.get(user=user)
        #     except Exception:
        #         models.Staff.objects.create(user=user)

        # return user
        
        password = validated_data.pop('password') if 'password' in validated_data else False
        # print(password)
        # try:
        #     password = validated_data.pop('password')
        # except Exception:
        #     pass
        
        try:
            print("started")
            nested_data = validated_data.pop('biodata')
            user = super().update(instance, validated_data)
                
            nested_serializer = self.fields['biodata']
            # print(f"nested serializer: {nested_serializer.data}")
            try:
                nested_instance = instance.biodata
                print("code not broke")
                # nested_data = validated_data['biodata']  # this may throw an exception, as `academic_data` is part of `validated_data`
                if nested_instance:
                    print("nested instance exists")
                    print(nested_instance)
                    biodata = nested_serializer.update(nested_instance, nested_data)
                # else:
                #     # nested_data.update(user=user)
                #     print("nested instance not found")
                #     nested_data['user'] = user
                #     biodata = models.Biodata.objects.create(**nested_data)
                #     print("biodata created")
                #     # biodata = nested_serializer.create(nested_data)
            except Exception:
                # nested_data.update(user=user)
                print("nested instance not found")
                nested_data['user'] = user
                try:
                    biodata = nested_serializer.create(nested_data)
                except Exception:
                    biodata = models.Biodata.objects.create(**nested_data)
                # biodata = models.Biodata.objects.create(**nested_data)
                print("biodata created")
                # biodata = nested_serializer.create(nested_data)

            # validated_data['academic_data'] = academic_data
            
            # biodata = models.Biodata.objects.create(**validated_data['biodata'], user=user)
            # print(f"biodata: {biodata}")
            # # validated_data['biodata'] = biodata

        except  Exception as e:
            # print(e)
            user = super().update(instance, validated_data)
            
        # print(f"updated user: {user}")
        # print(f"updated user password: {password}")
            
        if password:
            user.set_password(password)
            user.save()
                
        return user


class UserResponseSerializer(UserSerializer):

    specialization = aserializers.SpecializationResponseSerializer(read_only=True)


class StaffSerializer(BaseStaffSerializer):
    """serializer for the Staff model"""

    courses = aserializers.CourseSerializer(source='course_set', many=True, read_only=True)
    user = UserSerializer()
    department = serializers.ReadOnlyField()
    faculty = serializers.ReadOnlyField()

    class Meta(BaseStaffSerializer.Meta):
        additional_fields = [
            'courses',
            'department',
            'faculty',
        ]
        fields = BaseStaffSerializer.Meta.fields + additional_fields

    def create(self, validated_data):
        """create a new user with an encrypted password, a related user and return the user"""
        # try:
        #     new_user_data = validated_data.pop("new_user")
        #     new_user = get_user_model().objects.create_user(**new_user_data)

        #     user = validated_data.pop("user") if "user" in validated_data else None
        #     # if validated_data["user"]: user = validated_data.pop("user")
        #     # print(user)
        #     if user and new_user:
        #         print("\nBoth user and new_user provided. Only user is used!")
        #         staff = models.Staff.objects.create(user=user, **validated_data)
        #     else:
        #         staff = models.Staff.objects.create(user=new_user, **validated_data)

        #     if staff.user and staff.specialization and not new_user.specialization:
        #         new_user.specialization = staff.specialization
        #         new_user.save()

        # except Exception:
        #     print("\nnew_user not provided")
        #     staff = models.Staff.objects.create(**validated_data)
        
        # user = models.User(**validated_data['user'])
        # user.save()
        try:
            staff_id = setup.generate_staff_id()
            if not staff_id:
                raise Exception("Staff id generation failed")
            validated_data["staff_id"] = staff_id
        except Exception as e:
            print(e)

        try:
            user = get_user_model().objects.create_user(**validated_data['user'])
            validated_data['user'] = user
        except  Exception as e:
            # print(e)
            pass
            
        # try:
        #     specialization = amodels.Specialization.objects.create(**validated_data['specialization'])
        #     validated_data['specialization'] = specialization
        # except  Exception as e:
        #     # print(e)
        #     pass
            
        return super().create(validated_data)
        

        # return staff

    def update(self, instance, validated_data):
        """update a user, correctly setting the password and return it"""

        # if 'new_user' not in validated_data or validated_data['new_user'] == []:
        #     staff = super().update(instance, validated_data)
        # elif 'user' in validated_data:

        #     new_user_data = validated_data.pop('new_user')
        #     print("\nremoved new user data, user provided in request")
        #     staff = super().update(instance, validated_data)
        # else:

        #     new_user_data = validated_data.pop('new_user')
        #     password = new_user_data.pop('password')

        #     staff = super().update(instance, validated_data)
        #     user = staff.user

        #     try:
        #         user.first_name = new_user_data.get('first_name', user.first_name)
        #         user.middle_name = new_user_data.get('middle_name', user.middle_name)
        #         user.last_name = new_user_data.get('last_name', user.last_name)
        #         user.email = new_user_data.get('email', user.email)
        #         user.is_staff = new_user_data.get('is_staff', user.is_staff)

        #         if staff.user and staff.specialization and not user.specialization:
        #             user.specialization = staff.specialization

        #         if password:
        #             user.set_password(password)

        #         user.save()

        #     except Exception as e:
        #         print(f"\nThere was an error updating user: {e}")
        try:
            nested_serializer = self.fields['user']
            nested_instance = instance.user
            nested_data = validated_data['user']  # this may throw an exception, as `user` is part of `validated_data`
            user = nested_serializer.update(nested_instance, nested_data)
            validated_data['user'] = user
        except  Exception as e:
            # print(e)
            pass
            
        # try:
        #     nested_serializer = self.fields['specialization']
        #     nested_instance = instance.specialization
        #     nested_data = validated_data['specialization']  # this may throw an exception, as `specialization` is part of `validated_data`
        #     specialization = nested_serializer.update(nested_instance, nested_data)
        #     validated_data['specialization'] = specialization
        # except  Exception as e:
        #     # print(e)
        #     pass
        
        return super().update(instance, validated_data)

        # return staff


class StaffResponseSerializer(StaffSerializer):

    specialization = aserializers.SpecializationResponseSerializer(read_only=True)


class CourseAdviserResponseSerializer(CourseAdviserSerializer):
    """serializer for the CourseAdviser model"""

    staff = StaffSerializer(read_only=True)
    specialization = aserializers.SpecializationSerializer(read_only=True)
    department = aserializers.DepartmentSerializer(read_only=True)
    level = aserializers.LevelSerializer(read_only=True)
    semester = aserializers.SemesterSerializer(read_only=True)
    session = aserializers.SessionSerializer(read_only=True)


class StudentSerializer(BaseStudentSerializer):
    """serializer for the Student model"""

    user = UserSerializer()
    academic_data = AcademicDataSerializer(required=False, allow_null=True)
    results = ResultResponseSerializer(source='result_set', many=True, read_only=True)
    course_registrations = CourseRegistrationResponseSerializer(source='courseregistration_set', many=True, read_only=True)
    registered_quizes = qserializers.QuizTakerResponseSerializer(source='quiztaker_set', many=True, read_only=True)
    registered_assignments = qserializers.AssignmentTakerResponseSerializer(source='assignmenttaker_set', many=True, read_only=True)
    notices = iserializers.NoticeResponseSerializer(many=True, read_only=True)
    information = iserializers.InformationResponseSerializer(many=True, read_only=True)

    class Meta(BaseStudentSerializer.Meta):
        additional_fields = [
            'academic_data',
            'results',
            'course_registrations',
            'registered_quizes',
            'registered_assignments',
            'notices',
            'information',
        ]
        fields = BaseStudentSerializer.Meta.fields + additional_fields

    def create(self, validated_data):
        """create a new user with an encrypted password, a related user and return the user"""
        
        try:
            user = get_user_model().objects.create_user(**validated_data['user'])
            # print(f"user: {user}")
            validated_data['user'] = user
        except  Exception as e:
            # print(e)
            pass
            
        try:
            academic_data_data = validated_user.pop('academic_data')
        except Exception:
            pass
        
        try:
            student_id = setup.generate_student_id()
            if not student_id:
                raise Exception("Student id generation failed")
            validated_data["student_id"] = student_id
        except Exception as e:
            print(e)
        
        student = super().create(validated_data)
        
        try:
            matric_no = setup.generate_student_matric(student)
            if not matric_no:
                raise Exception("Matric no generation failed")
            student.matric_no = matric_no
            student.save()
        except Exception as e:
            print(e)
            
        try:
            # validated_user.pop('academic_data')
            academic_data_data['student'] = student
            academic_data = models.AcademicData.objects.create(**academic_data_data)
            # print(f"academic_data: {academic_data}")
            validated_data['academic_data'] = academic_data
        except  Exception as e:
            # print(e)
            pass
            
        # return super().create(validated_data)

        return student

    def update(self, instance, validated_data):
        """update a user, correctly setting the password and return it"""
        
        try:
            nested_serializer = self.fields['user']
            nested_instance = instance.user
            nested_data = validated_data['user']  # this may throw an exception, as `user` is part of `validated_data`
            user = nested_serializer.update(nested_instance, nested_data)
            validated_data['user'] = user
        except  Exception as e:
            # print(e)
            pass
            
        # try:
        #     nested_serializer = self.fields['specialization']
        #     nested_instance = instance.specialization
        #     nested_data = validated_data['specialization']  # this may throw an exception, as `specialization` is part of `validated_data`
        #     specialization = nested_serializer.update(nested_instance, nested_data)
        #     validated_data['specialization'] = specialization
        # except  Exception as e:
        #     # print(e)
        #     pass
        
        try:
            nested_serializer = self.fields['academic_data']
            nested_data = validated_data.pop('academic_data')  # this may throw an exception, as `academic_data` is part of `validated_data`
            student = super().update(instance, validated_data)
            

            try:
                if student.user.specialization:
                    print("student.user.specialization:")
                    print(student.user.specialization)
                nested_data['specialization'] = nested_data.get('specialization', student.user.specialization)
                nested_data['department'] = nested_data.get('department', student.user.specialization.department)
                
                # print("student.user.specialization:")
                # print(student.user.specialization)
            except Exception:
                # nested_data.update(specialization=student.user.specialization)
                # print("student.user.specialization:")
                # print(student.user.specialization)
                pass
            # print(datetime.today().year)
            try:
                nested_data['level'] = nested_data.get('level', amodels.Level.objects.create())
            except Exception:
                nested_data['level'] = nested_data.get('level', amodels.Level.objects.get(code=100))
            print(nested_data['level'])
            try:
                nested_data['session'] = nested_data.get('session', amodels.Session.objects.create())
            except Exception:
                nested_data['session'] = nested_data.get('session', amodels.Session.objects.get(year=str(datetime.today().year)))
            print(nested_data['session'])
            try:
                nested_data['start_date'] = nested_data.get('start_date', datetime.today().date())
                if nested_data['start_date'].year != datetime.today().year:
                    diff = int(nested_data['session']) - int(nested_data['start_date'].year)
            except Exception:
                # nested_data['start_date'] = nested_data.get('start_date', amodels.Session.objects.get(year=str(datetime.today().year)))
                pass
            print(nested_data['start_date'])
            print(nested_data['specialization'].max_level.code)
            try:
                years = nested_data['specialization'].max_level.code / 100
                print(years)
                nested_data['end_date'] = nested_data['start_date'] + relativedelta(years=years) -relativedelta(months=3)
            except Exception:
                pass
            print(nested_data['end_date'])
            
            
            try:
                nested_instance = instance.academic_data
                academic_data = nested_serializer.update(nested_instance, nested_data)
            except Exception:
                nested_data['student'] = student
                try:
                    academic_data = nested_serializer.create(nested_data)
                except Exception: 
                    academic_data = models.AcademicData.objects.create(**nested_data)
                
            validated_data['academic_data'] = academic_data
        except  Exception as e:
            # print(e)
            student = super().update(instance, validated_data)
        
        # return super().update(instance, validated_data)

        return student


class AcademicDataResponseSerializer(AcademicDataSerializer):
    """serializer for the AcademicData model"""

    student = BaseStudentSerializer(read_only=True)
    specialization = aserializers.SpecializationResponseSerializer(read_only=True)
    department = aserializers.DepartmentResponseSerializer(read_only=True)
    level = aserializers.LevelSerializer(read_only=True)
    semester = aserializers.SemesterSerializer(read_only=True)
    session = aserializers.SessionSerializer(read_only=True)
    course_adviser = CourseAdviserResponseSerializer(read_only=True)
    
    class Meta(AcademicDataSerializer.Meta):
        additional_fields = [
            'course_adviser',
        ]
        fields = AcademicDataSerializer.Meta.fields + additional_fields


class StudentBaseResponseSerializer(StudentSerializer):
    """serializer for the Student model"""

    academic_data = AcademicDataResponseSerializer(read_only=True)


class StudentResponseSerializer(StudentSerializer):

    academic_data = AcademicDataResponseSerializer(read_only=True)
    specialization = aserializers.SpecializationResponseSerializer(read_only=True)


class AccountSerializer(BaseUserSerializer):
    biodata = BiodataSerializer(required=False, allow_null=True)
    staff = StaffSerializer(source='staff_set', many=True, read_only=True)
    student = StudentBaseResponseSerializer(source='student_set', many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        additional_fields = [
            'biodata',
            'staff',
            'student',
        ]
        fields = BaseUserSerializer.Meta.fields + additional_fields
    
    def update(self, instance, validated_data):
        """update a user, correctly setting the password and return it"""
        
        password = validated_data.pop('password') if 'password' in validated_data else False
        
        try:
            nested_data = validated_data.pop('biodata')
            user = super().update(instance, validated_data)
                
            nested_serializer = self.fields['biodata']
            try:
                nested_instance = instance.biodata
                print("code not broke")
                # nested_data = validated_data['biodata']  # this may throw an exception, as `academic_data` is part of `validated_data`
                # if nested_instance:
                #     # print("nested instance exists")
                #     # print(nested_instance)
                #     biodata = nested_serializer.update(nested_instance, nested_data)
                biodata = nested_serializer.update(nested_instance, nested_data)

            except Exception:
                # nested_data.update(user=user)
                # print("nested instance not found")
                nested_data['user'] = user
                try:
                    biodata = nested_serializer.create(nested_data)
                except Exception:
                    biodata = models.Biodata.objects.create(**nested_data)
                # print("biodata created")

        except  Exception as e:
            # print(e)
            user = super().update(instance, validated_data)
            
        # print(f"updated user: {user}")
        # print(f"updated user password: {password}")
            
        if password:
            user.set_password(password)
            user.save()
                
        return user


class AccountResponseSerializer(AccountSerializer):

    staff = StaffResponseSerializer(source='staff_set', many=True, read_only=True)
    student = StudentResponseSerializer(source='student_set', many=True, read_only=True)
    specialization = aserializers.SpecializationSerializer(read_only=True)


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
        operation_description='login',
        operation_summary='login',
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
        operation_description='generata access token using refresh token',
        operation_summary='generata access token using refresh token',
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
        operation_description='verify access token is still valid',
        operation_summary='verify access token is still valid',
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
