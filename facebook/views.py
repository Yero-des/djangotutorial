from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class IndexListView(ListView):
    model = Post
    template_name = 'facebook/index.html'
    context_object_name = 'posts'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']
    success_url = reverse_lazy('facebook:index')
    template_name = 'facebook/create_post.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'active'
        return super().form_valid(form)
    
class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'facebook/detail_user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_posts"] = self.object.posts.all()
        context["is_user_detail"] = True
        return context
    