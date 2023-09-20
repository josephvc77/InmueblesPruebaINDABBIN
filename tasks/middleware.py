from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            current_time = timezone.now()
            if (current_time - request.user.last_login).seconds > settings.AUTO_LOGOUT_DELAY:
                logout(request)
        
        return response