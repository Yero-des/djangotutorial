from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, View, UpdateView
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
    
    # TODO: Dar estilos a formulario para crear publicaciones
    
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

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'photo']
    template_name = 'facebook/profile.html'
    
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
    
    def get_success_url(self):
        return reverse('facebook:profile', kwargs={
            'username': self.object.username
        })
    
    def form_valid(self, form):
        messages.success(self.request, f"Usuario '{self.object.username}' se actualizo correctamente.")
        return super().form_valid(form)
    
    # TODO: Dar estilos a formulario para actualizar datos de perfil
    
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
    