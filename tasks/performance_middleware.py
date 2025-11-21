"""
Middleware para optimizaciones de rendimiento:
- Headers de caché para recursos estáticos
- Compresión de respuestas
- Prevención de back/forward cache issues
"""
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re


class PerformanceOptimizationMiddleware(MiddlewareMixin):
    """
    Middleware para optimizar el rendimiento agregando headers apropiados
    """
    
    # Extensiones de archivos estáticos que deben tener caché largo
    STATIC_EXTENSIONS = ['.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', 
                        '.webp', '.woff', '.woff2', '.ttf', '.eot', '.ico', '.pdf']
    
    # Tiempo de caché en segundos (1 año para recursos estáticos)
    CACHE_MAX_AGE = 31536000  # 1 año
    
    def process_response(self, request, response):
        """
        Agrega headers de optimización a la respuesta
        """
        path = request.path
        
        # Headers para prevenir problemas de back/forward cache
        if not response.get('Cache-Control'):
            # Para páginas HTML dinámicas, usar no-cache
            if path.endswith('.html') or not any(path.endswith(ext) for ext in self.STATIC_EXTENSIONS):
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
            else:
                # Para recursos estáticos, usar caché largo
                response['Cache-Control'] = f'public, max-age={self.CACHE_MAX_AGE}, immutable'
        
        # Headers de compresión (si el servidor no los maneja)
        if 'Content-Encoding' not in response:
            content_type = response.get('Content-Type', '')
            if any(ct in content_type for ct in ['text/', 'application/javascript', 'application/json']):
                # El servidor web (nginx/apache) debería manejar la compresión
                # pero agregamos el header para indicar que aceptamos compresión
                if 'Accept-Encoding' in request.META:
                    response['Vary'] = 'Accept-Encoding'
        
        # Headers de seguridad y rendimiento adicionales
        if 'X-Content-Type-Options' not in response:
            response['X-Content-Type-Options'] = 'nosniff'
        
        if 'X-Frame-Options' not in response:
            response['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Prevenir problemas de back/forward cache solo para páginas HTML dinámicas
        # Pero permitir que el navegador use bfcache cuando sea apropiado
        if path.endswith('.html') or ('/' in path and not any(path.endswith(ext) for ext in self.STATIC_EXTENSIONS)):
            # Para páginas HTML, usar headers que permitan bfcache pero prevengan caché HTTP
            response['Cache-Control'] = 'no-cache, must-revalidate, max-age=0'
            # No usar 'no-store' ni 'private' para permitir bfcache
            response['Pragma'] = 'no-cache'
            # Agregar headers para mejorar bfcache
            if 'Vary' not in response:
                response['Vary'] = 'Accept-Encoding'
        
        # Agregar headers para mejorar el rendimiento
        if 'X-DNS-Prefetch-Control' not in response:
            response['X-DNS-Prefetch-Control'] = 'on'
        
        return response

