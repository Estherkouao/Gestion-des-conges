from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from gestion_congé_app.models import (
    CustomUser, Responsablerhs, Directors, Managers, Department, Employees
)

from .forms import AddEmployeeForm, EditEmployeeForm


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def manager_profile(request):
    pass


def adminhod_home(request):
    all_employee_count = Employees.objects.all().count()
    all_manager_count = Managers.objects.all().count()
    all_responsablerh_count = Responsablerhs.objects.all().count()
    all_director_count = Directors.objects.all().count()

    context={
        "all_employee_count" : all_employee_count,
        "all_manager_count" : all_manager_count,
        "all_responsablerh_count" : all_responsablerh_count,
        "all_director_count" : all_director_count,
        
    }

    return render(request, "hod_template/home_content.html", context)


def add_manager(request):
    return render(request, "hod_template/manager/add_manager.html")

def add_manager_save(request):
    if request.method != "POST":
        messages.error(request, "Méthode Invalide !")
        return redirect('add_manager')
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
      

        try:
            user = CustomUser.objects.create_user( email=email,username=username, password=password, first_name=first_name, last_name=last_name, user_type="2")
            user.managers.address = address
            user.save()
            messages.success(request, "Manager ajouté avec succes !")
            return redirect('add_manager')
        except:
            messages.error(request, "Erreur ajout manager!")
            return redirect('add_manager')


def manage_manager(request):
    managers = Managers.objects.all()
    context = {
        "managers": managers
    }
    return render(request, 'hod_template/manager/manage_manager.html', context)


def edit_manager(request, manager_id):
    manager = Managers.objects.get(admin=manager_id)
    context = {
        "manager": manager,
        "id": manager_id
    }
    return render(request, 'hod_template/manager/edit_manager.html', context)


def edit_manager_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")
    else:
        manager_id = request.POST.get('manager_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try: 
            user = CustomUser.objects.get(id=manager_id)
            user.email = email
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # INSERTING into manager Model
            manager_model = Managers.objects.get(admin=manager_id)
            manager_model.address = address
            manager_model.save()

            messages.success(request, "manager modifier avec succes.")
            return redirect('/edit_manager/'+ manager_id)

        except:
            messages.error(request, "Failed to Update Manager.")
            return redirect('/edit_manager/' + manager_id)


def delete_manager(request, manager_id):
    manager = Managers.objects.get(admin=manager_id)
    try:
        manager.delete()
        messages.success(request, "Manager Deleted Successfully.")
        return redirect('manage_manager')
    except:
        messages.error(request, "Failed to Delete Manager.")
        return redirect('manage_manager')
    

def add_responsablerh(request):
    return render(request, "hod_template/responsablerh/add_responsablerh.html")

def add_responsablerh_save(request):
    if request.method != "POST":
        messages.error(request, "Méthode Invalide !")
        return redirect('add_responsablerh')
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
      

        try:
            user = CustomUser.objects.create_user( email=email,username=username, password=password, first_name=first_name, last_name=last_name, user_type="3")
            user.responsablerhs.address = address
            user.save()
            messages.success(request, "Responsable RH ajouté avec succes !")
            return redirect('add_responsablerh')
        except:
            messages.error(request, "Erreur ajout Responsable RH !")
            return redirect('add_responsablerh')


def manage_responsablerh(request):
    responsablerhs = Responsablerhs.objects.all()
    context = {
        "responsablerhs": responsablerhs
    }
    return render(request, 'hod_template/responsablerh/manage_responsablerh.html', context)


def edit_responsablerh(request, responsablerh_id):
    responsablerh = Responsablerhs.objects.get(admin=responsablerh_id)
    context = {
        "responsablerh": responsablerh,
        "id": responsablerh_id
    }
    return render(request, 'hod_template/responsablerh/edit_responsablerh.html', context)


def edit_responsablerh_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")
    else:
        responsablerh_id = request.POST.get('responsablerh_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try: 
            user = CustomUser.objects.get(id=responsablerh_id)
            user.email = email
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # INSERTING into manager Model
            responsablerh_model = Responsablerhs.objects.get(admin=responsablerh_id)
            responsablerh_model.address = address
            responsablerh_model.save()

            messages.success(request, "Données Responsable RH modifiées avec succes.")
            return redirect('/edit_responsablerh/'+ responsablerh_id)

        except:
            messages.error(request, "Erreur de modification données Responsable RH ")
            return redirect('/edit_responsablerh/' + responsablerh_id)


def delete_responsablerh(request, responsablerh_id):
    responsablerh = Responsablerhs.objects.get(admin=responsablerh_id)
    try:
        responsablerh.delete()
        messages.success(request, "Responsable RH Deleted Successfully.")
        return redirect('manage_responsablerh')
    except:
        messages.error(request, "Failed to Delete responsable RH.")
        return redirect('manage_responsablerh')

        
def add_director(request):
    return render(request, "hod_template/director/add_director.html")

def add_director_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_director')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type="4")
            user.directors.address = address
            user.save()
            messages.success(request, "Director Added Successfully!")
            return redirect('add_director')
        except:
            messages.error(request, "Failed to Add Director!")
            return redirect('add_director')
        
def manage_director(request):
    directors = Directors.objects.all()

    context = {
        "directors": directors
    }
    return render(request, 'hod_template/director/manage_director.html', context)


def edit_director(request, director_id):
    director = Directors.objects.get(admin=director_id)
    context = {
        "director": director,
        "id": director_id
    }
    return render(request, 'hod_template/director/edit_director.html', context)


def edit_director_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")
    else:
        director_id = request.POST.get('director_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try: 
            user = CustomUser.objects.get(id=director_id)
            user.email = email
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # INSERTING into director Model
            director_model = Directors.objects.get(admin=director_id)
            director_model.address = address
            director_model.save()

            messages.success(request, "Données directeur modifiées avec succes.")
            return redirect('/edit_director/'+ director_id)

        except:
            messages.error(request, "Erreur de modification données directeur ")
            return redirect('/edit_director/' + director_id)


def delete_director(request, director_id):
    director = Directors.objects.get(admin=director_id)
    try:
        director.delete()
        messages.success(request, "directeur Deleted Successfully.")
        return redirect('manage_director')
    except:
        messages.error(request, "Failed to Delete directeur.")
        return redirect('manage_director')
    
    
def add_employee(request):
    form = AddEmployeeForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/employer/add_employee.html', context)


def add_employee_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_employee')
    else:
        form = AddEmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            manager_id = form.cleaned_data['manager_id']
            department_id = form.cleaned_data['departement_id']
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type="1")
                user.employees.address = address

                manager_obj = Managers.objects.get(id=manager_id)
                user.employees.manager_id = manager_obj

                department_obj = Department.objects.get(id=department_id)
                user.employees.department_id = department_obj

                user.employees.gender = gender
                user.employees.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "employees ajouter avec succes !")
                return redirect('add_employee')
            except:
                messages.error(request, "Failed to Add employees !")
                return redirect('add_employee')
        else:
            return redirect('add_employee')


def manage_employee(request):
    employees = Employees.objects.all()
    context = {
        "employees": employees
    }
    return render(request, 'hod_template/employer/manage_employee.html', context)


def edit_employee(request, employee_id):
    # Adding Student ID into Session Variable
    request.department['employee_id'] = employee_id

    employee = Employees.objects.get(admin=employee_id)
    form = EditEmployeeForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = employee.admin.email
    form.fields['username'].initial = employee.admin.username
    form.fields['first_name'].initial = employee.admin.first_name
    form.fields['last_name'].initial = employee.admin.last_name
    form.fields['address'].initial = employee.address
    form.fields['manager_id'].initial = employee.manager_id.id
    form.fields['gender'].initial = employee.gender
    form.fields['department_id'].initial = employee.department_id.id

    context = {
        "id": employee_id,
        "username": employee.admin.username,
        "form": form
    }
    return render(request, "hod_template/employer/edit_employee.html", context)


def edit_employee_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        employee_id = request.department.get('employee_id')
        if employee_id == None:
            return redirect('/manage_employee')

        form = EditEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            manager_id = form.cleaned_data['manager_id']
            gender = form.cleaned_data['gender']
            department_id = form.cleaned_data['department_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=employee_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                employee_model = Employees.objects.get(admin=employee_id)
                employee_model.address = address

                manager = Managers.objects.get(id=manager_id)
                employee_model.manager_id = manager

                department_obj = Department.objects.get(id=department_id)
                employee_model.department_id = department_obj


                employee_model.gender = gender
                if profile_pic_url != None:
                    employee_model.profile_pic = profile_pic_url
                employee_model.save()
                # Delete student_id SESSION after the data is updated
                del request.department['employee_id']

                messages.success(request, "employees mis a jour avec Succes !")
                return redirect('/edit_employee/'+employee_id)
            except:
                messages.success(request, "Failed to Uupdate employee.")
                return redirect('/edit_employee/'+employee_id)
        else:
            return redirect('/edit_employee/'+employee_id)


def delete_employee(request, employee_id):
    employee = Employees.objects.get(admin=employee_id)
    try:
        employee.delete()
        messages.success(request, "employee suprimer avec Succes.")
        return redirect('manage_employee')
    except:
        messages.error(request, "Failed to Delete employee.")
        return redirect('manage_employee')





@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
        

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)
        
def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def employee_profile(request):
    pass


def manager_profile(requtest):
    pass

def hr_profile(requtest):
    pass


