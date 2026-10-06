from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView

from ..models import Post


class IndexListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "facebook/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.for_content(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_view"] = "index"

        return context
