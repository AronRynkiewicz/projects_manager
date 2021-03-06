from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Position(models.Model):
    position_choices = (
        ('manager', 'manager'),
        ('employee', 'employee'),
    )
    position_name = models.CharField(choices=position_choices, max_length=20)
    reading_rights = models.BooleanField(default=False)
    saving_rights = models.BooleanField(default=False)
    adding_employees = models.BooleanField(default=False)
    removing_employees = models.BooleanField(default=False)


class Profile(models.Model):
    role = {
        True: '(Client)',
        False: '(Employee)',
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    mail = models.EmailField()

    def __str__(self):
        return '{} {} {}'.format(self.role[self.is_client], self.name, self.surname)


class Employee(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    position = models.OneToOneField(
        Position,
        on_delete=models.CASCADE,
    )


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    members = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )


class File(models.Model):
    file_name = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='client_files/')


class Task(models.Model):
    task_name = models.CharField(max_length=50)
    task_description = models.TextField()
    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    files = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
    )


class Client(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
