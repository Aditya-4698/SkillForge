"""
URL configuration for skillforge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.shortcuts import render
from skills import views
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return render(request, 'home.html')

def test(request):
    return render(request, 'test.html')

urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "",
        views.dashboard,
        name="home"
    ),

    path(
        "test/",
        test,
        name="test"
    ),

    path(
        "skills/",
        include("skills.urls")
    ),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)