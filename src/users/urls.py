from django.urls import path
from .views import RegisterView, CustomLoginView, ProfileView
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
