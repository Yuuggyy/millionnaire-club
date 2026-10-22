"""CORS minimal : autorise le front (surge.sh, domaines maison, etc.)
à appeler l'API. Pas de dépendance externe."""
from django.utils.deprecation import MiddlewareMixin


class CorsApiMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        origin = request.headers.get("Origin")
        if origin:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return response
