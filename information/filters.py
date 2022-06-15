from django_filters import rest_framework as filters
from information import models


class InformationFilter(filters.FilterSet):

    class Meta:
        model = models.Information
        fields = {
            'source__id': ['exact'],
            'scope__id': ['exact'],
            'source__first_name': ['icontains', 'exact'],
            'source__last_name': ['icontains', 'exact'],
            'source__email': ['icontains'],
            'scope__description': ['icontains'],
            'title': ['icontains'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class NoticeFilter(filters.FilterSet):

    class Meta:
        model = models.Notice
        fields = {
            'source__id': ['exact'],
            'scope__id': ['exact'],
            'source__first_name': ['icontains'],
            'source__last_name': ['icontains'],
            'source__email': ['icontains'],
            'scope__description': ['icontains'],
            'title': ['icontains'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class InformationImageFilter(filters.FilterSet):

    class Meta:
        model = models.InformationImage
        fields = {
            'information__id': ['exact'],
            'information__title': ['icontains'],
            'description': ['icontains'],
            'timestamp': ['exact', 'lt', 'gt'],
        }
