from celery import shared_task
import time
from .models import New_Task
import datetime

@shared_task(name="cheked_overdue_tasks")
def cheked_overdue_tasks():
    tasks = New_Task.objects.filter(overdue=False)

    for task in tasks:
        print(task.id)
        if task.date_complete.time() < datetime.datetime.now().time():
            task.overdue = True


@shared_task(name="reminder_task")
def reminder_task():
    tasks = New_Task.objects.filter(date_complete__isnull=False)
    for task in tasks:
        if (task.date_complete - datetime.timedelta(hours=1)) == datetime.datetime.now():
            pass 
            print("reminder task id - {}")
            """
            to do 
            запускаем таск который отправляет задачу напоминания в бот
            """
        if task.overdue == False:
            if task.date_complete < datetime.datetime.now():
                task.overdue = True
                task.save()

@shared_task(name="reminder")
def reminder(task):
   
    print("task {} ready".format(task))