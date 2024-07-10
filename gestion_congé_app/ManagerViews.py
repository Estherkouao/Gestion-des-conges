from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees, LeaveRequest,AttendanceReport
)

def manager_profile():
  pass

def manager_home(request):
#  subjects = Subjects.objects.filter(staff_id=request.user.id)

    
    
    all_employee_count = Employees.objects.all().count()
    all_conge_atente_count = LeaveRequest.objects.all().count()
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
        #  "all_leave_count": all_leave_count,
        # "attendance_list": employee_list,
        # "student_list": employee_list,
        # "attendance_present_list": employee_list_attendance_present,
        # "attendance_absent_list": employee_list_attendance_absent
    }
    return render(request, "manager_template/manager_home.html", context)


def liste_employee(request):
   managers = Managers.objects.all()
   context = {
        "managers": managers
    }
   return render(request, "manager_template/liste_employee.html", context)

def conge_attente(request):
    managers = Managers.objects.all()
    leave_requests = LeaveRequest.objects.all()

    context = {
        'managers': managers,
        'leave_requests': leave_requests
    }
    return render(request, 'manager_template/conge_attente.html', context)





