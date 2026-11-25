"""URL configuration for projeto project."""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    path('contato/', include("contato.urls")),
    path('login/', include("login.urls")),
]

# Serve arquivos de mídia (funciona também com DEBUG=False, ex.: no Render).
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
