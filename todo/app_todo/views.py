
import logging
import pytz
import json
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate, decorators, login, forms
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404

from  app_todo.models import New_Task, Rem_Task_Id
from app_todo.tasks import reminder
from todo.celery import app
from .forms import RegistrationForm



logger = logging.getLogger(__name__)


def index(request):
        return render(request, "app_todo/base.html")


@csrf_exempt
def create_task(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)
        text_task = body.get("text_task")
        end_time = body.get("end_time")
        rem_time = body.get("rem_time")

        if not text_task:
            return JsonResponse({"error": "Task text is required"}, status=400)

        new_task = New_Task()
        new_task.task = text_task
        new_task.status = False
        new_task.user = request.user

        if end_time:
            msk_timezone = pytz.timezone("Europe/Moscow")
            new_task.date_complete = msk_timezone.localize(
                datetime.datetime.fromisoformat(end_time)
            )

        new_task.save()

        if end_time and rem_time:
            end_dt = datetime.datetime.fromisoformat(end_time)
            rem_dt = datetime.datetime.fromisoformat(rem_time)

            if end_dt > rem_dt:
                msk_timezone = pytz.timezone("Europe/Moscow")
                remind_time = msk_timezone.localize(rem_dt)
                result = reminder.apply_async(
                    args=(text_task,), eta=remind_time.astimezone(pytz.utc)
                )
                remind_id = result.id

                new_rem_id = Rem_Task_Id()
                new_rem_id.task = new_task
                new_rem_id.remind_id = remind_id
                new_rem_id.save()

        return JsonResponse({"message": "Task created successfully"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


@decorators.login_required()
def read_all(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        # Получение задач текущего пользователя
        all_tasks = New_Task.objects.filter(user=request.user).order_by("id")

        data = serializers.serialize('json', all_tasks)

        return HttpResponse(data, content_type='application/json')

    except Exception as e:
        logger.error(f"Error retrieving tasks: {e}", exc_info=True)


@csrf_exempt
def delete_task(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Method not allowed")

    try:
        # Парсинг тела запроса
        body = json.loads(request.body)
        task_id = body.get("task_id")

        if not task_id:
            return JsonResponse({"error": "Task ID is required"}, status=400)

        # Получение задачи
        task = New_Task.objects.get(id=int(task_id))

        # Удаление задачи
        task.delete()
        return JsonResponse({"message": "Task deleted successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    except New_Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    except Exception as e:
        logger.error(f"Error deleting task: {e}", exc_info=True)
        return JsonResponse({"error": "An error occurred while deleting the task"}, status=500)


@csrf_exempt
def update_task(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)
        task_id = body.get("pk")
        new_text = body.get("newText")
        new_date_end = body.get("newDateEnd")
        new_date_rem = body.get("newDateRem")

        if not task_id:
            return JsonResponse({"error": "Task ID is required"}, status=400)

        # Получение задачи
        task = get_object_or_404(New_Task, id=int(task_id))

        # Обновление текста задачи
        if new_text:
            task.task = new_text

        # Обновление даты завершения
        if new_date_end:
            msk_timezone = pytz.timezone("Europe/Moscow")
            task.date_complete = msk_timezone.localize(datetime.datetime.fromisoformat(new_date_end))

        task.save()

        # Обновление напоминания
        if new_date_rem:
            update_reminder(task, new_text, new_date_end, new_date_rem)

        return JsonResponse({"message": "Task updated successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        return JsonResponse({"error": "An error occurred while updating the task"}, status=500)


def update_reminder(task, new_text, new_date_end, new_date_rem):
    """
    Обновление напоминания для задачи.
    """
    try:
        msk_timezone = pytz.timezone("Europe/Moscow")

        # Проверка, есть ли напоминание
        pk_rem_id = get_object_or_404(Rem_Task_Id, task=task)

        # Отмена текущего напоминания
        if pk_rem_id.remind_id:
            app.control.revoke(pk_rem_id.remind_id, terminate=False)

        # Проверка и установка нового напоминания
        new_end_dt = datetime.datetime.fromisoformat(new_date_end)
        new_rem_dt = datetime.datetime.fromisoformat(new_date_rem)

        if new_end_dt > new_rem_dt:
            msk_reminder = msk_timezone.localize(new_rem_dt)
            reminder_result = reminder.apply_async(
                args=(new_text,),
                eta=msk_reminder.astimezone(pytz.utc)  # Используем UTC
            )
            pk_rem_id.remind_id = reminder_result.id
            pk_rem_id.save()

    except Exception as e:
        logger.error(f"Error updating reminder: {e}", exc_info=True)
        raise


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_custom(request):
    if request.method == 'POST':
        form = forms.AuthenticationForm(request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "неверное имя пользователя или пароль")
    else:
        form = forms.AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})