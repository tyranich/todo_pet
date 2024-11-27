from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class New_Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=50, name='task')
    status = models.BooleanField()
    date_complete = models.DateTimeField(default=None, null=True)


class Rem_Task_Id(models.Model):
    task = models.OneToOneField(New_Task, on_delete=models.CASCADE, primary_key=True)
    remind_id = models.CharField(max_length=100, name='remind_id')