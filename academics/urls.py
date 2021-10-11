from django.urls import path, include
from rest_framework.routers import DefaultRouter
from academics import views

app_name = 'academics'

router = DefaultRouter()
router.register('faculty', views.FacultyViewSet)
router.register('department', views.DepartmentViewSet)
router.register('specialization', views.SpecializationViewSet)
router.register('course', views.CourseViewSet)
router.register('level', views.LevelViewSet)
router.register('semester', views.SemesterViewSet)
router.register('session', views.SessionViewSet)
router.register('recommended_courses', views.RecommendedCoursesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
