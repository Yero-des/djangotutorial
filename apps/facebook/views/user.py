from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, View

from ..forms import UserForm
from ..models import Follow, Post

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "facebook/users.html"
    context_object_name = "users"

    def get_queryset(self):
        return super().get_queryset().for_stats(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = "users"
        return context


class UserDetailView(DetailView):
    model = User
    context_object_name = "user"
    template_name = "facebook/detail_user.html"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        return super().get_queryset().for_stats(self.request.user)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["user_posts"] = self.object.posts.for_content(self.request.user)
        context["is_user_detail"] = True
        context["current_view"] = "users"

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "facebook/profile.html"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username).annotate(
            total_posts=Count("facebook_posts", distinct=True)
        )

    def get_success_url(self):
        return reverse("facebook:profile", kwargs={"username": self.object.username})

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Usuario '{self.object.username}' se actualizo correctamente.",
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts_user"] = self.object.posts.for_content(self.request.user)

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
                following_user=request.user, followed_user=user_to_follow
            )
            messages.success(self.request, f'Se comenzo a seguir a "{user_to_follow}"')

        return redirect(request.META.get("HTTP_REFERER", "/"))


class DarkModeView(LoginRequiredMixin, View):

    def post(self, request):

        try:

            config = request.user.config
            config.dark_mode = not config.dark_mode
            config.save()
            config.save(
                "NO ME LA CUENTES PUÑETAS DE MIERDA", "ESTO ES LA POYA CON CEBOLLA"
            )

            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "messages": str(e),
                },
                status=400,
            )
