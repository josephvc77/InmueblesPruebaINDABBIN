from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            current_time = timezone.now()
            if (current_time - request.user.last_login).seconds > settings.AUTO_LOGOUT_DELAY:
                # Cerrar la sesión
                logout(request)
                if request.resolver_match:
                    # Determinar a cuál sistema redirigir
                    if 'condia' in request.resolver_match.url_name:
                        login_url = reverse('signinCondia')
                    else:
                        login_url = reverse('signin')
                    return HttpResponseRedirect(login_url)
        
        return response
