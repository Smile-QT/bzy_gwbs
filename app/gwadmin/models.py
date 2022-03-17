from django.db import models


# Create your models here.


class AdminUser(models.Model):
    name = models.CharField(max_length=50, unique=True)
    room_num = models.CharField(max_length=10, default="0")
    password = models.CharField(max_length=256, default="123456")
    login_ip = models.GenericIPAddressField(null=True)
    login_os = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class Exam(models.Model):
    exam_info = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
