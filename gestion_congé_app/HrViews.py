from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from gestion_congé_app.models import (
    CustomUser, HRs, Directors, Managers, Department, Employees
)

def hr_home(request):
    pass