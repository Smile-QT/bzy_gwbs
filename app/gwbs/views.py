import datetime
import os
import time

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from GWWeb import settings
from app.gwadmin.models import Exam
from app.gwbs.forms import UserLoginForm
from app.gwbs.models import User, UserAnswer, ExamTime, FileInfo
# 登录逻辑
from app.gwbs.tools import RJson


class LoginView(View):
    def get(self, request):
        # 显示登录页面
        # 已登录则跳转到info
        return render(request, 'login/login.html')

    def post(self, request):
        # 获取登录表单
        # 验证表单数据
        # 写入session
        # 写入数据库
        # 跳转
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            candidate_num = user_login_form.cleaned_data['candidate_num']
            password = user_login_form.cleaned_data['password']
            try:
                user = User.objects.get(candidate_num=candidate_num)
                if user.login_ip and (user.login_ip != request.META.get("REMOTE_ADDR")):
                    return render(request, 'login/login.html', locals())

                if user.password == password:
                    # 设置 session
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['candidate_num'] = user.candidate_num
                    # 保存登录信息
                    user.login_os = request.META.get("OS")
                    user.login_ip = request.META.get("REMOTE_ADDR")
                    user.save()
                    return HttpResponseRedirect(reverse("info"))
                else:
                    msg = "密码不正确！"
                    print(msg)
                    return render(request, 'login/login.html', locals())
            except ObjectDoesNotExist:
                msg = "准考证输入有误！"
                print(msg)
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())


# 考试须知
class InfoView(View):
    # 显示页面信息
    # 是否登录，跳转
    # 是否勾选，跳转
    # 判断时间，跳转
    def get(self, request):
        if not request.session.get('is_login', ''):
            return HttpResponseRedirect(reverse("login"))

        user = User.objects.get(id=request.session['user_id'])
        try:
            exam_time = ExamTime.objects.first()
            # 时间戳相减
            end_timestamp = time.mktime(exam_time.exam_end_time.timetuple())
            cur_timestamp = time.mktime(datetime.datetime.now().timetuple())
            count_down = end_timestamp - cur_timestamp
            if count_down <= 0 or user.useranswer.is_over:
                return HttpResponseRedirect(reverse("over"))
        except:
            return render(request, 'gwbs/info.html')
        return render(request, 'gwbs/info.html')

    # 开始考试
    def post(self, request):
        # 判断勾选，并存入
        # 存入开始时间
        is_check = request.POST.get("check1")
        exam_time = ExamTime.objects.first()

        begin_timestamp = time.mktime(exam_time.exam_begin_time.timetuple())
        cur_timestamp = time.mktime(datetime.datetime.now().timetuple())
        if cur_timestamp - begin_timestamp > 0:
            print("考试还未开始！")
        if is_check == "on":
            user_answer = UserAnswer.objects.update_or_create(
                user_id=request.session['user_id'],
                defaults={
                    "user_id": request.session['user_id'],
                    "is_check": True,
                    "is_begin": True,
                }
            )
            print("is_check Ok!")
            return HttpResponseRedirect(reverse("index"))
        else:
            print("is_check Not!")
        return render(request, 'gwbs/info.html')


# 答题界面
class IndexView(View):
    # 页面展示
    def get(self, request):
        # 是否登录，返回到登陆
        # 是否勾选，返回到勾选
        # 获取开考时间
        # 判断时间，没过期传时间，过期跳转到结束
        # 判断上传成功

        if not request.session.get('is_login', ''):
            return HttpResponseRedirect(reverse("login"))

        user = User.objects.get(id=request.session['user_id'])

        if not user.useranswer.is_check:
            return HttpResponseRedirect(reverse("info"))

        exam_time = ExamTime.objects.first()
        # 时间戳相减
        end_timestamp = time.mktime(exam_time.exam_end_time.timetuple())
        cur_timestamp = time.mktime(datetime.datetime.now().timetuple())
        begin_timestamp = time.mktime(exam_time.exam_begin_time.timetuple())
        if begin_timestamp - cur_timestamp > 0:
            return HttpResponseRedirect(reverse("info"))

        print(end_timestamp - cur_timestamp)
        count_down = end_timestamp - cur_timestamp
        if count_down <= 0 or user.useranswer.is_over:
            return HttpResponseRedirect(reverse("over"))

        try:
            exam_info = Exam.objects.first()
            exam_info = exam_info.exam_info
        except:
            exam_info = "题目为空"

        return render(request, 'gwbs/index.html', {
            'count_down': count_down,
            "user_info": user,
            "exam_info": exam_info
        })

    # 交卷逻辑
    def post(self, request):
        # 设置交卷标志、锁定页面
        # 检查文件是否上传

        user = User.objects.get(id=request.session['user_id'])
        if user.useranswer.is_over:
            return RJson(405, "你已交卷，请不要重复提交！", "")

        word_is_up = user.useranswer.word_name
        pdf_is_up = user.useranswer.pdf_name

        if not word_is_up:
            return RJson(404, "请上传 WORD 文件！", "")

        if not pdf_is_up:
            return RJson(404, "请上传 PDF 文件！", "")

        user.useranswer.is_over = True
        user.useranswer.save()
        return RJson(200, "交卷成功！正在跳转....", "")


class OverView(View):
    def get(self, request):
        if not request.session.get('is_login', ''):
            return HttpResponseRedirect(reverse("login"))
        return render(request, 'gwbs/over.html')


# 文件上传逻辑
class Uploader(View):
    def post(self, request):
        # 获取文件对象
        file_obj = request.FILES.get("file1", None)
        # 判断文件是否存在
        if file_obj is None:
            return RJson(404, "请选择文件", "")

        # 获取文件类型
        file_type = file_obj.name.split('.')[1]

        # 转换为小写
        file_type = file_type.lower()

        # 判断文件类型是否合法
        if file_type not in ['doc', 'docx', 'pdf']:
            return RJson(305, "请选择正确的文件类型！", "")
        # 获取交卷状态
        user = User.objects.get(id=request.session['user_id'])
        if user.useranswer.is_over:
            return RJson(405, "你已交卷，请不要重复提交！", "")

        # 获取考室
        can_num = user.candidate_num
        # 创建上传目录
        path = os.path.join(settings.MEDIA_ROOT, 'upload/0{0}考室/{1}'.format(user.room_num, can_num))
        if os.path.exists(path):
            print("目录已经存在")
        else:
            os.makedirs(path)
        file_name = None
        if file_type == "pdf":
            # 如果pdf文件存在
            if user.useranswer.pdf_name:
                exists_file = os.path.join(path, user.useranswer.pdf_name)
                if os.path.exists(exists_file):
                    os.remove(exists_file)
            file_name = '{0}_{1}.{2}'.format(can_num, user.name, file_type)
            UserAnswer.objects.filter(user_id=request.session['user_id']).update(
                pdf_name=file_name)
        elif file_type in ["docx", "doc"]:
            if user.useranswer.word_name:
                exists_file = os.path.join(path, user.useranswer.word_name)
                if os.path.exists(exists_file):
                    os.remove(exists_file)

            file_name = '{0}_{1}.{2}'.format(can_num, user.name, file_type)
            UserAnswer.objects.filter(user_id=request.session['user_id']).update(
                word_name=file_name)

        file_path = os.path.join(path, file_name)
        print(file_path)
        # 写入文件
        f = open(file_path, 'wb+')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        # 保存上传文件记录
        FileInfo.objects.create(
            user_id=request.session['user_id'],
            file_name=file_name,
            file_path=file_obj.name,
            file_type=file_type
        )
        return RJson(200, "上传成功！", "")
