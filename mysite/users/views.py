from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm, CreateProfileForm
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from .models import Profile
from django.views import View
from food.owner import OwnerUpdateView
from django.views.generic import UpdateView, CreateView

# Create your views here.
def register(request):
    if request.method == "POST":
        Form = RegisterForm(request.POST)
        if Form.is_valid():
          Form.save()
          username = Form.cleaned_data.get('username')
          messages.success(request,f'Welcome {username} your account has been created now you can log in')
          return redirect('login')
    else:
        Form = RegisterForm()

    return render(request, 'users/register.html',{'form':Form} )


@login_required
def profilepage(request):
    return render(request, 'users/profile.html')


class UpdateProfile(UpdateView):
    model = Profile
    fields = ['image','location']
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')
    

class CreateProfile(CreateView):
    model = Profile
    
    template_name = 'users/create_profile.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('profile')

    def form_valid(self,form):
        
        # find logged in user
        form.instance.user = self.request.user

        return super().form_valid(form)
    
    