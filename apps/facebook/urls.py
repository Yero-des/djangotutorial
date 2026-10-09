from django.urls import path

from . import views

app_name = "facebook"
urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("post/create", views.PostCreateView.as_view(), name="create-post"),
    path("post/<int:pk>/edit", views.PostUpdateView.as_view(), name="edit-post"),
    path("post/<int:pk>/delete", views.PostDeleteView.as_view(), name="delete-post"),
    path("post/<int:post_id>/liked", views.LikePostView.as_view(), name="like-post"),
    path(
        "user/detail/<str:username>", views.UserDetailView.as_view(), name="detail-user"
    ),
    path("user/dark-mode/toggle", views.DarkModeView.as_view(), name="dark-mode"),
    path("user/list", views.UserListView.as_view(), name="list-users"),
    path("follow/<int:user_id>", views.FollowView.as_view(), name="follow-user"),
    path("profile/<str:username>/edit", views.UserUpdateView.as_view(), name="profile"),
]
