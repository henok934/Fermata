from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from django.http import JsonResponse
from .models import CustomUser, Buschange
class UserAccountSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        buschanges_count = Buschange.objects.count()
        request.buschanges_count = buschanges_count
        if hasattr(request, '_request'):
            request._request.buschanges_count = buschanges_count
        
        is_html = 'text/html' in request.META.get('HTTP_ACCEPT', '')
        
        exempt_urls = [reverse('login'), reverse('logout')]
        if request.path in exempt_urls or request.path.startswith('/static/'):
            return self.get_response(request)
        user_id = request.session.get('user_id')
        if not user_id:
            request.session.flush()
            if is_html:
                return render(request, 'users/login.html', {
                    'error': 'Unauthorized! Please login to manage your account.',
                    'buschanges_count': buschanges_count
                })
            return JsonResponse({'error': 'Unauthorized! Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            current_user = CustomUser.objects.get(id=user_id)
            request.current_user = current_user
            if hasattr(request, '_request'):
                request._request.current_user = current_user
            if not current_user.is_approved:
                profile_update_url = reverse('update_profile')
                
                if request.path != profile_update_url and not request.path.startswith('/api/'):
                    if is_html:
                        return render(request, 'users/profile_update.html', {
                            'user': current_user,
                            'buschanges_count': buschanges_count,
                            'error': 'Access Restricted: Your account is pending approval. Please complete your registration data.'
                        })
                    return JsonResponse({'error': 'Forbidden. Account pending approval.'}, status=status.HTTP_403_FORBIDDEN)

        except CustomUser.DoesNotExist:
            request.session.flush()
            return redirect('login')

        response = self.get_response(request)
        return response
