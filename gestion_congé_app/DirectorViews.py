from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import date

from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees
)

def director_home(request):
    all_employee_actif_count = Employees.objects.all().count()
    all_employee_nonActif_count = Employees.objects.all().count()

    context={
        "all_employee_actif_count": all_employee_actif_count,
        "all_employee_nonActif_count": all_employee_nonActif_count,
    }
    return render(request, "director_template/director_home.html", context)

def director_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    director = Directors.objects.get(admin=user)

    context={
        "user": user,
        "director": director,
    }
    return render(request, 'director_template/director_profile.html', context)


def director_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('director_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            director = Directors.objects.get(admin=customuser.id)
            director.address = address
            director.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('director_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('director_profile')
        

        
def liste_employee_actif(request):
    today = date.today()
    liste_employee_actif = Employees.objects.filter(
        leaverequest__status__in=['Approved by Manager', 'Approved by Responsablerh', 'Approved by Director'],
        leaverequest__start_date__lte=today,
        leaverequest__end_date__gte=today
    ).distinct()
    liste_employee_actif = Employees.objects.exclude(id__in=liste_employee_actif.values_list('id', flat=True))

    context = {
        "liste_employee_actif": liste_employee_actif
    }
    return render(request, 'director_template/liste_employee_actif.html', context)




def liste_employee_nonActif(request):
    today = date.today()
    liste_employee_nonActif = Employees.objects.filter(
        leaverequest__status__in=['Approved by Manager', 'Approved by Responsablerh', 'Approved by Director'],
        leaverequest__start_date__lte=today,
        leaverequest__end_date__gte=today
    ).distinct()

    context = {
        "liste_employee_nonActif": liste_employee_nonActif
    }
    return render(request, 'director_template/liste_employee_nonActif.html', context)

