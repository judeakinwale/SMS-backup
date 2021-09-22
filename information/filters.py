from django_filters import rest_framework as filters
from information import models


class InformationFilter(filters.FilterSet):
    # source__first_name = filters.CharFilter(lookup_expr='icontains')
    # source__last_name = filters.CharFilter(lookup_expr='icontains')
    # source__email = filters.CharFilter(lookup_expr='icontains')
    # scope__description = filters.CharFilter(lookup_expr='icontains')
    # title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Information
        # fields = [
        #     'source__first_name',
        #     'source__last_name',
        #     'source__email',
        #     'scope__description',
        #     'title',
        #     'timestamp'
        # ]

        fields = {
            'source__first_name': ['icontains'],
            'source__last_name': ['icontains'],
            'source__email': ['icontains'],
            'scope__description': ['icontains'],
            'title': ['icontains'],
            'timestamp': ['exact', 'lt', 'gt'],
        }


class NoticeFilter(filters.FilterSet):
    # source__first_name = filters.CharFilter(lookup_expr='icontains')
    # source__last_name = filters.CharFilter(lookup_expr='icontains')
    # source__email = filters.CharFilter(lookup_expr='icontains')
    # scope__description = filters.CharFilter(lookup_expr='icontains')
    # title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Notice
        fields = {
            'source__first_name': ['icontains'],
            'source__last_name': ['icontains'],
            'source__email': ['icontains'],
            'scope__description': ['icontains'],
            'title': ['icontains'],
        }


class InformationImageFilter(filters.FilterSet):
    # information__title = filters.CharFilter(lookup_expr='icontains')
    # description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.InformationImage
        fields = {
            'information__title': ['icontains'],
            'description': ['icontains'],
            'timestamp': ['exact', 'lt', 'gt'],
        }
