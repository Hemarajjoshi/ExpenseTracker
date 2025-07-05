from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
    

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError("Username already Taken !")
        
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("Email already Taken !")
        
        return data

    def validate_password(self, data):
        try:
            validate_password(data)
        except Exception as e:
            raise serializers.ValidationError(e)
    
        return data
    
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do no match")
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username, password=password
            )

        if not user:
            raise serializers.ValidationError("Invalid Username or password.")
        

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }
    

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get('refresh')
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token
            return {
                'access': str(new_access_token),
                'refresh': str(refresh)
            }
        except Exception as e:
            raise serializers.ValidationError(e)
