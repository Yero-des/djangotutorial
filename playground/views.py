from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
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
