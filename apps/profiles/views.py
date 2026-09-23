from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.views import LoginView
from django.contrib import messages

class AuthenticatedLoginTemplate(LoginView):
    template_name = 'profiles/login.html'
    
    def form_invalid(self, form):
        messages.error(self.request,'Usuario o contraseña incorrectos.', extra_tags='danger')
        return super().form_invalid(form)