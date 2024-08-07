from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LeaveRequestCommentForm
from datetime import date
from django.db.models import Sum, Case, When, DurationField, F
from django.utils import timezone
from datetime import timedelta


from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees, LeaveRequest,AttendanceReport
)


def manager_home(request):
      # Vérifiez si l'utilisateur connecté est un manager
    try:
        manager = Managers.objects.get(admin=request.user)
    except Managers.DoesNotExist:
        return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page.")
    manager = get_object_or_404(Managers, admin=request.user)

    
    
    all_employee_count = Employees.objects.all().count()
    all_conge_atente_count = LeaveRequest.objects.all().count()
    all_leave_balance_count = Employees.objects.all().count()
   

    # all_leave_count = AttendanceReport.objects.filter(employee_id=employee.id, leave_status=1).count()

   
    # employees_attendance = Employees.objects.filter('employee_id')
    # employee_list = []
    # employee_list_attendance_present = []
    # employee_list_attendance_absent = []
    # for employee in employees_attendance:
    #     attendance_present_count = AttendanceReport.objects.filter(status=True, employee_id=employee.id).count()
    #     attendance_absent_count = AttendanceReport.objects.filter(status=False, employee_id=employee.id).count()
    #     employee_list.append(employee.admin.first_name+" "+ employee.admin.last_name)
    #     employee_list_attendance_present.append(attendance_present_count)
    #     employee_list_attendance_absent.append(attendance_absent_count)

    context={
        "all_employee_count": all_employee_count,
        "all_conge_atente_count": all_conge_atente_count,
        "manager_id": manager.id,
        "all_leave_balance_count":all_leave_balance_count,
        'manager': manager,

    }
    return render(request, "manager_template/manager_home.html", context)

# def all_leave_balance_count(request):
#     total_leave_balance = Employees.objects.aggregate(total_leave_balance=Sum('leave_balance'))['total_leave_balance']
#     context = {
#         'total_leave_balance': total_leave_balance
#     }
#     return render(request, 'manager_template/manager_home.html', context)
    

from datetime import date
import logging
logger = logging.getLogger(__name__)

def liste_employee(request, manager_id):
    logger.debug(f"Requête pour le manager avec ID: {manager_id}")
    manager = get_object_or_404(Managers, id=manager_id)
    logger.debug(f"Manager trouvé: {manager}")
    
    employees = Employees.objects.filter(manager_id=manager.id)
    logger.debug(f"Nombre d'employés trouvés: {employees.count()}")
    
    today = date.today()
    employees_status = []

    for employee in employees:
        logger.debug(f"Traitement de l'employé: {employee.admin.first_name} {employee.admin.last_name} (ID: {employee.id})")
        leave_requests = LeaveRequest.objects.filter(
            employee_id=employee.id, 
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
        'manager': manager,
        'manager_id': manager_id,
        'employees_status': employees_status,
    }
    logger.debug(f"Contexte passé au template: {context}")
    return render(request, 'manager_template/liste_employee.html', context)



def conge_attente(request, manager_id):
    manager = get_object_or_404(Managers, id=manager_id)
    leave_requests = LeaveRequest.objects.filter(employee_id__manager_id=manager, status='Pending')

    if request.method == 'POST':
        leave_request_id = request.POST.get('leave_request_id')
        action = request.POST.get('action')
        leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)

        # Gestion des actions d'approbation et de rejet
        if action == 'approve':
            leave_request.status = 'Approved by Manager'
            messages.success(request, f"La demande de congé de {leave_request.employee_id.admin.username} a été approuvée par le manager et envoyée au Responsablerh.")
            send_notification_to_responsablerh(leave_request)
        elif action == 'reject':
            leave_request.status = 'Rejected by Manager'
            messages.success(request, f"La demande de congé de {leave_request.employee_id.admin.username} a été rejetée.")
            notify_employee_of_rejection(leave_request)

        # Sauvegarde du commentaire du manager
        form = LeaveRequestCommentForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()

        leave_request.save()
        return redirect('conge_attente', manager_id=manager_id)
    
    else:
        form = LeaveRequestCommentForm()

    context = {
        'manager_id': manager_id,
        'leave_requests': leave_requests,
        'form': form,
    }
    return render(request, 'manager_template/conge_attente.html', context)

def leave_balance(request, manager_id):
    manager = get_object_or_404(Managers, id=manager_id)
    employees = Employees.objects.filter(manager_id=manager)

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
        'manager_id': manager_id,
        'employee_balances': employee_balances,
    }
    return render(request, 'manager_template/leave_balance.html', context)


def send_notification_to_responsablerh(leave_request):
    pass

def notify_employee_of_rejection(leave_request):
    pass


def manager_profile(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    manager = get_object_or_404(Managers, admin=user)
    manager_id = manager.id

    context={
        "user": user,
        "manager": manager,
        "manager_id": manager_id,
    }
    return render(request, 'manager_template/manager_profile.html', context)


def manager_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manager_profile')
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

            manager = Managers.objects.get(admin=customuser.id)
            manager.address = address
            manager.save()

            messages.success(request, "Profil mis a jour avec succes")
            return redirect('manager_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('manager_profile')


