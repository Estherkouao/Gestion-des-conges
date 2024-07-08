from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Responsablerhs, Directors, Managers, Department, Employees, LeaveRequest, Notification

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Responsablerhs)
admin.site.register(Directors)
admin.site.register(Managers)
admin.site.register(Department)
admin.site.register(Employees)
admin.site.register(LeaveRequest)
admin.site.register(Notification)
