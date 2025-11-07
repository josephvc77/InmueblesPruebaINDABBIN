#!/usr/bin/env python
"""
Script simple para ejecutar tests de seguridad y mostrar resultados
Uso: python test_security_simple.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
django.setup()

from django.test.utils import get_runner
from django.conf import settings

def main():
    """Ejecuta los tests de seguridad y muestra un resumen"""
    print("=" * 60)
    print("🔒 EJECUTANDO TESTS DE SEGURIDAD")
    print("=" * 60)
    print()
    
    # Obtener el test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)
    
    # Ejecutar tests
    failures = test_runner.run_tests(['tasks.test_security'])
    
    print()
    print("=" * 60)
    if failures:
        print("❌ ALGUNOS TESTS FALLARON")
        print(f"   {failures} test(s) fallaron")
        print()
        print("⚠️  REVISA LOS ERRORES ARRIBA Y CORRÍGELOS")
    else:
        print("✅ TODOS LOS TESTS PASARON")
        print("   Tu sistema está protegido contra vulnerabilidades comunes")
    print("=" * 60)
    
    return failures

if __name__ == '__main__':
    sys.exit(main())

