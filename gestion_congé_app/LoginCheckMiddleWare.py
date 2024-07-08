from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "gestion_congé_app.EmployeeViews":
                    pass
                elif modulename == "gestion_congé_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("employee_home")
            
            elif user.user_type == "2":
                if modulename == "gestion_congé_app.ManagerViews":
                    pass
                elif modulename == "gestion_congé_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("manager_home")
            
            elif user.user_type == "3":
                if modulename == "gestion_congé_app.HrViews":
                    pass
                elif modulename == "gestion_congé_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("responsablerh_home")
                
                 
            elif user.user_type == "4":
                if modulename == "gestion_congé_app.DirectorViews":
                    pass
                elif modulename == "gestion_congé_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("director_home")
                
                    
            elif user.user_type == "5":
                if modulename == "gestion_congé_app.HODViews":
                    pass
                elif modulename == "gestion_congé_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("adminhod_home")

            else:
                return redirect("login")

        else:
            if request.path == reverse("login") or request.path == reverse("doLogin"):
                pass
            else:
                return redirect("login")