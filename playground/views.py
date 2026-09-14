from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Person

# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        kwargs['nuevo'] = "else"
        return super().get_context_data(**kwargs)
    
class PersonListView(ListView):
    model = Person
    template_name = "playground/person_list.html"


class PersonDetailView(DetailView):
    model = Person
    template_name = "playground/person_detail.html"
    context_object_name = 'person'
    
class PersonCreateView(CreateView):
    model = Person
    template_name = "playground/person_create.html"
    fields = ['name', 'last_name']
    success_url = reverse_lazy('playground:person-list')