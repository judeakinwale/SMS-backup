from rest_framework import serializers
from django.contrib.auth import get_user_model
from information import models
from academics import models as amodels


class InformationImageSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the InformationImage model"""

    information = serializers.PrimaryKeyRelatedField(
        queryset=models.Information.objects.all(),
        allow_null=True, required=False,
    )

    class Meta:
        model = models.InformationImage
        fields = [
            'id',
            'url',
            'information',
            'image',
            'description',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:informationimage-detail'}
        }


class InformationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Information model"""

    source = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        allow_null=True,
        required=False
    )
    scope = serializers.PrimaryKeyRelatedField(
        queryset=models.Scope.objects.all(),
    )
    images = InformationImageSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = models.Information
        lookup_field = 'id'
        fields = [
            'id',
            'url',
            'title',
            'body',
            'images',
            'source',
            'scope',
            'timestamp'
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:information-detail'},
        }

    def create(self, validated_data):
        """extend the default create serializer method"""

        information = None  # avoid errors in the except block
        try:
            images_data = validated_data.pop('images')
            information =  super().create(validated_data)
            for data in images_data:
                data['information'] = information
                models.InformationImage.objects.get_or_create(**data)
        except Exception:
            # check if information created in try block to avoid duplication
            information =  super().create(validated_data) if not information else information 

        return information

    def update(self, instance, validated_data):
        """extend the default update serializer method"""

        information = None  # avoid errors in the except block
        try:
            if "images" not in validated_data:
                raise Exception("No images provided")
            images_data = validated_data.pop('images')
            information = super().update(instance, validated_data)

            for image_data in images_data:
                nested_data = image_data
                nested_data['information'] = information
                images = None
                try:
                    images = models.InformationImage.objects.filter(**nested_data)
                    image, created = models.InformationImage.objects.get_or_create(**nested_data)
                except Exception as e:
                    if not images:
                        raise Exception(e)
        except  Exception as e:
            print(f"There was an exception updating images: {e}")
            information = super().update(instance, validated_data) if not information else information

        return information


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Notice model"""

    source = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        allow_null=True,
        required=False
    )
    scope = serializers.PrimaryKeyRelatedField(
        queryset=models.Scope.objects.all(),
    )

    class Meta:
        model = models.Notice
        fields = ['id', 'url', 'title', 'message', 'source', 'scope', 'timestamp']
        extra_kwargs = {
            'url': {'view_name': 'information:notice-detail'}
        }


class ScopeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Scope model"""

    faculty = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Faculty.objects.all(),
        allow_null=True, required=False,
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Department.objects.all(),
        allow_null=True, required=False,
    )
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Specialization.objects.all(),
        allow_null=True, required=False,
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Course.objects.all(),
        allow_null=True, required=False,
    )
    level = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Level.objects.all(),
        allow_null=True, required=False,
    )
    information_set = InformationSerializer(many=True, read_only=True)
    notice_set = NoticeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Scope
        fields = [
            'id',
            'url',
            'faculty',
            'department',
            'specialization',
            'course',
            'level',
            'description',
            'is_general',
            'is_first_year',
            'is_final_year',
            'information_set',
            'notice_set',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:scope-detail'}
        }


class ScopeStringRelatedSerializer(ScopeSerializer):
    """serializer for the Scope model"""

    faculty = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    specialization = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    level = serializers.StringRelatedField()


class InformationResponseSerializer(InformationSerializer):

    # source = UserSerializer(read_only=True)
    # scope = ScopeSerializer(read_only=True)
    scope = ScopeStringRelatedSerializer(read_only=True)


class NoticeResponseSerializer(NoticeSerializer):

    # source = UserSerializer(read_only=True)
    # scope = ScopeSerializer(read_only=True)
    scope = ScopeStringRelatedSerializer(read_only=True)
