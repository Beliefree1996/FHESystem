# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Cateory(models.Model):
    id = models.AutoField(primary_key=True)
    cateory_name = models.CharField(max_length=50, null=False, verbose_name="分类名称")

    def __str__(self):
        return self.cateory_name

    class Meta:
        verbose_name_plural = "分类"


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    cateory = models.ForeignKey(Cateory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "博文内容"


class GetNum(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    number = models.IntegerField()

    def __str__(self):
        return self.date

    class Meta:
        verbose_name_plural = "网站访问情况"


class Wage(models.Model):
    id = models.AutoField(primary_key=True)
    IC_num = models.CharField(max_length=20)
    pf = models.FloatField()
    ss = models.FloatField()
    date = models.IntegerField()

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name_plural = "个人信息"


class UserIC(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    IC_num = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name_plural = "用户身份信息"
