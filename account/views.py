from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import SignupSerializer, LoginSerializer, RefreshTokenSerializer


class SignupViewSet(viewsets.GenericViewSet):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                'message': 'User Created Successfully', 
                'user':{
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({
                'message': 'Login Successfull',
                'user': serializer.validated_data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenViewSet(viewsets.GenericViewSet):
    """
    ViewSet for refreshing JWT tokens
    """
    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]  # No authentication needed, just valid refresh token
    
    def create(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            'message': 'Token refreshed successfully',
            **serializer.validated_data
        }, status=status.HTTP_200_OK)


        
    
 
    


