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
from django.conf import settings
from django.core.mail import send_mail

from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees, LeaveRequest,Notification
)


def employee_home(request):
    try:
        employee = Employees.objects.get(admin=request.user)
    except Employees.DoesNotExist:
        return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page.")
    employee = get_object_or_404(Employees, admin=request.user)

   
    all_liste_demandes_conge_count = Employees.objects.all().count()

    context={
        
        "all_solde_conge_count":all_liste_demandes_conge_count,
        "employee":employee,
        "employee_id":employee.id,
        

    }
    return render(request, "employee_template/employee_home.html", context)

def liste_demandes_conge(request):
    # Récupérer l'employé connecté
    employee = Employees.objects.get(admin=request.user)
    
    # Récupérer les demandes de congés de l'employé
    leave_requests = LeaveRequest.objects.filter(employee_id=employee)

    # Calculer le nombre total de jours de congés pris par l'employé cette année
    current_year = timezone.now().year
    total_leave_days = LeaveRequest.objects.filter(
        employee_id=employee,
        leave_type='CONGE',
        start_date__year=current_year,
        active=True 
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

    return render(request, 'employee_template/liste_demandes_conge.html', {
        'leave_requests': leave_requests,
        'leave_balance': leave_balance,
        'today': timezone.now().date(),
    })


def soumettre_demande(request, leave_request_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)
    
    if leave_request.status == 'Draft':
        leave_request.status = 'Pending'
      
        leave_request.save()

        messages.success(request, "La demande a été envoyée au manager.")
    else:
        messages.error(request, "La demande ne peut pas être soumise.")

    return redirect('liste_demandes_conge') 


def espace_conge(request):
 # Récupérer l'employé connecté
    employee = Employees.objects.get(admin=request.user)
    
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
                leave_request.status = 'Draft'
                leave_request.save()
                
                    # Envoi d'email
                subject = 'Nouvelle demande de congé'
                message = f"Une nouvelle demande de congé a été soumise par {leave_request.employee_id.admin.first_name} {leave_request.employee_id.admin.last_name} pour la période du {leave_request.start_date} au {leave_request.end_date}."
                recipient_list = []
                
                # Ajouter l'email du manager si disponible
                if employee.manager_id:
                    manager_user = employee.manager_id.admin
                    recipient_list.append(manager_user.email)
                
                if recipient_list:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        recipient_list,
                        fail_silently=False,
                    )
                
                messages.success(request, 'Votre demande de congé a été soumise avec succès.')
                return redirect('liste_demandes_conge')
        else:
            messages.error(request, 'Erreur lors de la soumission de la demande de congé.')
    else:
        form = LeaveRequestForm()

    return render(request, 'employee_template/espace_conge.html', {
        'form': form,
        'leave_balance': leave_balance,
    })





def modifier_demande(request, id):
    leave_request = get_object_or_404(LeaveRequest, id=id)
    # Vérifiez que la demande est rejetée
    if leave_request.status not in ['Rejected by Manager', 'Rejected by Responsablerh', 'Pending', 'Draft'] :
        messages.error(request, 'Vous ne pouvez modifier que les demandes rejetées.')
        return redirect('liste_demandes_conge')

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.status = 'Draft'  # Réinitialise le statut pour une nouvelle approbation
            leave_request.save()
            messages.success(request, 'Votre demande de congé a été modifiée et renvoyée pour approbation.')
            return redirect('liste_demandes_conge')
    else:
        form = LeaveRequestForm(instance=leave_request)
    
    return render(request, 'employee_template/modifier_demande.html', {
        'form': form,
        'leave_request': leave_request,
    })

def supprimer_demande(request, id):
    leave_request = get_object_or_404(LeaveRequest, id=id)

    if leave_request.status in ['Rejected by Manager', 'Rejected by Responsablerh', 'Pending']:
        leave_request.delete()
        messages.success(request, 'Votre demande de congé a été supprimée avec succès.')
    elif leave_request.status == 'Approved by Responsablerh':
        if leave_request.end_date < timezone.now().date():
            # Si la demande est passée et approuvée, elle est supprimée sans affecter le solde
            leave_request.delete()
            messages.success(request, 'Votre demande de congé passée a été supprimée avec succès.')
        else:
            messages.error(request, 'Vous ne pouvez supprimer que les demandes passées qui ont été approuvées.')
    else:
        messages.error(request, 'Vous ne pouvez supprimer que les demandes rejetées ou en attente.')

    return redirect('liste_demandes_conge')


def employee_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Employees.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'employee_template/employee_profile.html', context)


def employee_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('employee_profile')
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

            employee = Employees.objects.get(admin=customuser.id)
            employee.address = address
            employee.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('employee_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('employee_profile')