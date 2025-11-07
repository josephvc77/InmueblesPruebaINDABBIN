#!/bin/bash

# Script para ejecutar tests de seguridad
# Uso: ./run_security_tests.sh

echo "=========================================="
echo "Ejecutando Tests de Seguridad"
echo "=========================================="
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Ejecutar tests de seguridad
echo "Ejecutando tests de seguridad..."
python manage.py test tasks.test_security --verbosity=2

echo ""
echo "=========================================="
echo "Tests de Seguridad Completados"
echo "=========================================="

