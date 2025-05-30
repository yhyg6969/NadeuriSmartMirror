"""
URL configuration for CompleteSolution project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
from .views import smartmirror, inquiry, popup_modal, CustomPasswordChangeView
from django.contrib.auth import views as auth_views


app_name = 'smartmirror'


urlpatterns = [
    path('', views.smartmirror, name='smartmirror'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('inquiry/popup_modal/', views.popup_modal, name='popup_modal'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),
    path('logout/', views.logout_view, name='logout'),
]



