from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    candidate_num = models.CharField(max_length=100, unique=True)
    room_num = models.CharField(max_length=10, default="0")
    password = models.CharField(max_length=256, default="123456")
    login_ip = models.GenericIPAddressField(null=True)
    login_os = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class UserAnswer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_check = models.BooleanField(default=False,)
    is_begin = models.BooleanField(default=False)
    is_over = models.BooleanField(default=False)
    word_name = models.CharField(max_length=500, null=True)
    pdf_name = models.CharField(max_length=500, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class FileInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=500)
    file_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class TimeInfo(models.Model):
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ExamTime(models.Model):
    exam_name = models.CharField(max_length=100)
    exam_begin_time = models.DateTimeField()
    exam_end_time = models.DateTimeField()
