from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Post
from ..forms import PostForm
from ..forms import PostForm

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
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