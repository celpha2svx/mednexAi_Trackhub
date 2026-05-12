from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Auto-login after registration
        login(self.request, self.object)
        messages.success(self.request, f"Welcome, {self.object.username}! You're now part of the community.")
        return response
