from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="School Management System API",
        default_version='v0.5',
        description="School management system",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="judeakinwale@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
