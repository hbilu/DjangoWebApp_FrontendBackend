"""
URL configuration for assignment_project project.

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
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView
from users.views import UserListView, UpdateUserStatusView

urlpatterns = [
    path('', TemplateView.as_view(template_name="main_page.html"), name='main_page'),
    # REST API routes 
    path('api/', include([
        path('users/', UserListView.as_view(), name='api_user_list'),
        path('status/', UpdateUserStatusView.as_view(), name='api_update_status'),
    ])), 
    path('users/', include('users.urls')), # UI routes for users
    path('films/', include('films.urls')), 
    path('admin/', admin.site.urls), # Admin panel
]
