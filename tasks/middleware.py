# middleware.py
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Tiempo límite de inactividad
        max_idle_time = getattr(settings, 'AUTO_LOGOUT_TIME', 3000)

        last_activity_str = request.session.get('last_activity')

        if last_activity_str:
            last_activity = datetime.fromisoformat(last_activity_str)
            elapsed_time = (timezone.now() - last_activity).total_seconds()

            if elapsed_time > max_idle_time:
                # Cerrar la sesión y enviar mensaje de "Sesión expirada"
                logout(request)
                messages.warning(request, "Sesión expirada. Por favor, inicia sesión nuevamente.")
                return self.get_response(request)

        request.session['last_activity'] = timezone.now().isoformat()
        return self.get_response(request)
