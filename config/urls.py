from django.contrib import admin
from django.urls import path, include
from django.views import generic
from django.conf import settings

urlpatterns = [
    path('', generic.RedirectView.as_view(pattern_name='facebook:index')),
    path('polls/', include('apps.polls.urls')),
    path('playground/', include('apps.playground.urls')),
    path('facebook/', include('apps.facebook.urls')),
    path('facebook/authentication/', include('apps.profiles.urls')),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Django debug toolbar
if not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
