"""SMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from SMS.schema import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls', namespace='core')),
    path('api-auth/', include('rest_framework.urls')),
    path("information/", include('information.urls', namespace='information')),
    path("assessment/", include('assessment.urls', namespace='assessment')),
    path("academics/", include('academics.urls', namespace='academics')),
    path("user/", include('user.urls', namespace='user')),

    # For drf-yasg
    path("swagger(<format>\\.json|\\.yaml)", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # For django-rest-passwordreset
    path("password_reset/", include('django_rest_passwordreset.urls', namespace='password_reset')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
