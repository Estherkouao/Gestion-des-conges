from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from systeme_de_gestion_des_conges_des_employes import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_congé_app.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
