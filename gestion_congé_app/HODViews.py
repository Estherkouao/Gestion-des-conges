from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from gestion_congé_app.models import (
    CustomUser, HRs, Directors, Managers, Department, Employees
)


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
    context={
        "all_employee_count" : all_employee_count,
        "all_manager_count" : all_manager_count,
        
    }

    return render(request, "hod_template/home_content.html", context)


def add_manager(request):
    return render(request, "hod_template/add_manager.html")

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
    return render(request, 'hod_template/manage_manager.html', context)


def edit_manager(request, manager_id):
    manager = Managers.objects.get(admin=manager_id)
    context = {
        "manager": manager,
        "id": manager_id
    }
    return render(request, 'hod_template/edit_manager.html', context)


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
    


def add_Hr(request):
    return render(request, "hod_template/add_Hr.html")


def add_Hr_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_Hr')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type="3")
            user.Hrs.address = address
            user.save()

            messages.success(request, "Hr ajouté avec succes !")
            return redirect('add_Hr')
        except:
            messages.error(request, "Erreur ajout Hr !")
            return redirect('add_Hr')

def manage_Hr(request):
    Hrs= HRs.objects.all()

    context = {
        "Hrs": Hrs,
       
    }
    return render(request, 'hod_template/manage_Hr.html', context)

def edit_Hr(request, Hr_id):
    Hr = HRs.objects.get(admin=Hr_id)
    context = {
        "Hr": Hr,
        "id": Hr_id
    }
    return render(request, 'hod_template/edit_Hr.html', context)

def edit_Hr_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")
    else:
        Hr_id = request.POST.get('Hr_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=Hr_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

               # INSERTING into HRS Model
            Hr_model = HRs.objects.get(admin=Hr_id)
            Hr_model.address = address
            Hr_model.save()

            messages.success(request, "Hr Updated Successfully.")
            return redirect('/edit_Hr/' + Hr_id)

        except:
            messages.error(request, "Failed to Update Hr.")
            return redirect('/edit_Hr/' + Hr_id)

def delete_Hr(request, Hr_id):
    Hr = HRs.objects.get(admin=Hr_id)
    try:
       Hr.delete()
       messages.success(request, "Hr Deleted Successfully.")
       return redirect('manage_Hr')
    except:
        messages.error(request, "Failed to Delete Hr.")
        return redirect('manage_Hr')
    

        
def add_director(request):
    return render(request, "hod_template/add_director.html")

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
        "directors": directors,
    }
    return render(request, 'hod_template/manage_director.html', context)

def edit_director(request, director_id):
    director = Directors.objects.get(admin=director_id)
    context = {
        "director": director,
        "id": director_id
    }
    return render(request, 'hod_template/edit_ director.html', context)

def edit_director_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")
    else:
        director_id = request.POST.get(' Director_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id= director_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

               # INSERTING into  Directors Model
            director_model = HRs.objects.get(admin= director_id)
            director_model.address = address
            director_model.save()

            messages.success(request, " director Updated Successfully.")
            return redirect('/edit_ director/' + director_id)

        except:
            messages.error(request, "Failed to Update director.")
            return redirect('/edit_ director/' +  director_id)

def delete_director(request,  director_id):
    director=  Directors.objects.get(admin=director_id)
    try:
       director.delete()
       messages.success(request, " director_id Deleted Successfully.")
       return redirect('manage_ director')
    except:
        messages.error(request, "Failed to Delete  director.")
        return redirect('manage_director')




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



def employee_feedback_message(request):
    feedbacks = FeedBackemployee.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackemployee.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def employee_feedback_message(request):
    feedbacks = FeedBackemployee.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def employee_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackemployee.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportEmployees.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def manager_leave_reject(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('manager_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportEmployees.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def employee_leave_approve(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('employee_leave_view')


def hr_leave_reject(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    leave.leave_status = 3
    leave.save()
    return redirect('hr_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


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


