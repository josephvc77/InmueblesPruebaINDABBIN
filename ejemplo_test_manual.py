"""
Ejemplo de cómo probar manualmente algunas vulnerabilidades
Esto te muestra qué buscan los tests automáticos
"""

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def ejemplo_test_manual():
    """Ejemplos de pruebas manuales que puedes hacer"""
    
    client = Client()
    
    print("=" * 60)
    print("EJEMPLOS DE PRUEBAS MANUALES DE SEGURIDAD")
    print("=" * 60)
    print()
    
    # 1. Test de Login con credenciales inválidas
    print("1️⃣  Probando login con credenciales inválidas...")
    response = client.post('/signin/', {
        'username': 'usuario_inexistente',
        'password': 'contraseña_incorrecta'
    })
    if response.status_code == 200 and not response.wsgi_request.user.is_authenticated:
        print("   ✅ PASS: Login rechazado correctamente")
    else:
        print("   ❌ FAIL: Login debería haber sido rechazado")
    print()
    
    # 2. Test de SQL Injection en login
    print("2️⃣  Probando protección contra SQL Injection...")
    sql_injection = "admin'--"
    response = client.post('/signin/', {
        'username': sql_injection,
        'password': 'cualquier_cosa'
    })
    if response.status_code != 500:
        print("   ✅ PASS: Sistema protegido contra SQL Injection")
    else:
        print("   ❌ FAIL: Vulnerable a SQL Injection")
    print()
    
    # 3. Test de acceso sin autenticación
    print("3️⃣  Probando acceso a página protegida sin login...")
    response = client.get('/principal/')
    if response.status_code == 302:  # Redirect to login
        print("   ✅ PASS: Redirige al login correctamente")
    else:
        print("   ❌ FAIL: Permite acceso sin autenticación")
    print()
    
    # 4. Test de CSRF
    print("4️⃣  Probando protección CSRF...")
    # Crear usuario para login
    user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')
    client.login(username='testuser', password='testpass123')
    
    # Intentar POST sin CSRF token
    response = client.post('/inmuebles/crear/', {
        'NombreInmueble': 'Test'
    }, follow=False)
    
    if response.status_code == 403:
        print("   ✅ PASS: Protección CSRF activa")
    else:
        print("   ⚠️  WARNING: CSRF podría no estar funcionando correctamente")
    print()
    
    print("=" * 60)
    print("💡 Estos son ejemplos básicos.")
    print("   Los tests automáticos son mucho más completos!")
    print("=" * 60)

if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
    django.setup()
    ejemplo_test_manual()

