from django.urls import path
from .views import RegisterView, LoginView , PromoteToAdminView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path("promote-to-admin/", PromoteToAdminView.as_view(), name="promote-to-admin"),
]