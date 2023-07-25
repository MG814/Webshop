from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegisterForm, LoginForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    success_message = "You have been successfully signed up!"


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
