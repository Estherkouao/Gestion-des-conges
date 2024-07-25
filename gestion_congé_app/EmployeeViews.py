from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseNotFound
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LeaveRequestForm
from django.utils import timezone
from django.db.models import Sum,DurationField,F,Case, When
from datetime import timedelta

from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees, LeaveRequest,Notification
)


def employee_home(request):
    try:
        employee = Employees.objects.get(admin=request.user)
    except Employees.DoesNotExist:
        return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page.")
    employee = get_object_or_404(Employees, admin=request.user)

    all_espace_conge_count = LeaveRequest.objects.all().count()
    all_solde_conge_count = LeaveRequest.objects.all().count()

    context={
        "all_espace_conge_count":all_espace_conge_count,
        "all_solde_conge_count":all_solde_conge_count,
        "employee":employee,
        "employee_id":employee.id,
        

    }
    return render(request, "employee_template/employee_home.html", context)


def espace_conge(request):
    # Récupérer l'employé connecté
    employee = Employees.objects.get(admin=request.user)
    
    # Récupérer les demandes de congés de l'employé
    leave_requests = LeaveRequest.objects.filter(employee_id=employee)

    # Calculer le nombre total de jours de congés pris par l'employé cette année
    current_year = timezone.now().year
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

    leave_limit = 30  # Limite de 30 jours pour 'CONGE'
    leave_balance = leave_limit - total_leave_days

    if request.method == 'POST':
        if 'leave_request_id' in request.POST:
            leave_request = get_object_or_404(LeaveRequest, id=request.POST['leave_request_id'], employee_id=employee)
            form = LeaveRequestForm(request.POST, instance=leave_request)
        else:
            form = LeaveRequestForm(request.POST)
        
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_days_requested = (leave_request.end_date - leave_request.start_date).days + 1
            if leave_request.leave_type == 'CONGE' and (total_leave_days + leave_days_requested) > leave_limit:
                messages.error(request, 'Vous avez atteint votre limite de 30 jours de congé pour cette année.')
            else:
                leave_request.employee_id = employee
                leave_request.save()
                
                # Envoyer une notification au manager
                if employee.manager_id:
                    manager_user = employee.manager_id.admin
                    notification = Notification(
                        recipient=manager_user,
                        message=f"Nouvelle demande de congé de {employee.admin.username}"
                    )
                    notification.save()

                 # Envoyer une notification au responsable RH global
                responsablerh = Responsablerhs.objects.first()  
                if responsablerh:
                    responsablerh_user = responsablerh.admin
                    notification = Notification(
                        recipient=responsablerh_user,
                        message=f"Nouvelle demande de congé de {employee.admin.username}"
                    )
                    notification.save()
                
                messages.success(request, 'Votre demande de congé a été soumise avec succès.')
                return redirect('espace_conge')
        else:
            messages.error(request, 'Erreur lors de la soumission de la demande de congé.')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'employee_template/espace_conge.html', {
        'leave_requests': leave_requests,
        'form': form,
        'leave_balance': leave_balance,
    })





def modifier_demande(request, id):
    leave_request = get_object_or_404(LeaveRequest, id=id)
    # Vérifiez que la demande est rejetée
    if leave_request.status not in ['Rejected by Manager', 'Rejected by Responsablerh', 'Pending'] :
        messages.error(request, 'Vous ne pouvez modifier que les demandes rejetées.')
        return redirect('espace_conge')

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.status = 'Pending'  # Réinitialise le statut pour une nouvelle approbation
            leave_request.save()
            messages.success(request, 'Votre demande de congé a été modifiée et renvoyée pour approbation.')
            return redirect('espace_conge')
    else:
        form = LeaveRequestForm(instance=leave_request)
    
    return render(request, 'employee_template/modifier_demande.html', {
        'form': form,
        'leave_request': leave_request,
    })

def supprimer_demande(request, id):
    leave_request = get_object_or_404(LeaveRequest, id=id)
    if leave_request.status not in ['Rejected by Manager', 'Rejected by Responsablerh', 'Pending']:
        messages.error(request, 'Vous ne pouvez supprimer que les demandes rejetées.')
    else:
        leave_request.delete()
        messages.success(request, 'Votre demande de congé a été supprimée avec succès.')
    return redirect('espace_conge')

def rapport_presence():
    pass

def solde_conge():
    pass

def employee_profile():
    pass