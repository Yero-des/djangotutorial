from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Post, Follow
from django.contrib import messages

User = get_user_model()

class IndexListView(ListView):
    model = Post
    template_name = 'facebook/index.html'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = 'index'
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']
    success_url = reverse_lazy('facebook:index')
    template_name = 'facebook/create_post.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'active'
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = 'create-post'
        return context
    
class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'facebook/detail_user.html'
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["user_posts"] = self.object.posts.all()
        context["is_user_detail"] = True
        context["current_view"] = 'users'
        context['is_following'] = Follow.objects.filter(
            followed_user=self.object,
            following_user=self.request.user,
        ).exists()        
        
        return context

class FollowView(LoginRequiredMixin, View):
    
    def post(self, request, user_id):
        
        user_to_follow = get_object_or_404(User, id=user_id)
        
        follow = Follow.objects.filter(
            followed_user=user_to_follow,
            following_user=request.user,
        )
        
        # Si el seguimiento existe se elimina
        if follow.exists():
            follow.delete()
            
            messages.warning(self.request, f'Se dejo de seguir a "{user_to_follow}"')
            
        else:
            Follow.objects.create(
                following_user=request.user,
                followed_user=user_to_follow
            )
        
            messages.success(self.request, f'Se comenzo a seguir a "{user_to_follow}"', extra_tags='primary')
            
        return redirect(request.META.get('HTTP_REFERER', '/'))
    