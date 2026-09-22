from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Person
from datetime import datetime

# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        kwargs['nuevo'] = "else"
        return super().get_context_data(**kwargs)
    
class PersonListView(ListView):
    model = Person
    template_name = "playground/person_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['now'] = datetime.now()
        
        return context

class PersonDetailView(DetailView):
    model = Person
    template_name = "playground/person_detail.html"
    context_object_name = 'person'
    
class PersonCreateView(CreateView):
    model = Person
    template_name = "playground/person_create.html"
    fields = ['name', 'last_name', 'shirt_sizes', 'partner', 'country']
    success_url = reverse_lazy('playground:person-list')