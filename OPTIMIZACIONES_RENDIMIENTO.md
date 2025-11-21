# Optimizaciones de Rendimiento - Lighthouse

Este documento describe las optimizaciones implementadas y recomendaciones adicionales para mejorar el rendimiento según los reportes de Lighthouse.

## ✅ Optimizaciones Implementadas

### 1. Eliminación de Recursos que Bloquean el Renderizado
- **CSS crítico**: Cargado normalmente (Bootstrap, estilos principales)
- **CSS no crítico**: Cargado con `preload` y `onload` para carga diferida
- **Scripts**: Agregado `defer` a todos los scripts no críticos
- **Preconnect**: Agregado para CDNs externos (mejora DNS lookup)

### 2. Imágenes Optimizadas
- Agregado `width` y `height` a todas las imágenes para prevenir layout shift
- Agregado `loading="lazy"` para carga diferida
- Agregado `decoding="async"` para mejor rendimiento
- Uso de formato WebP cuando sea posible

### 3. Middleware de Optimización
- Creado `tasks/performance_middleware.py` para:
  - Headers de caché apropiados para recursos estáticos
  - Prevención de problemas de back/forward cache
  - Headers de seguridad adicionales

## 📋 Recomendaciones Adicionales para el Servidor

### 1. Compresión de Texto (Est savings: 19 KiB)
**Para Nginx:**
```nginx
# En /etc/nginx/nginx.conf o tu configuración del sitio
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript 
           application/json application/javascript application/xml+rss 
           application/rss+xml font/truetype font/opentype 
           application/vnd.ms-fontobject image/svg+xml;
gzip_disable "msie6";
```

**Para Apache:**
```apache
# En .htaccess o configuración del servidor
LoadModule deflate_module modules/mod_deflate.so

<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css
    AddOutputFilterByType DEFLATE application/xml application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml application/javascript
    AddOutputFilterByType DEFLATE application/json
</IfModule>
```

### 2. Caché de Recursos Estáticos (5 resources found)
**Para Nginx:**
```nginx
# En la configuración del sitio
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

**Para Apache:**
```apache
# En .htaccess
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType font/woff "access plus 1 year"
    ExpiresByType font/woff2 "access plus 1 year"
</IfModule>
```

### 3. Reducir Tiempo de Respuesta del Servidor (6,510 ms)
**Optimizaciones de Django:**
- Usar `DEBUG = False` en producción
- Configurar `ALLOWED_HOSTS` correctamente
- Usar un servidor WSGI optimizado (Gunicorn con múltiples workers)
- Implementar caché de base de datos (Redis/Memcached)
- Optimizar consultas de base de datos (usar `select_related` y `prefetch_related`)

**Ejemplo con Gunicorn:**
```bash
gunicorn djangocrud.wsgi:application \
    --workers 4 \
    --worker-class gevent \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

### 4. Minificar CSS y JavaScript
**Opción 1: Usar django-compressor**
```bash
pip install django-compressor
```

Agregar a `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'compressor',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
```

**Opción 2: Minificar manualmente con herramientas**
- CSS: https://cssminifier.com/
- JavaScript: https://javascript-minifier.com/

### 5. Reducir CSS y JavaScript No Utilizados
- Usar herramientas como PurgeCSS para eliminar CSS no usado
- Revisar qué librerías de JavaScript realmente se necesitan
- Considerar usar versiones más ligeras de librerías (ej: usar solo los módulos necesarios de jQuery)

**Ejemplo con PurgeCSS:**
```bash
npm install -g purgecss
purgecss --css static/inicio/css/styles.css --content "tasks/templates/**/*.html" --output static/inicio/css/
```

### 6. Optimizar Tamaño de Imágenes (Est savings: 41 KiB)
- Usar herramientas como ImageOptim, TinyPNG, o Squoosh
- Convertir imágenes a formato WebP cuando sea posible
- Usar tamaños apropiados (no cargar imágenes de 2000px cuando solo se muestran a 200px)
- Implementar responsive images con `srcset`

### 7. Prevenir Problemas de Back/Forward Cache
Ya implementado en el middleware, pero también se puede agregar:
```html
<!-- En el <head> -->
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
```

## 🔧 Configuración del Middleware

Agregar el middleware a `settings.py`:

```python
MIDDLEWARE = [
    # ... otros middlewares ...
    'tasks.performance_middleware.PerformanceOptimizationMiddleware',
]
```

## 📊 Métricas Esperadas Después de las Optimizaciones

- **First Contentful Paint (FCP)**: < 1.8s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Time to Interactive (TTI)**: < 3.8s
- **Total Blocking Time (TBT)**: < 200ms
- **Cumulative Layout Shift (CLS)**: < 0.1

## 🚀 Pasos Siguientes

1. ✅ Implementar compresión en el servidor web
2. ✅ Configurar caché de recursos estáticos
3. ✅ Minificar CSS y JavaScript
4. ✅ Optimizar imágenes
5. ✅ Revisar y eliminar código no utilizado
6. ✅ Configurar CDN si es posible
7. ✅ Monitorear rendimiento con herramientas como Google PageSpeed Insights

## 📝 Notas

- Algunas optimizaciones requieren acceso al servidor web (nginx/apache)
- Las optimizaciones de base de datos pueden requerir análisis de consultas
- El uso de CDN puede mejorar significativamente el rendimiento para usuarios lejanos

