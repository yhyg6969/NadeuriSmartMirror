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


urlpatterns = [
    path('main/', views.main, name='main'),
    path('popup_modal/', views.popup_modal, name='popup_modal'),
    path('Xplaywall/', include('Xplaywall.urls'), name="Xplaywall"),
    path('Xfloor/', include('Xfloor.urls'), name="Xfloor"),
    path('smartmirror/', include('smartmirror.urls'), name="smartmirror"),
    path('inbody/', include('inbody.urls'), name="inbody"),
    path('ranking/', include('ranking.urls'), name="ranking"),
    path('management/', include('management.urls'), name="management"),
]
