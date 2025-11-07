"""
Configuración de Seguridad para Producción
Copia estas configuraciones a tu settings.py cuando despliegues a producción
"""

# ============================================
# CONFIGURACIÓN DE SEGURIDAD - PRODUCCIÓN
# ============================================

# IMPORTANTE: Estas configuraciones solo deben usarse en producción
# No las uses en desarrollo ya que pueden causar problemas

# 1. DEBUG debe ser False en producción
DEBUG = False

# 2. SECRET_KEY debe ser seguro y único
# NUNCA uses el mismo SECRET_KEY en producción que en desarrollo
# Genera uno nuevo con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# SECRET_KEY = 'tu-secret-key-generado-aqui'

# 3. ALLOWED_HOSTS debe incluir solo tus dominios
ALLOWED_HOSTS = [
    'tu-dominio.com',
    'www.tu-dominio.com',
    # No incluyas 'localhost' o '127.0.0.1' en producción
]

# 4. Cookies de Sesión Seguras (requiere HTTPS)
SESSION_COOKIE_SECURE = True  # Solo envía cookies por HTTPS
SESSION_COOKIE_HTTPONLY = True  # Previene acceso JavaScript a cookies
SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF adicional

# 5. Cookies CSRF Seguras (requiere HTTPS)
CSRF_COOKIE_SECURE = True  # Solo envía cookies por HTTPS
CSRF_COOKIE_HTTPONLY = True  # Previene acceso JavaScript
CSRF_USE_SESSIONS = False  # Usa cookies (más seguro que sesiones)

# 6. Redirección Forzada a HTTPS
SECURE_SSL_REDIRECT = True  # Redirige HTTP a HTTPS automáticamente

# 7. HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Incluye subdominios
SECURE_HSTS_PRELOAD = True  # Permite preload en navegadores

# 8. Protección XSS
SECURE_BROWSER_XSS_FILTER = True  # Filtro XSS del navegador
SECURE_CONTENT_TYPE_NOSNIFF = True  # Previene MIME sniffing

# 9. Clickjacking Protection
X_FRAME_OPTIONS = 'DENY'  # Previene embedding en iframes
# Alternativa: 'SAMEORIGIN' si necesitas iframes del mismo origen

# 10. Referrer Policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# 11. Timeout de Sesión
SESSION_COOKIE_AGE = 3600  # 1 hora (ajusta según necesidades)
SESSION_SAVE_EVERY_REQUEST = True  # Renueva sesión en cada request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expira al cerrar navegador

# 12. Logging de Seguridad
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# 13. Base de Datos - Usa conexiones seguras
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'ssl': {'ca': '/path/to/ca-cert.pem'},
#         },
#     }
# }

# 14. Archivos Estáticos y Media
# Asegúrate de servir archivos estáticos desde un servidor web (Nginx, Apache)
# No uses Django para servir archivos estáticos en producción

# 15. Email Backend Seguro
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST = 'smtp.tu-servidor.com'
# EMAIL_PORT = 587

# ============================================
# CONFIGURACIÓN CONDICIONAL RECOMENDADA
# ============================================

# En tu settings.py, puedes usar esto:
"""
import os

# Detectar si estamos en producción
PRODUCTION = os.environ.get('ENVIRONMENT') == 'production'

if PRODUCTION:
    # Aplicar todas las configuraciones de seguridad arriba
    DEBUG = False
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # ... etc
else:
    # Configuración de desarrollo
    DEBUG = True
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
"""

# ============================================
# CHECKLIST DE SEGURIDAD PRE-DESPLIEGUE
# ============================================

"""
Antes de desplegar a producción, verifica:

[ ] DEBUG = False
[ ] SECRET_KEY único y seguro
[ ] ALLOWED_HOSTS configurado correctamente
[ ] HTTPS configurado y funcionando
[ ] SESSION_COOKIE_SECURE = True
[ ] CSRF_COOKIE_SECURE = True
[ ] SECURE_SSL_REDIRECT = True
[ ] HSTS configurado
[ ] Base de datos con credenciales seguras
[ ] Archivos estáticos servidos por servidor web
[ ] Logs configurados
[ ] Backups configurados
[ ] Firewall configurado
[ ] Actualizaciones de seguridad aplicadas
[ ] Tests de seguridad ejecutados y pasando
[ ] Variables de entorno para secretos
[ ] Rate limiting implementado (si aplica)
[ ] Monitoreo de seguridad configurado
"""

