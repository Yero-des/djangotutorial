from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

class IndexListView(ListView):
    model = Post
    template_name = 'facebook/index.html'
    context_object_name = 'posts'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']
    success_url = reverse_lazy('facebook:index')
    template_name = 'facebook/create_post.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user:
            return HttpResponseForbidden("El usuario no esta logueado")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'active'
        return super().form_valid(form)