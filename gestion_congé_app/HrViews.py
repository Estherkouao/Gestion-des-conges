from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees
)

def responsablerh_home(request):
    pass