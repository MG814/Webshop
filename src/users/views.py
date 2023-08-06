from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, LoginForm, ProfileUpdateForm, UserUpdateForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    success_message = "You have been successfully signed up!"


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class ProfileView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile's been updated!")
            return redirect('profile')

        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
