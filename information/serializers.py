from rest_framework import serializers
from django.contrib.auth import get_user_model
from information import models
from academics import models as amodels


class InformationImageSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the InformationImage model"""

    information = serializers.PrimaryKeyRelatedField(
        queryset=models.Information.objects.all(),
        # view_name='information:information-detail',
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

    source = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        allow_null=True,
        required=False
    )
    scope = serializers.PrimaryKeyRelatedField(
        queryset=models.Scope.objects.all(),
        # view_name='information:scope-detail',
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

        # if ('images' not in validated_data) or validated_data['images'] == []:
        #     information = super().create(validated_data)
        # else:
        #     images_data = validated_data.pop('images')
        #     information = super().create(validated_data)
        #     for data in images_data:
        #         data['information'] = information
        #         models.InformationImage.objects.create(**data)
                
        try:
            images_data = validated_data.pop('images')
            information =  super().create(validated_data)
            for data in images_data:
                data['information'] = information
                models.InformationImage.objects.create(**data)
        except Exception:
            information =  super().create(validated_data)

        return information

    def update(self, instance, validated_data):
        """extend the default update serializer method"""

        # if ('images' not in validated_data) or validated_data['images'] == []:
        #     information = super().update(instance, validated_data)
        # else:
        #     images = (instance.images).all()
        #     list_images = list(images)
        #     images_data = validated_data.pop('images')
        #     information = super().update(instance, validated_data)

        #     if list_images == []:
        #         for data in images_data:
        #             data['information'] = information
        #             models.InformationImage.objects.create(**data)
        #     else:
        #         n = 0
        #         for data in images_data:
        #             try:
        #                 image = images[n]
        #                 n += 1
        #                 image.image = data.get('image', image.image)
        #                 image.description = data.get('description', image.description)
        #                 image.save()
        #             except Exception:
        #                 data['information'] = information
        #                 models.InformationImage.objects.create(**data)
                        
        try:
            images_data_list = validated_data.pop('images')
            print("started")
            information = super().update(instance, validated_data)
            # url = super()(information).data['url']
            n = 0
            for image_data in images_data_list:
                nested_data = image_data
                # nested_data.update(information=information)
                    
                nested_serializer = self.fields['images']
                # print(instance.images.all()[n])
                
                
                try:
                    print(f'continued, n is {n}')
                    nested_instance = instance.images.all()[n]
                    print("nested image exists")
                    images = InformationImageSerializer.update(self, nested_instance, nested_data)
                    print("Image created")
                except Exception as e:
                    print(f"There was an exception: {e}")
                    nested_data.update(information=information)
                    # print(super().list())
                    # images = nested_serializer.create(nested_data)
                    # images = InformationImageSerializer.create(self, nested_data)
                    images = models.InformationImage.objects.create(**nested_data)
                    print("new image created instead")

                # if nested_instance:
                #     images = nested_serializer.update(nested_instance, nested_data)
                # else:
                #     images = nested_serializer.create(nested_data)
                
                n += 1
        except  Exception as e:
            # print(f"There was an exception: {e}")
            information = super().update(instance, validated_data)

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
        # view_name='information:scope-detail',
    )

    class Meta:
        model = models.Notice
        fields = ['id', 'url', 'title', 'message', 'source', 'scope']
        extra_kwargs = {
            'url': {'view_name': 'information:notice-detail'}
        }


class ScopeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Scope model"""

    faculty = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Faculty.objects.all(),
        # view_name='academics:faculty-detail',
        allow_null=True,
        required=False,
    )
    departmment = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Department.objects.all(),
        # view_name='academics:departmment-detail',
        allow_null=True,
        required=False,
    )
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Specialization.objects.all(),
        # view_name='academics:specialization-detail',
        allow_null=True,
        required=False,
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Course.objects.all(),
        # view_name='academics:course-detail',
        allow_null=True,
        required=False,
    )
    level = serializers.PrimaryKeyRelatedField(
        queryset=amodels.Level.objects.all(),
        # view_name='academics:level-detail',
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
            'specialization',
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
