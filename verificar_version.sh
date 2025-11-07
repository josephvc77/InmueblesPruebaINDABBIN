#!/bin/bash

# Script para verificar la versión en diferentes lugares

echo "=========================================="
echo "🔍 VERIFICACIÓN DE VERSIÓN"
echo "=========================================="
echo ""

# 1. Versión en .env
echo "1️⃣  Versión en .env:"
if [ -f .env ]; then
    VERSION_ENV=$(grep "^APP_VERSION=" .env | cut -d '=' -f2 | tr -d ' ')
    echo "   ✅ .env: $VERSION_ENV"
else
    echo "   ❌ .env no encontrado"
fi

# 2. Versión en .env.bak (solo para referencia, NO debe usarse)
echo ""
echo "2️⃣  Versión en .env.bak (solo referencia, NO se usa):"
if [ -f .env.bak ]; then
    VERSION_BAK=$(grep "^APP_VERSION=" .env.bak | cut -d '=' -f2 | tr -d ' ' 2>/dev/null || echo "N/A")
    echo "   ⚠️  .env.bak: $VERSION_BAK (este archivo NO debe ser leído)"
else
    echo "   ℹ️  .env.bak no existe"
fi

# 3. Versión en settings.py (valor por defecto)
echo ""
echo "3️⃣  Versión por defecto en settings.py:"
VERSION_SETTINGS=$(grep "APP_VERSION = os.environ.get" djangocrud/settings.py | grep -o "'[^']*'" | tail -1 | tr -d "'")
echo "   ✅ settings.py (default): $VERSION_SETTINGS"

# 4. Versión que Django lee realmente
echo ""
echo "4️⃣  Versión que Django lee (desde .env):"
python3 << 'PYTHON_SCRIPT'
import os
import sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
import django
django.setup()
from django.conf import settings
print(f"   ✅ Django lee: {settings.APP_VERSION}")
PYTHON_SCRIPT

echo ""
echo "=========================================="
echo "✅ Verificación completada"
echo "=========================================="
echo ""
echo "💡 Si las versiones no coinciden:"
echo "   1. Reinicia el servidor Django"
echo "   2. Verifica que .env tenga la versión correcta"
echo "   3. El .env.bak NO debe ser leído (es solo backup)"

