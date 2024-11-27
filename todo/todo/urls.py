"""
URL configuration for todo_pet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from app_todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    
    path('read', views.read_all, name='read_all'),
    path('delete', views.delete_task, name='delet_task'),
    path('update', views.update_task, name='update_all'),
    path('create', views.create_task, name='create_task'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_custom, name='login'),
    path('register/', views.register, name='register'),

]

