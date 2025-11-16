from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserService:
    @staticmethod
    def create_user(username, password):
        """Create a new user"""
        if User.objects.filter(username=username).exists():
            raise ValueError("A user with that username already exists.")
        
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user and return tokens"""
        user = authenticate(username=username, password=password)
        if not user:
            raise ValueError("Invalid username or password")
        
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username
        }
    
    @staticmethod
    def promote_to_admin(user):
        """Promote user to admin role"""
        user.role = "ADMIN"
        user.save()
        return user