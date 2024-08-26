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

    
    
    """ all_employee_count = Employees.objects.all().count()
    all_conge_atente_count = LeaveRequest.objects.all().count()
    all_leave_balance_count = Employees.objects.all().count() """
   


    context={
        "manager_id": manager.id,
        'manager': manager,

    }
    return render(request, "manager_template/manager_home.html", context)

    

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

from django.core.mail import send_mail
from django.conf import settings

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
            leave_request.save()
            messages.success(request, f"La demande de congé de {leave_request.employee_id.admin.username} a été approuvée par le manager et envoyée au Responsablerh.")
            send_notification_to_responsablerh(leave_request)
        elif action == 'reject':
            leave_request.status = 'Rejected by Manager'
            leave_request.save()
            messages.success(request, f"La demande de congé de {leave_request.employee_id.admin.username} a été rejetée.")
            notify_employee_of_rejection(leave_request)

        # Sauvegarde du commentaire du manager
        form = LeaveRequestCommentForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()
        notify_employee_of_comment(leave_request)    

        leave_request.save()

      
    
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
      # Envoi d'email
                subject = 'Nouvelle demande de congé aprouvée par le manager'
                message = f"Une nouvelle demande de congé a été soumise par {leave_request.employee_id.admin.first_name} {leave_request.employee_id.admin.last_name} pour la période du {leave_request.start_date} au {leave_request.end_date}."
                recipient_list = []

                # Ajouter l'email du responsable RH global si disponible
                responsablerh = Responsablerhs.objects.first()  
                if responsablerh:
                    responsablerh_user = responsablerh.admin
                    recipient_list.append(responsablerh_user.email)

                if recipient_list:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        recipient_list,
                        fail_silently=False,
                    )    


def notify_employee_of_rejection(leave_request):
    employee = leave_request.employee_id
    subject = 'Votre demande de congé a été rejetée'
    message = f"Bonjour {employee.admin.first_name},\n\n" \
              f"Votre demande de congé du {leave_request.start_date} au {leave_request.end_date} a été rejetée par le manager.\n\n" \
              f"Veuillez modifier votre requette et le renvoyer.\n\n" \
              f"Cordialement,\n"
    recipient_list = [employee.admin.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
    
def notify_employee_of_comment(leave_request):
    employee = leave_request.employee_id
    subject = 'Votre demande de congé a été commenter'
    message = f"Bonjour {employee.admin.first_name},\n\n" \
              f"Votre demande de congé du {leave_request.start_date} au {leave_request.end_date} a été commenter.\n\n" \
              f"Cordialement,\n"
    recipient_list = [employee.admin.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


def ajout_commentaire(request, leave_request_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)
    manager_id = request.user.id
    
    if request.method == 'POST':
        form = LeaveRequestCommentForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_request.manager_comment = form.cleaned_data['manager_comment']
            leave_request.save()
            return redirect('manager_home')
        
    else:
        form = LeaveRequestCommentForm(instance=leave_request)

    return render(request, 'manager_template/ajout_commentaire.html', {
        'form': form,
        'leave_request': leave_request,
        'manager_id': manager_id
    })


def supprimer_commentaire(request, leave_request_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)

    leave_request.manager_comment = ""
    leave_request.save()
    return redirect('manager_home')


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
        

         

         



