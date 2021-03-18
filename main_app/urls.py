from .views import index, register, VerificationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name="register"),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]





