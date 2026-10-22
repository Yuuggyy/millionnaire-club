from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import path, include, re_path
from django.views.generic import TemplateView


def serve_asset(request, file_path=""):
    """Sert les fichiers du build Vite (frontend/assets)."""
    base = (Path(settings.BASE_DIR) / "frontend" / "assets").resolve()
    cible = (base / file_path).resolve()
    if not str(cible).startswith(str(base)) or not cible.is_file():
        raise Http404
    ct = "text/css" if cible.suffix == ".css" else (
         "text/javascript" if cible.suffix == ".js" else "application/octet-stream")
    return FileResponse(open(cible, "rb"), content_type=ct)


def serve_root_file(request, name):
    """favicon etc. à la racine du build."""
    base = Path(settings.BASE_DIR) / "frontend"
    cible = (base / name).resolve()
    if not str(cible).startswith(str(base)) or not cible.is_file():
        raise Http404
    return FileResponse(open(cible, "rb"))


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("menuapp.urls")),
    re_path(r"^assets/(?P<file_path>.*)$", serve_asset),
    re_path(r"^(?P<name>favicon\.svg|favicon\.ico|CNAME|page-flip\.browser\.min\.js)$", serve_root_file),
    path("", TemplateView.as_view(template_name="index.html"), name="menu"),
]
