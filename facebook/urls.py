from django.urls import path
from . import views

app_name = 'facebook'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('post/create', views.PostCreateView.as_view(), name='create-post')
]
