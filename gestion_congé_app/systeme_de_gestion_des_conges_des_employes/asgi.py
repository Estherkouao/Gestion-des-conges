"""
ASGI config for systeme_de_gestion_des_conges_des_employes project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'systeme_de_gestion_des_conges_des_employes.settings')

application = get_asgi_application()
