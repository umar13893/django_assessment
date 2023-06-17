from django.urls import path
from .views import RegisterUserAPIView, CreateLoanAPIView, UserDetailAPI
urlpatterns = [
    path('get-user-details/', UserDetailAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('create-loan/', CreateLoanAPIView.as_view()),
]
