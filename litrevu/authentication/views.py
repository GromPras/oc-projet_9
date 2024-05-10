from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignInForm, SignUpForm


class SignInView(LoginView):
    form_class = SignInForm
    template_name = "authentication/signin.html"
    next_page = reverse_lazy("reviews:feed")


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("signin")
    template_name = "authentication/signup.html"
