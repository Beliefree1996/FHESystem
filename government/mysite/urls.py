# -*- coding: UTF-8 -*-
"""vuesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from myapp import views

urlpatterns = [
    # path('', views.index),
    path('admin/', admin.site.urls),
    path('opens/get_info', views.get_info),  # 提供数据接口
    path('opens/add', views.add_data),  # 添加数据
    path('opens/change_data', views.change_data),    # 修改数据
    path('opens/face', views.checkface),  # 人脸识别api
    path('opens/user/getstatus', views.Users.get_status),  # 返回状态 是否登录
    path('opens/user/login', views.Users.login_user),  # 登录
    path('opens/user/logout', views.Users.logout_user),  # 注销
    path('opens/user/register', views.Users.register),   # 注册
]
