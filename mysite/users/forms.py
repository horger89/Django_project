from django import forms
# built in django User model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

# define metaclass
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class CreateProfileForm(ModelForm):
    class Meta:

      model = Profile
      fields = ['image', 'location']






