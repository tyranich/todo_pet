# Generated by Django 5.1.1 on 2024-10-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_task',
            name='date_complete',
            field=models.DateTimeField(default=None),
        ),
    ]
