import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, View

from ..forms import PostForm
from ..models import Post, PostLike


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("facebook:index")
    template_name = "facebook/create_post.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "active"
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = "create-post"
        return context


class PostDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):

        post = get_object_or_404(Post, pk=pk, user=request.user)
        post.delete()

        return redirect("facebook:profile", username=request.user.username)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "facebook/create_post.html"

    def get_success_url(self):
        return reverse(
            "facebook:profile", kwargs={"username": self.request.user.username}
        )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = "edit-post"
        return context


class LikePostView(LoginRequiredMixin, View):

    def post(self, request, post_id, *args, **kwargs):

        post = get_object_or_404(Post, id=post_id)
        like = PostLike.objects.filter(liked_post=post, user_like=request.user)
        liked = True

        if like.exists():
            like.delete()
            liked = not liked
        else:
            PostLike.objects.create(
                liked_post=post, user_like=request.user, reaction="like"
            )

        return JsonResponse(
            {
                "status": "ok",
                "post": post.id,
                "user": request.user.username,
                "liked": liked,
            }
        )
