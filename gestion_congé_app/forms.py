from django import forms 
from django.forms import Form
from gestion_congé_app.models import Managers, Department


class DateInput(forms.DateInput):
    input_type = "date"


class AddEmployeeForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        managers = Managers.objects.all()
        manager_list = []
        for manager in managers:
            single_manager = (manager.id, manager.manager_name)
            manager_list.append(single_manager)
    except:
        manager_list = []
    
    #For Displaying Session Years
    try:
        departments = Department.objects.all()
        department_list = []
        for department in departments:
            single_department = (department.id, str(department.department)+" to "+str(department.department))
            department_list.append(single_department)
            
    except:
        department_list = []
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    manager_id = forms.ChoiceField(label="manager", choices=manager_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    department_id = forms.ChoiceField(label="department", choices=department_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditEmployeeForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying manager
    try:
        managers = Managers.objects.all()
        manager_list = []
        for manager in managers:
            single_manager = (manager.id, manager.manager_name)
            manager_list.append(single_manager)
    except:
        manager_list = []

    #For Displaying Session Years
    try:
        departments = Department.objects.all()
        department_list = []
        for department in departments:
            single_department = (department.id, str(department.department)+" to "+str(department.department_end))
            department_list.append(single_department)
            
    except:
        department_list = []

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    manager_id = forms.ChoiceField(label="manager", choices=manager_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    department_id = forms.ChoiceField(label="departement", choices=department_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
