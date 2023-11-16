from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegisterForm, LoginForm, ProfileUpdateForm, UserUpdateForm, AddressForm, AddressEditForm
from .models import Address
from shop.mixins import ExtraContextMixin


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/login/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    success_message = "You have been successfully signed up!"


class CustomLoginView(LoginView):
    template_name = 'users/login/login.html'
    form_class = LoginForm


class ProfileView(ExtraContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_form = UserUpdateForm(instance=self.request.user)
        profile_form = ProfileUpdateForm(instance=self.request.user.profile)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile's been updated!")
            return redirect('profile')

        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class AddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/address/address.html'
    success_url = '/cart/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressEditView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressEditForm
    template_name = 'users/address/address_edit.html'
    success_url = '/cart/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
