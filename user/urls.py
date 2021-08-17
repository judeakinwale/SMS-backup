from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as JWTViews
from user import views


app_name = 'user'

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('staff', views.StaffViewSet)
router.register('student', views.StudentViewSet)
router.register('biodata', views.BiodataViewSet)
router.register('academic_data', views.AcademicDataViewSet)
router.register('academic_history', views.AcademicHistoryViewSet)
router.register('health_data', views.HealthDataViewSet)
router.register('family_data', views.FamilyDataViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('account/', views.ManageUserApiView.as_view(), name="account"),
    path("token/", JWTViews.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/verify", JWTViews.TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh", JWTViews.TokenRefreshView.as_view(), name="token_refresh"),
]
