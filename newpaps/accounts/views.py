from django.shortcuts import render
from news.forms import SignUpForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User

class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'
