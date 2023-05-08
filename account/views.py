from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,PharmacyRegistrationSerializer,UserLoginSerializer, UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
from account.models import User,Pharmacy
#from rest_framework.renderers import JSONRenderer, YAMLRenderer
# Create your views here.

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes=[UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return Response({'msg':'Registration Successfully'}, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response({'request name'}, status=status.HTTP_400_BAD_REQUEST)
  
#PharmacyRegisterView
class PharmacyRegistrationView(APIView):
   renderer_classes=[UserRenderer]
   def post(self, request, format=None):
    serializer = PharmacyRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        pharmacy = serializer.save()
        return Response({'msg':'Registration Of Pharmacy Successfully'}, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response({'request name'}, status=status.HTTP_400_BAD_REQUEST) 

'''
class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
   '''
class UserLoginView(APIView):
  def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token
        }
        return response


#login Pharmacy View
class PharmacyLoginView(APIView):
   def post(self, request):
        email = request.data['email']
        password = request.data['password']

        pharmacy = Pharmacy.objects.filter(email=email).first()

        if pharmacy is None:
            raise AuthenticationFailed('Pharmacy Account not found!')

        if not pharmacy.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': pharmacy.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token
        }
        return response

   


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)         
      

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
  
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)    