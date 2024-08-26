from django import forms 
from django.forms import Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Field, Div, Row, Column
from gestion_congé_app.models import Managers, Department, LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'leave_type': forms.Select(choices=[
                ('MALADIE', 'Maladie'),
                ('CONGE', 'Congé'),
                ('MARIAGE', 'Mariage'),
                ('DECES', 'Décès')
            ]),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(LeaveRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('leave_type', css_class='form-group col-md-6 mb-0'),
                Column('start_date', css_class='form-group col-md-3 mb-0'),
                Column('end_date', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Div('reason', css_class='form-group'),
            Submit('submit', 'soumetre', css_class='btn btn-primary')
        )

class DateInput(forms.DateInput):
    input_type = "date"


class AddEmployeeForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (('Male','Male'),('Female','Female'))

    manager_id = forms.ChoiceField(label="Manager", choices=[], widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    department_id = forms.ChoiceField(label="Department", choices=[], widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager_id'].choices = self.get_manager_choices()
        self.fields['department_id'].choices = self.get_department_choices()

    def get_manager_choices(self):
        try:
            managers = Managers.objects.all()
            return [(manager.id, f"{manager.admin.first_name} {manager.admin.last_name}") for manager in managers]
        except Managers.DoesNotExist:
            return []

    def get_department_choices(self):
        try:
            departments = Department.objects.all()
            return [(department.id, department.name) for department in departments]
        except Department.DoesNotExist:
            return []

class EditEmployeeForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (('Male','Male'),('Female','Female'))

    manager_id = forms.ChoiceField(label="Manager", choices=[], widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    department_id = forms.ChoiceField(label="Department", choices=[], widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager_id'].choices = self.get_manager_choices()
        self.fields['department_id'].choices = self.get_department_choices()

    def get_manager_choices(self):
        try:
            managers = Managers.objects.all()
            return [(manager.id, f"{manager.admin.first_name} {manager.admin.last_name}") for manager in managers]
        except Managers.DoesNotExist:
            return []

    def get_department_choices(self):
        try:
            departments = Department.objects.all()
            return [(department.id, department.name) for department in departments]
        except Department.DoesNotExist:
            return []

    
from django import forms
from .models import LeaveRequest

class LeaveRequestCommentForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['manager_comment']
        widgets = {
            'manager_comment': forms.Textarea(attrs={'rows': 4}),
        }

class LeaveRequestCommentrhForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['hr_comment']
        widgets = {
            'hr_comment': forms.Textarea(attrs={'rows': 4}),
        }        

