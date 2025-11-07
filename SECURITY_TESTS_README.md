# Tests de Seguridad del Sistema

Este documento describe los tests de seguridad implementados para proteger el sistema contra vulnerabilidades comunes.

## 📋 Contenido

El archivo `tasks/test_security.py` contiene una suite completa de tests de seguridad que cubre:

### 1. **Autenticación** (`AuthenticationSecurityTests`)
- ✅ Login con credenciales válidas
- ✅ Login con credenciales inválidas
- ✅ Prevención de SQL Injection en login
- ✅ Prevención de XSS en campos de login
- ✅ Logout limpia sesión correctamente
- ✅ Expiración de sesión

### 2. **Protección CSRF** (`CSRFSecurityTests`)
- ✅ Verificación de que CSRF middleware está habilitado
- ✅ POST sin token CSRF debe fallar
- ✅ Formularios incluyen token CSRF

### 3. **Autorización** (`AuthorizationSecurityTests`)
- ✅ Acceso no autenticado redirige al login
- ✅ Decoradores de permisos funcionan correctamente
- ✅ Usuarios no pueden acceder a datos de otros
- ✅ Superusuarios tienen acceso completo

### 4. **Validación de Entrada** (`InputValidationSecurityTests`)
- ✅ Prevención de SQL Injection en búsquedas
- ✅ Prevención de XSS en campos de texto
- ✅ Validación de tipos de archivo
- ✅ Validación de longitud máxima de campos

### 5. **Seguridad de Sesiones** (`SessionSecurityTests`)
- ✅ Cookies de sesión seguras
- ✅ Cookies HttpOnly
- ✅ Prevención de fijación de sesión

### 6. **Configuración de Seguridad** (`ConfigurationSecurityTests`)
- ✅ DEBUG debe ser False en producción
- ✅ SECRET_KEY no debe ser inseguro
- ✅ ALLOWED_HOSTS configurado
- ✅ Middlewares de seguridad habilitados

### 7. **Seguridad de APIs AJAX** (`APISecurityTests`)
- ✅ Endpoints AJAX requieren autenticación
- ✅ Validación de entrada en endpoints AJAX
- ✅ Rate limiting (si está implementado)

### 8. **Seguridad de Contraseñas** (`PasswordSecurityTests`)
- ✅ Contraseñas están hasheadas
- ✅ Verificación de contraseñas funciona
- ✅ Validación de longitud mínima

### 9. **Acceso a Datos** (`DataAccessSecurityTests`)
- ✅ Usuarios no pueden modificar datos de otros
- ✅ Usuarios no pueden eliminar datos de otros

### 10. **Prevención SQL Injection** (`SQLInjectionSecurityTests`)
- ✅ ORM previene inyección SQL

### 11. **Prevención XSS** (`XSSSecurityTests`)
- ✅ Templates auto-escapan contenido

## 🚀 Cómo Ejecutar los Tests

### Opción 1: Usando el script proporcionado

```bash
chmod +x run_security_tests.sh
./run_security_tests.sh
```

### Opción 2: Usando Django directamente

```bash
# Activar entorno virtual (si aplica)
source venv/bin/activate

# Ejecutar todos los tests de seguridad
python manage.py test tasks.test_security

# Ejecutar con más detalles
python manage.py test tasks.test_security --verbosity=2

# Ejecutar una clase específica de tests
python manage.py test tasks.test_security.AuthenticationSecurityTests

# Ejecutar un test específico
python manage.py test tasks.test_security.AuthenticationSecurityTests.test_login_with_valid_credentials
```

### Opción 3: Usando pytest (si está instalado)

```bash
pytest tasks/test_security.py -v
```

## 📊 Interpretación de Resultados

### ✅ Tests Exitosos
Si todos los tests pasan, verás:
```
Ran X tests in Y.YYYs

OK
```

### ❌ Tests Fallidos
Si algún test falla, verás:
```
FAIL: test_name (tasks.test_security.ClassName)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
AssertionError: ...

----------------------------------------------------------------------
Ran X tests in Y.YYYs

FAILED (failures=1)
```

## 🔧 Configuración Recomendada para Producción

Antes de desplegar a producción, asegúrate de:

1. **DEBUG = False** en `settings.py`
2. **SECRET_KEY** seguro y no expuesto
3. **ALLOWED_HOSTS** configurado correctamente
4. **SESSION_COOKIE_SECURE = True** (para HTTPS)
5. **CSRF_COOKIE_SECURE = True** (para HTTPS)
6. **SECURE_SSL_REDIRECT = True** (forzar HTTPS)
7. **SECURE_HSTS_SECONDS = 31536000** (HSTS)
8. **SECURE_HSTS_INCLUDE_SUBDOMAINS = True**
9. **SECURE_HSTS_PRELOAD = True**

Ejemplo de configuración en `settings.py`:

```python
# Solo en producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

## 🛡️ Buenas Prácticas de Seguridad

1. **Nunca** expongas `SECRET_KEY` en el código
2. **Siempre** usa variables de entorno para secretos
3. **Valida** toda la entrada del usuario
4. **Escapa** todo el output del usuario
5. **Usa** HTTPS en producción
6. **Mantén** Django y dependencias actualizadas
7. **Revisa** logs regularmente
8. **Implementa** rate limiting en APIs públicas
9. **Usa** contraseñas fuertes
10. **Habilita** autenticación de dos factores cuando sea posible

## 📝 Notas

- Algunos tests pueden fallar en desarrollo si `DEBUG=True`
- Los tests de rate limiting requieren implementación adicional
- Los tests de validación de archivos dependen de la configuración del modelo
- Algunos tests requieren permisos específicos configurados

## 🔍 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'tasks.test_security'"
- Asegúrate de estar en el directorio raíz del proyecto
- Verifica que el archivo `tasks/test_security.py` existe

### Error: "django.core.exceptions.ImproperlyConfigured"
- Verifica que la base de datos de test esté configurada
- Ejecuta `python manage.py migrate` primero

### Tests fallan por permisos
- Algunos tests requieren que los usuarios tengan permisos específicos
- Verifica la configuración de permisos en el admin

## 📚 Recursos Adicionales

- [Django Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

