#!/bin/bash

# Archivo .env
ENV_FILE=".env"
SETTINGS_FILE="djangocrud/settings.py"

# Verifica que exista el .env
if [ ! -f $ENV_FILE ]; then
  echo "$ENV_FILE no encontrado!"
  exit 1
fi

# Leer la versión actual del .env
CURRENT_VERSION=$(grep "^APP_VERSION=" $ENV_FILE | cut -d '=' -f2 | tr -d ' ')

if [ -z "$CURRENT_VERSION" ]; then
  echo "APP_VERSION no definida en $ENV_FILE"
  exit 1
fi

echo "Versión actual: $CURRENT_VERSION"

# Separar en partes: major.minor.patch
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Incrementar el patch
PATCH=$((PATCH + 1))

# Nueva versión
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Reemplazar en .env
# Nota: sed -i.bak crea un backup, pero lo eliminaremos después
sed -i.bak "s/^APP_VERSION=.*/APP_VERSION=$NEW_VERSION/" $ENV_FILE

# Eliminar el backup .env.bak para evitar confusión
# El .env.bak puede causar problemas si se lee accidentalmente
if [ -f "${ENV_FILE}.bak" ]; then
    rm -f "${ENV_FILE}.bak"
    echo "Backup .env.bak eliminado (para evitar confusión)"
fi

# También actualizar el valor por defecto en settings.py como respaldo
if [ -f "$SETTINGS_FILE" ]; then
  # Actualizar el valor por defecto en settings.py
  sed -i.bak "s/APP_VERSION = os.environ.get('APP_VERSION', '[^']*')/APP_VERSION = os.environ.get('APP_VERSION', '$NEW_VERSION')/" $SETTINGS_FILE
  echo "settings.py actualizado con versión por defecto: $NEW_VERSION"
fi

echo "Nueva versión: $NEW_VERSION"
echo "Archivos actualizados:"
echo "  - $ENV_FILE"
echo "  - $SETTINGS_FILE (valor por defecto)"

echo ""
echo "=========================================="
echo "🐳 Construyendo imagen Docker..."
echo "=========================================="

# Verificar que Docker esté disponible
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado o no está en el PATH"
    exit 1
fi

# Verificar que Docker esté corriendo
if ! docker info &> /dev/null; then
    echo "❌ Docker no está corriendo"
    echo "   Inicia Docker Desktop o el servicio de Docker"
    exit 1
fi

# Verificar que buildx esté disponible
if ! docker buildx version &> /dev/null; then
    echo "⚠️  Docker buildx no está disponible, usando docker build estándar"
    BUILD_CMD="docker build"
else
    BUILD_CMD="docker buildx build --platform=linux/x86_64 --load"
fi

echo "Construyendo imagen: iodocker-dgtic.sep.gob.mx/siisep/siisep-django:$NEW_VERSION"
echo "Esto puede tardar varios minutos..."

# Construir Docker con la nueva versión
if [ "$BUILD_CMD" == "docker buildx build --platform=linux/x86_64 --load" ]; then
    docker buildx build --platform=linux/x86_64 --load --no-cache -t iodocker-dgtic.sep.gob.mx/siisep/siisep-django:$NEW_VERSION .
else
    docker build --no-cache -t iodocker-dgtic.sep.gob.mx/siisep/siisep-django:$NEW_VERSION .
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker construido exitosamente con versión $NEW_VERSION"
    echo "   Imagen: iodocker-dgtic.sep.gob.mx/siisep/siisep-django:$NEW_VERSION"
    echo ""
    echo "Para ejecutar el contenedor:"
    echo "   docker run -p 8000:8000 iodocker-dgtic.sep.gob.mx/siisep/siisep-django:$NEW_VERSION"
else
    echo ""
    echo "❌ Error al construir Docker"
    echo "   Verifica los logs arriba para más detalles"
    exit 1
fi
