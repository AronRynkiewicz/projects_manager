from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Position(models.Model):
    position_choices = (
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    )
    position_name = models.CharField(choices=position_choices, max_length=20)
    reading_rights = models.BooleanField(default=False)
    saving_rights = models.BooleanField(default=False)
    adding_employees = models.BooleanField(default=False)
    removing_employees = models.BooleanField(default=False)

    def __str__(self):
        return self.position_name


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    possible_roles = (
        ('Client', 'Client'),
        ('Employee', 'Employee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(choices=possible_roles, max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    mail = models.EmailField()

    def __str__(self):
        return '({}) {} {}'.format(
            self.role,
            self.name,
            self.surname,
        )


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return '(Team) {}'.format(self.team_name)


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
    )
    teams = models.ManyToManyField(
        Team,
    )

    def __str__(self):
        return '(Employee) {} {}'.format(
            self.profile.name,
            self.profile.surname,
        )


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='client_files/')

    def __str__(self):
        return self.file_name


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=50)
    task_description = models.TextField()
    assigned_team = models.ManyToManyField(
        Team,
    )
    files = models.ManyToManyField(
        File,
    )

    def __str__(self):
        return self.task_name


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    task = models.ManyToManyField(
        Task,
    )

    def __str__(self):
        return '(Client) {} {}'.format(
            self.profile.name,
            self.profile.surname
        )
