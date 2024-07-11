from django.urls import path, include
from . import views
from .import EmployeeViews, HrViews, DirectorViews, HODViews, ManagerViews

# url admin
urlpatterns = [
    path('', views.loginPage, name='login'),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),

    path('admin_profile/', HODViews.admin_profile, name="admin_profile"),
    path('admin_home/', HODViews.adminhod_home, name="adminhod_home"),
    path('check_email_exist/', HODViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HODViews.check_username_exist, name="check_username_exist"),

    path('add_manager/', HODViews.add_manager, name="add_manager"),
    path('add_manager_save/', HODViews.add_manager_save, name="add_manager_save"),
    path('manage_manager/', HODViews.manage_manager, name="manage_manager"),
    path('edit_manager/<int:manager_id>/', HODViews.edit_manager, name="edit_manager"),
    path('edit_manager_save/', HODViews.edit_manager_save, name="edit_manager_save"),
    path('delete_manager/<int:manager_id>/', HODViews.delete_manager, name="delete_manager"),


    path('add_responsablerh/', HODViews.add_responsablerh, name="add_responsablerh"),
    path('add_responsablerh_save/', HODViews.add_responsablerh_save, name="add_responsablerh_save"),
    path('manage_responsablerh/', HODViews.manage_responsablerh, name="manage_responsablerh"),
    path('edit_responsablerh/<int:responsablerh_id>/', HODViews.edit_responsablerh, name="edit_responsablerh"),
    path('edit_responsablerh_save/', HODViews.edit_responsablerh_save, name="edit_responsablerh_save"),
    path('delete_responsablerh/<int:responsablerh_id>/', HODViews.delete_responsablerh, name="delete_responsablerh"),


    path('add_director/', HODViews.add_director, name="add_director"),
    path('add_director_save/', HODViews.add_director_save, name="add_director_save"),
    path('manage_director/', HODViews.manage_director, name="manage_director"),
    path('edit_director/<int:director_id>/', HODViews.edit_director, name="edit_director"),
    path('edit_director_save/', HODViews.edit_director_save, name="edit_director_save"),
    path('delete_director/<int:director_id>/', HODViews.delete_director, name="delete_director"),


    path('add_employee/', HODViews.add_employee, name="add_employee"),
    path('add_employee_save/', HODViews.add_employee_save, name="add_employee_save"),
    path('manage_employee/', HODViews.manage_employee, name="manage_employee"),
    path('edit_employee/<int:employee_id>/', HODViews.edit_employee, name="edit_employee"),
    path('edit_employee_save/', HODViews.edit_employee_save, name="edit_employee_save"),
    path('delete_employee/<int:employee_id>/', HODViews.delete_employee, name="delete_employee"),


    path('admin_profile/', HODViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HODViews.admin_profile_update, name="admin_profile_update"),


 # url manager
   path('manager_home/', ManagerViews.manager_home, name="manager_home"),
   path('manager/<int:manager_id>/liste_employee', ManagerViews.liste_employee, name="liste_employee"),
   path('manager/<int:manager_id>/conge_attente', ManagerViews.conge_attente, name="conge_attente"),
   path('manager/<int:manager_id>/leave_balance', ManagerViews.leave_balance, name="leave_balance"),

   
   path('manager_profile/', ManagerViews.manager_profile, name="manager_profile"),
   path('manager_profile_update/', ManagerViews.manager_profile_update, name="manager_profile_update"),
   
   
]
