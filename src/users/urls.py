from django.urls import path
from .views import RegisterView, CustomLoginView, ProfileView, AddressView, AddressEditView
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/login/logout.html'), name='logout'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('address/add', AddressView.as_view(), name='address-add'),
    path('address/<int:pk>/edit/', AddressEditView.as_view(), name='address-edit'),
]
