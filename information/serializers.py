from rest_framework import serializers
from django.contrib.auth import get_user_model
from information import models
from academics import models as amodels


class InformationImageSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the InformationImage model"""

    information = serializers.HyperlinkedRelatedField(
        queryset=models.Information.objects.all(),
        view_name='information:information-detail',
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.InformationImage
        fields = [
            'id',
            'url',
            'information',
            'image',
            'description',
            'timestamp'
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:informationimage-detail'}
        }


class InformationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Information model"""

    source = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), allow_null=True, required=False)
    scope = serializers.HyperlinkedRelatedField(
        queryset=models.Scope.objects.all(),
        view_name='information:scope-detail',
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
        # try:
        #     images_data = validated_data.pop('images')
        # except:
        #     pass
        
        if ('images' not in validated_data) or validated_data['images'] == []:
            information = super().create(validated_data)
            # print("1")
        else:
            # print("2")
            images_data = validated_data.pop('images')
            information = super().create(validated_data)
            # print(images_data)
            for data in images_data:
                data['information'] = information
                image = models.InformationImage.objects.create(**data)
                # print(data)

        # if "title" in validated_data:
        #     print(validated_data["title"])

        # if "images" in validated_data:
        #     print(validated_data["images"])

        # if 'images' in validated_data:
        #     print("1")
        #     images_data = validated_data.pop('images')
        #     information = super().create(validated_data)
        #     print(images_data)
        #     for data in images_data:
        #         print("3")
        #         data['information'] = information
        #         image = models.InformationImage.objects.create(**data)
        #         print(data)
        # else:
        #     print("4")
        #     information = super().create(validated_data)
        
        return information

    def update(self, instance, validated_data):
        if ('images' not in validated_data) or validated_data['images'] == []:
            # instance.title = validated_data.get('title', instance.title) 
            # instance.body = validated_data.get('body', instance.title) 
            # instance.images = validated_data.get('images', instance.title) 
            # instance.source = validated_data.get('source', instance.title) 
            # instance.scope = validated_data.get('scope', instance.title) 
            information = super().update(instance, validated_data)
        else:
            images = (instance.images).all()
            list_images = list(images)
            images_data = validated_data.pop('images')
            information = super().update(instance, validated_data)

            # print(list_images)

            if list_images == []:
                for data in images_data:
                    data['information'] = information
                    models.InformationImage.objects.create(**data)
            else:
                n = 0
                # print(images)
                for data in images_data:
                    # data['information'] = information
                    # image = images.pop(0)
                    image = images[n]
                    n += 1
                    image.image = data.get('image', image.image)
                    image.description = data.get('description', image.description)
                    image.save()
                    # image = models.InformationImage.objects.create(**data)
        
        return information
        # return super().update(instance, validated_data)

class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Notice model"""

    source = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), allow_null=True, required=False)
    scope = serializers.HyperlinkedRelatedField(
        queryset=models.Scope.objects.all(),
        view_name='information:scope-detail',
    )

    class Meta:
        model = models.Notice
        fields = ['id', 'url', 'title', 'message', 'source', 'scope']
        extra_kwargs = {
            'url': {'view_name': 'information:notice-detail'}
        }


class ScopeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Scope model"""

    faculty = serializers.HyperlinkedRelatedField(
        queryset=amodels.Faculty.objects.all(),
        view_name='academics:faculty-detail',
        allow_null=True,
        required=False,
    )
    departmment = serializers.HyperlinkedRelatedField(
        queryset=amodels.Department.objects.all(),
        view_name='academics:departmment-detail',
        allow_null=True,
        required=False,
    )
    programme = serializers.HyperlinkedRelatedField(
        queryset=amodels.Programme.objects.all(),
        view_name='academics:programme-detail',
        allow_null=True,
        required=False,
    )
    course = serializers.HyperlinkedRelatedField(
        queryset=amodels.Course.objects.all(),
        view_name='academics:course-detail',
        allow_null=True,
        required=False,
    )
    level = serializers.HyperlinkedRelatedField(
        queryset=amodels.Level.objects.all(),
        view_name='academics:level-detail',
        allow_null=True,
        required=False,
    )
    information_set = InformationSerializer(many=True, allow_null=True, required=False)
    notice_set = NoticeSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = models.Scope
        fields = [
            'id',
            'url',
            'faculty',
            'departmment',
            'programme',
            'course',
            'level',
            'description',
            'is_general',
            'is_first_year',
            'is_final_year',
            'information_set',
            'notice_set',
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:scope-detail'}
        }
