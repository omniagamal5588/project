from rest_framework import serializers
from account.models import User,Pharmacy
from . import utils
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError



class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  #password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=[ 'frist_name','last_name','email', 'password', 'phone_number', 'address']
    extra_kwargs={
      'password':{'write_only':True}
    }

# Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    #password2 = attrs.get('password2')
   

    email = attrs.get('email', None)
    if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email')})
    return super().validate(attrs)
  def create(self, validate_data):
    return User.objects.create_user(**validate_data)
  

#PharmacyRegisterSerializer
class PharmacyRegistrationSerializer(serializers.ModelSerializer):
 
  class Meta:
    model =Pharmacy
    fields=[ 'name','email', 'phone_number', 'location', 'password','description','pharmacy_image']
    extra_kwargs={
      'password':{'write_only':True}
    }

# Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    #password2 = attrs.get('password2')
    

    email = attrs.get('email', None)
    if Pharmacy.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email')})
    return super().validate(attrs)
  def create(self, validate_data):
    return Pharmacy.objects.create_pharmacy_account(**validate_data)


#login Serializer
class UserLoginSerializer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'frist_name','last_name','phone_number','address','password']    


#login pharmacy serializer
class PharmacyLoginSeraializer(serializers.ModelSerializer):
  class Meta:
    model=Pharmacy
    fields=['email','password']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs



class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      # Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')
    
class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')    