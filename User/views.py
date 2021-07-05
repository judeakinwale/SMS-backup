from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer, HealthDataSerializer, BiodataSerializer, AcademicDataSerializer, FamilyDataSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User, BioData, HealthData, AcademicData, FamilyData



class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer_class = UserRegistrationSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'User registered successfully!'
        }
        
        status_ = status.HTTP_200_OK
        return Response(response, status_)




class StudentLoginView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request):
        student_email = request.data.get('email')
        check = student_email.split('@')[1]
        if check.startswith('student'):
            response = log_user_in(self.serializer_class, request_data=request.data)
            status_ = status.HTTP_200_OK

        else:
            response = {
                'success' : True,
                'status code' : status.HTTP_400_BAD_REQUEST,
                'message': 'User credentials not qualified'
                }

            status_ = status.HTTP_400_BAD_REQUEST            

        return Response(response, status=status_)



class StaffLoginView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request):
        student_email = request.data.get('email')
        check = student_email.split('@')[1]
        if check.startswith('staff'):
            response = log_user_in(self.serializer_class, request_data=request.data)
            status_ = status.HTTP_200_OK

        else:
            response = {
                'success' : True,
                'status code' : status.HTTP_400_BAD_REQUEST,
                'message': 'User credentials not qualified'
                }

            status_ = status.HTTP_400_BAD_REQUEST            

        return Response(response, status=status_)



def log_user_in(serializer_class, request_data):
    serializer = serializer_class(data=request_data)
    serializer.is_valid(raise_exception=True)
    response = {
        'success' : True,
        'status code' : status.HTTP_200_OK,
        'message': 'User logged in  successfully!',
        'token' : serializer.data['token'],
        }
     
    return response



class BioDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):

        try:
            
            user_biodata = BioData.objects.get(user=request.user)
            status_ = status.HTTP_200_OK

            response = {
                'success': True,
                'status_code': status_,
                'message': 'User profile fetched successfully!',
                'data': [{
                    'email': user_biodata.email,
                    'birthday': user_biodata.birthday,
                    'first_name': user_biodata.first_name,
                    'last_name': user_biodata.last_name,
                    'middle_name': user_biodata.middle_name if user_biodata.middle_name else '',
                    'matric_no': user_biodata.matric_no,
                    'marital_status': user_biodata.marital_status,
                    'gender': user_biodata.gender,
                    'religion': user_biodata.religion,
                    'birthday': user_biodata.birthday,
                    'nationality': user_biodata.nationality,
                    'state_of_origin': user_biodata.state_of_origin,
                    'local_govt': user_biodata.local_govt,
                    'permanent_address': user_biodata.birthday,
                    'phone1': user_biodata.phone1,
                    'phone2': user_biodata.phone2,
                    'profile_picture': user_biodata.profile_picture.url if user_biodata.profile_picture else ''
                }]
            }

        except Exception as error:
            status_ = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_,
                'message': 'User does not exists',
                'error': str(error)
                }
        return Response(response, status=status_)



    def patch(self, request):
        permission_classes = (IsAuthenticated, )
        authentication_class = JSONWebTokenAuthentication
        bio_data = BioData.objects.get(user = request.user)
        serializer_class = BiodataSerializer(bio_data, data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'User biodata updated successfully!'
        }
        
        status_ = status.HTTP_200_OK
        return Response(response, status_)



class HealthDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):

        try:
            
            user_healthdata = HealthData.objects.get(user=request.user)
            status_ = status.HTTP_200_OK

            response = {
                'success': True,
                'status_code': status_,
                'message': 'User Health data fetched successfully!',
                'data': [{
                    'blood_group': user_healthdata.blood_group,
                    'genotype': user_healthdata.genotype,
                    'allergies': user_healthdata.allergies,
                    'diabetes': user_healthdata.diabetes,
                    'STI': user_healthdata.STIs,
                    'heart_disease': user_healthdata.heart_disease,
                    'disabilities': user_healthdata.disabilities,
                    'respiratory_problems': user_healthdata.respiratory_problems
                }]
            }

        except Exception as error:
            status_ = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_,
                'message': 'User does not exists',
                'error': str(error)
                }

        return Response(response, status=status_)



    def patch(self, request):
        permission_classes = (IsAuthenticated, )
        authentication_class = JSONWebTokenAuthentication
        health_data = HealthData.objects.get(user=request.user)
        request.data['user'] = request.user.id
        serializer_class = HealthDataSerializer(health_data, data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'User health data updated successfully!'
        }
        
        status_ = status.HTTP_200_OK
        return Response(response, status_)