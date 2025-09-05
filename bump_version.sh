#!/bin/bash

# Archivo .env
ENV_FILE=".env"

# Verifica que exista
if [ ! -f $ENV_FILE ]; then
  echo "$ENV_FILE no encontrado!"
  exit 1
fi

# Leer la versión actual
CURRENT_VERSION=$(grep APP_VERSION $ENV_FILE | cut -d '=' -f2)

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
sed -i.bak "s/APP_VERSION=.*/APP_VERSION=$NEW_VERSION/" $ENV_FILE

echo "Nueva versión: $NEW_VERSION"

docker buildx build --platform=linux/x86_64 --load --no-cache -t iodocker-dgtic.sep.gob.mx/siisep/siisep-django:$NEW_VERSION .

echo "Docker construido con versión $NEW_VERSION"
