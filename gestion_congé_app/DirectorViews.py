from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect

from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees,LeaveRequest
)

def director_home(request):

    try:
        director = Directors.objects.get(admin=request.user)
    except Directors.DoesNotExist:
        return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page.")

    all_employee_count = Employees.objects.all().count()

    context = {
        "all_employee_count": all_employee_count,
        "director_id": director.id,
    }

    # Debugging
    print(f"all_employee_count: {all_employee_count}")
    print(f"director_id: {director.id}")

    return render(request, "director_template/director_home.html", context)


def director_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    director = Directors.objects.get(admin=user)

    context={
        "user": user,
        "director": director,
        "director_id": director.id,
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
        

import logging
logger = logging.getLogger(__name__)

def liste_des_employee(request):
   employees = Employees.objects.all()
   today = date.today()

    
   employees_status = []

   for employee in employees:
        logger.debug(f"Traitement de l'employé: {employee.admin.first_name} {employee.admin.last_name} (ID: {employee.id})")
        leave_requests = LeaveRequest.objects.filter(
            employee_id=employee, 
            status__in=['Approved by Manager', 'Approved by Responsablerh'],
            start_date__lte=today, 
            end_date__gte=today
        )
        on_leave = leave_requests.exists()
        employees_status.append({
            'employee': employee,
            'on_leave': on_leave
        })
        logger.debug(f"Statut de l'employé {employee.id}: {'En congé' if on_leave else 'Présent'}")

   context = {
         'employees_status': employees_status,
    }
   return render(request, 'director_template/liste_des_employee.html', context)




