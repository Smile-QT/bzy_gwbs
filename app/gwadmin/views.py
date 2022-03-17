# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from app.gwadmin.forms import AdminUserLoginForm, GwExamTimeForm
from app.gwadmin.models import Exam, AdminUser
from app.gwbs.models import ExamTime as ExamTimeModel, User
from app.gwbs.models import User as UserModel


# 登录逻辑
class LoginView(View):
    def get(self, request):
        # 显示登录页面
        # 已登录则跳转
        return render(request, 'gwadmin/login/login.html')

    def post(self, request):
        # 获取登录表单
        # 验证表单数据
        # 写入session
        # 写入数据库
        # 跳转
        print(request.POST)
        user_form = AdminUserLoginForm(request.POST)
        if user_form.is_valid():
            name = user_form.cleaned_data['name']
            password = user_form.cleaned_data['password']
            print(name)
            try:
                user = AdminUser.objects.get(name=name)
                if user.password == password:
                    # 设置 session
                    request.session['name'] = name
                    request.session['room_num'] = user.room_num
                    # 保存登录信息
                    user.login_os = request.META.get("OS")
                    user.login_ip = request.META.get("REMOTE_ADDR")
                    user.save()
                    msg = {
                        "code": 200,
                        "msg": "登录成功！"
                    }

                    return JsonResponse(msg, safe=False)
                else:
                    msg = {
                        "code": 401,
                        "msg": "密码不正确！"
                    }
                    return JsonResponse(msg, safe=False)
            except ObjectDoesNotExist:
                msg = {
                    "code": 402,
                    "msg": "用户名不存在！"
                }
                return JsonResponse(msg, safe=False)
        else:
            msg = {
                "code": 403,
                "msg": "请输入正确的用户名和密码！"
            }
            return JsonResponse(msg, safe=False)


def logout(request):
    # 1. 将session中的用户名、昵称删除
    request.session.flush()
    # 2. 重定向到 登录界面
    return HttpResponseRedirect(reverse("gwlogin"))


class GwAdmin(View):
    def get(self, request):
        if not request.session.get('name', ''):
            return HttpResponseRedirect(reverse("gwlogin"))
        data = {
            "msg": "msg",
        }
        return render(request, 'gwadmin/index.html', locals())


class GwShow(View):
    def get(self, request):
        room_num = request.session.get("room_num", "")
        print(room_num)
        if room_num in ["0", ]:
            user_list = UserModel.objects.all()
        else:
            user_list = UserModel.objects.filter(room_num=room_num).all()

        msg = {
            "sum": user_list.count(),
            "num1": 0.,
            "num2": 0,
        }
        return JsonResponse(msg, safe=False)


class GwUser(View):
    def get(self, request):
        if not request.session.get('name', ''):
            return HttpResponseRedirect(reverse("gwlogin"))
        room_num = request.session.get("room_num", "")
        print(room_num)
        if room_num in ["0", ]:
            user_list = UserModel.objects.all()
        else:
            user_list = UserModel.objects.filter(room_num=room_num).all()
        print(user_list)
        return render(request, 'gwadmin/user.html', locals())


class GwUserAnswer(View):
    def get(self, request):
        if not request.session.get('name', ''):
            return HttpResponseRedirect(reverse("gwlogin"))
        room_num = request.session.get("room_num", "")
        if room_num in ["0", ]:
            user_list = User.objects.all()
        else:
            user_list = User.objects.filter(room_num=room_num).all()
        print(user_list)
        return render(request, 'gwadmin/user_answer.html', locals())


class GwExamTime(View):
    def get(self, request):
        if not request.session.get('name', ''):
            return HttpResponseRedirect(reverse("gwlogin"))
        user_list = ExamTimeModel.objects.all()
        print(user_list)

        return render(request, 'gwadmin/exam_time.html', locals())

    def post(self, request):
        time_form = GwExamTimeForm(request.POST)
        if time_form.is_valid():
            begin_time = time_form.cleaned_data['begin_time']
            end_time = time_form.cleaned_data['end_time']
            print(begin_time)
            print(end_time)
            exam_time = ExamTimeModel.objects.first()

            exam_time.exam_begin_time = begin_time
            exam_time.exam_end_time = end_time
            exam_time.save()
            msg = {
                "code": 200,
                "msg": "保存成功！"
            }
            return JsonResponse(msg, safe=False)
        else:
            msg = {
                "code": 404,
                "msg": "请先选择日期！"
            }
            return JsonResponse(msg, safe=False)


class GwExamImport(View):
    def get(self, request):
        if not request.session.get('name', ''):
            return HttpResponseRedirect(reverse("gwlogin"))
        exam_list = Exam.objects.first()
        print(exam_list)

        return render(request, 'gwadmin/exam.html', locals())

    def post(self, request):
        exam_info = request.POST.get('exam_content')

        exam = Exam.objects.first()
        exam.exam_info = exam_info
        exam.save()
        msg = {
            "code": 200,
            "msg": "保存成功！"
        }
        return JsonResponse(msg, safe=False)
