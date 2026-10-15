import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, View

from ..forms import PostForm
from ..models import Comment, Post, PostLike


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("facebook:index")
    template_name = "facebook/create_post.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "active"
        if form.is_valid():
            messages.success(
                self.request,
                f"Publicación '{form.instance.title}' se creo correctamente.",
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = "create-post"
        return context


class PostDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):

        post = get_object_or_404(Post, pk=pk, user=request.user)
        messages.warning(
            self.request, f"Publicación '{post.title}' se elimino.", extra_tags="danger"
        )
        post.delete()

        return redirect(request.META.get("HTTP_REFERER", "/"))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "facebook/create_post.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Publicación '{self.object.title}' se actualizo correctamente.",
        )
        return super().form_valid(form)

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


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        description = request.POST.get("comment", "").strip()

        if not description:
            msg_error = "Escribe un comentario antes de enviarlo."
            return JsonResponse(
                {
                    "status": "error",
                    "error": msg_error,
                    "error_html": render_to_string(
                        "components/social/messages/message.html",
                        {"toast_style": "text-bg-danger", "message": msg_error},
                    ),
                },
                status=400,
            )

        with transaction.atomic():
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                description=description,
                image=request.FILES.get("image"),
                status="active",
            )

        return JsonResponse(
            {
                "status": "ok",
                "comment_html": render_to_string(
                    "facebook/components/post/comment_post.html",
                    {"comment": comment},
                    request=request,
                ),
                "success_html": render_to_string(
                    "components/social/messages/message.html",
                    {
                        "toast_style": "text-bg-success",
                        "message": "Commentario subido correctamente.",
                    },
                ),
                "comments_count": post.comments.count(),
            },
            status=201,
        )
