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


    path('add_Hr/', HODViews.add_Hr, name="add_Hr"),
    path('add_Hr_save/', HODViews.add_Hr_save, name="add_Hr_save"),
    path('manage_Hr/', HODViews.manage_Hr, name="manage_Hr"),
    path('edit_Hr/<int:Hr_id>/', HODViews.edit_Hr, name="edit_Hr"),
    path('edit_Hr_save/', HODViews.edit_Hr_save, name="edit_Hr_save"),
    path('delete_Hr/<int:Hr_id>/', HODViews.delete_Hr, name="delete_Hr"),

    path('add_director/', HODViews.add_director, name="add_director"),
    path('add_director_save/', HODViews.add_director_save, name="add_director_save"),
    path('manage_director/', HODViews.manage_director, name=" manage_director"),
    path('edit_director/<int:director_id>/', HODViews.edit_director, name="edit_director"),
    path('edit_director_save/', HODViews.edit_director_save, name="edit_director_save"),
    path('delete_director/<int:director_id>/', HODViews.delete_director, name="delete_director"),

]
