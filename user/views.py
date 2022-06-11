from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, permissions
from rest_framework import status, views, response
from rest_framework_simplejwt.views import (
  TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from user import serializers, models, filters
from core import permissions as cpermissions
from core import utils, mixins

from django_rest_passwordreset.signals import reset_password_token_created
from drf_yasg.utils import no_body, swagger_auto_schema
# For django rest password reset
# TODO: Add link to drf password reset documentation
from django_rest_passwordreset.views import (
    ResetPasswordValidateTokenViewSet, 
    ResetPasswordConfirmViewSet,
    ResetPasswordRequestTokenViewSet
)

# Create your views here.


class UserViewSet(mixins.swagger_documentation_factory("user with biodata"), viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    serializer_action_classes = {
        'list': serializers.UserResponseSerializer,
        'retrieve': serializers.UserResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsITDept
    ]
    filterset_class = filters.UserFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        # TODO: Refactor account creation mail logic
        user = serializer.save()
        try:
            reciepients = [user.email, ]
            context = {
                "user": user,
                "school_name": "UNI",
                "login_url": "https://sms-lotus.herokuapp.com/api-auth/login/"
            }
            utils.send_account_creation_email(self.request, reciepients, context)
        except Exception as e:
            print(f"user creation email error: {e} \n")

        return user


class ManageUserApiView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    queryset = get_user_model().objects.all()
    serializer_class = serializers.AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = filters.UserFilter

    def get_object(self):
        """retrieve and return the authenticated user"""
        return self.request.user
    
    @swagger_auto_schema(
        operation_description="retrieve authenticated user details",
        operation_summary='retrieve authenticated user details (account)'
    )
    def get(self, request, *args, **kwargs):
        """get method docstring"""
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update authenticated user details and update or create biodata",
        operation_summary='update authenticated user details (account) and update or create biodata'
    )
    def put(self, request, *args, **kwargs):
        """put method docstring"""
        try:
            return super().put(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="partial update authenticated user details and update or create biodata",
        operation_summary='partial update authenticated user details (account) and update or create biodata'
    )
    def patch(self, request, *args, **kwargs):
        """patch method docstring"""
        try:
            return super().patch(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


class StaffViewSet(mixins.swagger_documentation_factory("staff with user"), viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    serializer_action_classes = {
        'list': serializers.StaffResponseSerializer,
        'retrieve': serializers.StaffResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsStaff
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.StaffFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def perform_create(self, serializer):
        if "user" not in serializer.validated_data:
            serializer.validated_data["user"] = self.request.user
        return super().perform_create(serializer)


class CourseAdviserViewSet(mixins.swagger_documentation_factory("course adviser"), viewsets.ModelViewSet):
    queryset = models.CourseAdviser.objects.all()
    serializer_class = serializers.CourseAdviserSerializer
    serializer_action_classes = {
        'list': serializers.CourseAdviserResponseSerializer,
        'retrieve': serializers.CourseAdviserResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsHead
        or cpermissions.IsDean
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.CourseAdviserFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class StudentViewSet(mixins.swagger_documentation_factory("student with user"), viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    serializer_action_classes = {
        'list': serializers.StudentResponseSerializer,
        'retrieve': serializers.StudentResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsStudent
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.StudentFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def perform_create(self, serializer):
        if "user" not in serializer.validated_data:
            serializer.validated_data["user"] = self.request.user
        return super().perform_create(serializer)


class BiodataViewSet(mixins.swagger_documentation_factory("biodata", "a", "biodata"), viewsets.ModelViewSet):
    queryset = models.Biodata.objects.all()
    serializer_class = serializers.BiodataSerializer
    serializer_action_classes = {
        'list': serializers.BiodataResponseSerializer,
        'retrieve': serializers.BiodataResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsITDept
        or cpermissions.IsStaff
        or cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.BiodataFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
    def perform_create(self, serializer):
        if "user" not in serializer.validated_data:
            serializer.validated_data["user"] = self.request.user
        return super().perform_create(serializer)


class ResultViewSet(mixins.swagger_documentation_factory("result"), viewsets.ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer
    serializer_action_classes = {
        'list': serializers.ResultResponseSerializer,
        'retrieve': serializers.ResultResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsITDept
        or cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.ResultFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class AcademicDataViewSet(mixins.swagger_documentation_factory("academic data", "an", "academic data"), viewsets.ModelViewSet):
    queryset = models.AcademicData.objects.all()
    serializer_class = serializers.AcademicDataSerializer
    serializer_action_classes = {
        'list': serializers.AcademicDataResponseSerializer,
        'retrieve': serializers.AcademicDataResponseSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsStaff
        or cpermissions.IsStudent
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.AcademicDataFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def perform_create(self, serializer):
        if "student" not in serializer.validated_data:
            serializer.validated_data["student"] = self.request.user.student_set.all().first()
        return super().perform_create(serializer)


class AcademicHistoryViewSet(mixins.swagger_documentation_factory("academic history", "an", "academic history"), viewsets.ModelViewSet):
    queryset = models.AcademicHistory.objects.all()
    serializer_class = serializers.AcademicHistorySerializer
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsITDept
        or cpermissions.IsStaff
        or cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.AcademicHistoryFilter
    
    def perform_create(self, serializer):
        if "biodata" not in serializer.validated_data:
            serializer.validated_data["biodata"] = self.request.user.biodata
        return super().perform_create(serializer)


class HealthDataViewSet(mixins.swagger_documentation_factory("health data", "a", "health data"), viewsets.ModelViewSet):
    queryset = models.HealthData.objects.all()
    serializer_class = serializers.HealthDataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsITDept
        or cpermissions.IsStaff
        or cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.HealthDataFilter
    
    def perform_create(self, serializer):
        if "biodata" not in serializer.validated_data:
            serializer.validated_data["biodata"] = self.request.user.biodata
        return super().perform_create(serializer)



class FamilyDataViewSet(mixins.swagger_documentation_factory("family data", "a", "family data"), viewsets.ModelViewSet):
    queryset = models.FamilyData.objects.all()
    serializer_class = serializers.FamilyDataSerializer
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsBursar
        or cpermissions.IsITDept
        or cpermissions.IsStaff
        or cpermissions.IsStudentOrReadOnly
    ]
    filterset_class = filters.FamilyDataFilter
    
    def perform_create(self, serializer):
        if "biodata" not in serializer.validated_data:
            serializer.validated_data["biodata"] = self.request.user.biodata
        return super().perform_create(serializer)


class CourseRegistrationViewSet(mixins.swagger_documentation_factory("course registration"), viewsets.ModelViewSet):
    queryset = models.CourseRegistration.objects.all()
    serializer_class = serializers.CourseRegistrationSerializer
    serializer_action_classes = {
        'list': serializers.CourseRegistrationSerializer,
        'retrieve': serializers.CourseRegistrationSerializer,
    }
    permission_classes = [
        cpermissions.IsSuperUser
        or cpermissions.IsStudent
        or cpermissions.IsITDeptOrReadOnly
    ]
    filterset_class = filters.CourseRegistrationFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        if "student" not in serializer.validated_data:
            serializer.validated_data["student"] = self.request.user.student_set.all().first()
        return super().perform_create(serializer)


# Simple JWT integration with drf-yasg (views)
# Decorated drf-simplejwt views
class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description='login',
        operation_summary='login',
        responses={
            status.HTTP_200_OK: serializers.TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description='generata access token using refresh token',
        operation_summary='generata access token using refresh token',
        responses={
            status.HTTP_200_OK: serializers.TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_description='verify access token is still valid',
        operation_summary='verify access token is still valid',
        responses={
            status.HTTP_200_OK: serializers.TokenVerifyResponseSerializer})
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


# django-passwordreset integration with drf-yasg (views)
# Decorated django-passwordreset views
class DecoratedResetPasswordValidateTokenViewSet(ResetPasswordValidateTokenViewSet):
    @swagger_auto_schema(
        operation_description='validate password reset token',
        operation_summary='validate password reset token',
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    

class DecoratedResetPasswordConfirmViewSet(ResetPasswordConfirmViewSet):
    @swagger_auto_schema(
        operation_description='confirm password reset token',
        operation_summary='confirm password reset token',
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    

class DecoratedResetPasswordRequestTokenViewSet(ResetPasswordRequestTokenViewSet):
    @swagger_auto_schema(
        operation_description='request password reset token',
        operation_summary='request password reset token',
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # send an e-mail to the user
        # TODO: Refactor email logic
        print(reset_password_token.user)
        title = "School Management Portal"
        backend_base_url = instance.request.build_absolute_uri()
        frontend_base_url = "http://127.0.0.1:3000" # Should be gotten from the frontend devs
        rel_path = ""
        if not reset_password_token.user.is_staff:
            rel_path = f"{frontend_base_url}/student/newpassword"
        else:
            rel_path = f"{frontend_base_url}/staff/confirmpassword"
            
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.first_name,
            'email': reset_password_token.user.email,
            
            'reset_password_url': "{}?token={}".format(
                # instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
                rel_path,
                reset_password_token.key)
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        # print("context set")
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            f"Password Reset for {title}",
            # message:
            email_plaintext_message,
            # from:   # "noreply@somehost.local"
            settings.EMAIL_HOST_USER,
            # to:
            [reset_password_token.user.email,],
        )
        print("message created")
        msg.attach_alternative(email_html_message, "text/html")
        print("html attached")
        msg.send()
        print("Forgot Password Mail successfully sent")
    except Exception as e:
        print(f"There was an error sending Forgot Password Mail: {e}")
