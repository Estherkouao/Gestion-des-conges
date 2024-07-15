from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("1", "Employee"),
        ("2", "Manager"),
        ("3", "Responsablerh"),
        ("4", "Director"),
        ("5", "HOD"),
    )
    user_type = models.CharField(default="4", choices=USER_TYPE_CHOICES, max_length=150)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Responsablerhs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Directors(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Managers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    manager_id = models.ForeignKey(Managers, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    leave_balance = models.IntegerField(default=30)

    def reduce_leave_balance(self, days):
        if self.leave_balance >= days:
            self.leave_balance -= days
            self.save()
        else:
            raise ValueError("Insufficient leave balance")
        

        
class AttendanceReport():
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)  # Relate to Employees
    date = models.DateField()
    status = models.CharField(max_length=20)
    objects = models.Manager()

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved by Manager', 'Approved by Manager'),
        ('Rejected by Manager', 'Rejected by Manager'),
        ('Approved by Responsablerh', 'Approved by Rresponsablerh'),
        ('Rejected by Responsablerh', 'Rejected by Rresponsablerh'),
        ('Approved by Director', 'Approved by Director'),
        ('Rejected by Director', 'Rejected by Director'),
    )
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50)
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    manager_comment = models.TextField(blank=True, null=True)
    hr_comment = models.TextField(blank=True, null=True)
    director_comment = models.TextField(blank=True, null=True)

    @property
    def leave_days(self):
        return (self.end_date - self.start_date).days + 1  # Including the end date

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating profile for user type: {instance.user_type}")
        if instance.user_type == "1":
            Employees.objects.create(admin=instance, manager_id=Managers.objects.get(id=1), department_id=Department.objects.get(id=1),  address="")
        elif instance.user_type == "2":
            Managers.objects.create(admin=instance)
        elif instance.user_type == "3":
            Responsablerhs.objects.create(admin=instance)
        elif instance.user_type == "4":
            Directors.objects.create(admin=instance)
        elif instance.user_type == "5":
            AdminHOD.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    print(f"Saving profile for user type: {instance.user_type}")
    if instance.user_type == "1":
        instance.employees.save()
    elif instance.user_type == "2":
        instance.managers.save()
    elif instance.user_type == "3":
        instance.responsablerhs.save()
    elif instance.user_type == "4":
        instance.directors.save()
    elif instance.user_type == "5":
        instance.adminhod.save()

