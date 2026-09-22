from django.urls import path
from . import views

app_name = 'facebook'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('post/create', views.PostCreateView.as_view(), name='create-post'),
    path('user/detail/<int:pk>', views.UserDetailView.as_view(), name="detail-user"),
    path('follow/<int:user_id>', views.FollowView.as_view(), name='follow-user')
]
