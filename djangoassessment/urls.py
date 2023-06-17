from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loan_app.urls')),
    path('token-auth/', views.obtain_auth_token)
]
