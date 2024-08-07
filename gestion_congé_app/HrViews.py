from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .forms import LeaveRequestCommentrhForm
from datetime import date
from django.db.models import Sum, Case, When, DurationField, F
from django.utils import timezone
from datetime import timedelta

from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees,LeaveRequest
)

def responsablerh_home(request):
    
    try:
        responsablerh = Responsablerhs.objects.get(admin=request.user)
    except Responsablerhs.DoesNotExist:
        return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page.")
    responsablerh = get_object_or_404(Responsablerhs, admin=request.user) 

    all_employee_count = Employees.objects.all().count()
    all_conge_atente_count = LeaveRequest.objects.all().count()
    all_leave_balance_count = Employees.objects.all().count()

    context={

        "all_employee_count": all_employee_count,
        "all_conge_atente_count": all_conge_atente_count,
        "responsablerh_id": responsablerh.id,
        "all_leave_balance_count" :all_leave_balance_count,

    }
    return render(request, "rh_template/responsablerh_home.html", context)


def liste_employee_rh(request):
    employees = Employees.objects.all()
    today = date.today()

    employees_on_leave = []
    employees_not_on_leave = []

    for employee in employees:
        leave_requests = LeaveRequest.objects.filter(
            employee_id=employee, 
            status__in=['Approved by Manager', 'Approved by Responsablerh'],
            start_date__lte=today, 
            end_date__gte=today
        )
        on_leave = leave_requests.exists()

        if on_leave:
            employees_on_leave.append(employee)
        else:
            employees_not_on_leave.append(employee)

    context = {
        "employees_on_leave": employees_on_leave,
        "employees_not_on_leave": employees_not_on_leave
    }
    return render(request, 'rh_template/liste_employee_rh.html', context)



def conge_atente_rh(request):
    # Récupérer toutes les demandes de congé en attente d'approbation par le Responsablerh
    leave_requests = LeaveRequest.objects.filter(status='Approved by Manager')

    if request.method == 'POST':
        leave_request_id = request.POST.get('leave_request_id')
        action = request.POST.get('action')
        leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)

        # Gestion des actions d'approbation et de rejet par le Responsablerh
        if action == 'approve':
            leave_request.status = 'Approved by Responsablerh'
            messages.success(request, f"La demande de congé de {leave_request.employee_id.admin.username} a été approuvée par le Responsablerh.")
            # Notifier l'employé que la demande est approuvée
            notify_employee_of_approval(leave_request)
        elif action == 'reject':
            leave_request.status = 'Rejected by Responsablerh'
            messages.success(request, f"La demande de congé de {leave_request.employee_id.admin.username} a été rejetée par le Responsablerh.")
            # Notifier l'employé du rejet
            notify_employee_of_rejection(leave_request)

        leave_request.save()
        return redirect('conge_atente_rh')
    
    context = {
        'leave_requests': leave_requests,
    }
    return render(request, 'rh_template/conge_atente_rh.html', context)

def notify_employee_of_approval(leave_request):
    pass

def notify_employee_of_rejection(leave_request):
    pass



def leave_balance_rh(request):
    employees = Employees.objects.all()  # Récupérer tous les employés

    current_year = timezone.now().year
    leave_limit = 30  # Limite de 30 jours pour 'CONGE'

    # Calculer le solde de congé pour chaque employé
    employee_balances = []
    for employee in employees:
        total_leave_days = LeaveRequest.objects.filter(
            employee_id=employee,
            leave_type='CONGE',
            start_date__year=current_year
        ).aggregate(
            total_days=Sum(
                Case(
                    When(end_date__isnull=False, then=F('end_date') - F('start_date') + timedelta(days=1)),
                    default=timedelta(days=0),
                    output_field=DurationField()
                )
            )
        )['total_days']

        # Convertir en jours
        if total_leave_days is not None:
            total_leave_days = total_leave_days.days
        else:
            total_leave_days = 0

        leave_balance = leave_limit - total_leave_days
        employee_balances.append({
            'employee': employee,
            'leave_balance': leave_balance
        })

    context = {
        'employee_balances': employee_balances,
    }
    return render(request, 'rh_template/leave_balance_rh.html', context)




def responsablerh_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    responsablerh = Responsablerhs.objects.get(admin=user)

    context={
        "user": user,
        "responsablerh": responsablerh,
    }
    return render(request, 'rh_template/responsablerh_profile.html', context)


def responsablerh_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('responsablerh_profile')
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

            responsablerh = Responsablerhs.objects.get(admin=customuser.id)
            responsablerh.address = address
            responsablerh.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('responsablerh_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('responsablerh_profile')


