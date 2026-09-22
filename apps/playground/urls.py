from django.urls import path
from . import views 

app_name = 'playground'

urlpatterns = [
    path('', views.PersonListView.as_view(), name="person-list"),
    path('detail/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),
    path('create', views.PersonCreateView.as_view(), name='person-create')
]
