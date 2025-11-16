from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer , PromoteToAdminSerializer
from .services import UserService
from utlis.response import ResponseHandler

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.data:
            return ResponseHandler.error(error="Username and password are required")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = UserService.create_user(
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password']
                )
                return ResponseHandler.success(
                    data={"username": user.username, "id": user.id},
                    message="User created successfully"
                )
            except ValueError as e:
                return ResponseHandler.error(error=str(e))
        return ResponseHandler.error(error=ResponseHandler.get_error_message(serializer.errors))


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.data:
            return ResponseHandler.error(error="Username and password are required")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                tokens = UserService.authenticate_user(
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password']
                )
                return ResponseHandler.success(data=tokens, message="Login successful")
            except ValueError as e:
                return ResponseHandler.error(error=str(e))
    
        return ResponseHandler.error(error=ResponseHandler.get_error_message(serializer.errors))
    
    
class PromoteToAdminView(generics.GenericAPIView):
    serializer_class = PromoteToAdminSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = UserService.promote_to_admin(request.user)
            return ResponseHandler.success(
                data={"role": user.role},
                message=f"{user.username} has been promoted to ADMIN"
            )
        except Exception as e:
            return ResponseHandler.error(error="Failed to promote user")
