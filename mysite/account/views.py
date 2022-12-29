from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
# Create your views here.
from .import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login") #reverses back to the login page after user signs up
    template_name = "account/signup.html"
