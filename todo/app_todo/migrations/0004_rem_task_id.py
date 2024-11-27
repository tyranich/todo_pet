# Generated by Django 5.1.2 on 2024-10-30 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_todo', '0003_new_task_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rem_Task_Id',
            fields=[
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app_todo.new_task')),
                ('remind_id', models.CharField(max_length=100)),
            ],
        ),
    ]
