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
    path('seal/test', views.test),  # 更新公钥
    # path('seal/BFV_kengen', views.BFV_kengen),  # BFV密钥生成
    # path('seal/BFV_Encrypt', views.BFV_Encrypt),  # BFV加密
    # path('seal/BFV_Decrypt', views.BFV_Decrypt),    # BFV解密
    # path('seal/BFV_add', views.BFV_add),  # BFV加
    # path('seal/BFV_mul', views.BFV_mul),  # BFV乘
    # path('seal/CKKS_kengen', views.CKKS_kengen),  # CKKS密钥生成
    # path('seal/CKKS_Encrypt', views.CKKS_Encrypt),  # CKKS加密
    # path('seal/CKKS_Decrypt', views.CKKS_Decrypt),   # CKKS解密
    # path('seal/CKKS_add', views.CKKS_add),   # CKKS加
    # path('seal/CKKS_mul', views.CKKS_mul),   # CKKS乘
]
