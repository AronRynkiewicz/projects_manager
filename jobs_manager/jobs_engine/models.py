from django.db import models


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


class Employee(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    mail = models.EmailField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
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
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    mail = models.EmailField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
