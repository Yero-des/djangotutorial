from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        protected_paths = [reverse('profiles:login')]
        
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.path in protected_paths:
            return redirect('facebook:index')
            
        return response
    