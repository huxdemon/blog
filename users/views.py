from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, ResetForm, Forget_emailForm, Forget_codeForm
from django.core.mail import send_mail
from django.conf import settings
import string
import random
from users.models import VerifyCode
from django.utils import timezone
import datetime
from django.db import models


# Create your views here.
# 登录
def Login(request):
    if request.user.is_authenticated:
        messages.warning(request, "请不要重复登陆!")
        return HttpResponseRedirect(reverse('blog:index'))
    context = dict()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "欢迎！")
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                messages.error(request, "用户验证失败！")
        else:
            messages.error(request, "输入错误！")
    form = LoginForm()
    context['form'] = form
    return render(request, 'users/login.html', context)


# def Login(request):
#     if request.user.is_authenticated:
#         messages.warning(request, "请不要重复登陆!")
#         return HttpResponseRedirect(reverse('blog:index'))
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         # 查找用户是否存在
#         user = authenticate(request, username=username, password=password)
#         if user is None:
#             # 失败
#             messages.error(request, "登陆失败!")
#             return HttpResponseRedirect(reverse('users:login'))
#         else:
#             login(request, user)
#             messages.success(request, "登陆成功!")
#             return HttpResponseRedirect(reverse('blog:index'))
#     return render(request, 'users/login.html')


# 登出
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))


# 注册
def Register(request):
    context = dict()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password1)
            messages.success(request, "注册成功，欢迎登录！")
            return HttpResponseRedirect(reverse('users:login'))
        else:
            context['form'] = form
            return render(request, 'users/register.html', context)
    form = RegisterForm()
    context['form'] = form
    return render(request, 'users/register.html', context)


# def Register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         email = request.POST['email']
#         if username and password1 and password2 and email is False:
#             messages.error(request, '输入不能为空！')
#             return HttpResponseRedirect(reverse('users:register'))
#         elif User.objects.filter(username=username).count():
#             # 用户已存在
#             messages.error(request, '用户已存在！')
#             return HttpResponseRedirect(reverse('users:register'))
#         elif password1 != password2:
#             messages.error(request, '密码不一致！')
#             return HttpResponseRedirect(reverse('users:register'))
#         else:
#             user = User.objects.create_user(username, email, password1)
#             messages.success(request, '注册成功，请登录！')
#             return HttpResponseRedirect(reverse('users:login'))
#     return render(request, 'users/register.html')


# 修改密码
def Reset(request):
    context = dict()
    user = request.user
    if request.method == "POST":
        # 表示request.POST是传给data的，不至于混淆，传参的问题
        form = ResetForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            user.set_password(new_password1)
            user.save()
            messages.success(request, "密码修改成功，请重新登录！")
            logout(request)
            return HttpResponseRedirect(reverse('users:login'))
        else:
            context['form'] = form
            return render(request, 'users/reset.html', context)
    form = ResetForm(user=request.user)
    context['form'] = form
    return render(request, 'users/reset.html', context)


# def Reset(request):
#     if request.method == 'POST':
#         # 1、从前台拿到数据
#         username = request.POST['username']
#         old_password = request.POST['old_password']
#         new_password1 = request.POST['new_password1']
#         new_password2 = request.POST['new_password2']
#         # 2、检查前台数据
#         if username and old_password and new_password1 and new_password2 is False:
#             messages.error(request, '输入不能为空！')
#             return HttpResponseRedirect(reverse('users:reset'))
#         user = request.user
#         if user.check_password(old_password) is False:
#             messages.error(request, '原密码错误！')
#             return HttpResponseRedirect(reverse('users:reset'))
#         elif new_password1 != new_password2:
#             messages.error(request, '密码不一致！')
#             return HttpResponseRedirect(reverse('users:reset'))
#         else:
#             user.set_password(new_password1)
#             user.save()
#             messages.success(request, '密码修改成功！')
#             logout(request)
#             return HttpResponseRedirect(reverse('users:login'))
#     return render(request, 'users/reset.html')


# 找回密码-验证用户名
def ForgetEmail(request):
    context = dict()
    if request.method == "POST":
        form = Forget_emailForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)[0]
            verify_code = ''.join(random.sample(string.digits, 6))
            VerifyCode.objects.get_or_create(user=user, code=verify_code, type=0, is_valid=1,
                                            active_time=timezone.now()+datetime.timedelta(minutes=30))
            subject = '来自huxdemon博客的验证邮件'
            text_content = '你的用户名:' + username + ',验证码:'+verify_code
            send_mail(subject, text_content, settings.EMAIL_FROM, [user.email], html_message=text_content)
            return HttpResponseRedirect(reverse('users:forget_done'))
        else:
            context['form'] = form
            return render(request, 'users/forget_email', context)
    form = Forget_emailForm()
    context['form'] = form
    return render(request, 'users/forget_email.html', context)


# 找回密码-输入验证码
def ForgetDone(request):
    context = dict()
    if request.method == "POST":
        form = Forget_codeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            code = form.cleaned_data['code']
            user = User.objects.filter(username=username)[0]
            user.set_password(password1)
            user.save()
            messages.success(request, "密码更改成功！")
            # verify_code = VerifyCode.objects.filter(code=code)[0]
            return HttpResponseRedirect(reverse('users:login'))
        else:
            context['form'] = form
            return render(request, 'users/forget_done.html', context)
    form = Forget_codeForm()
    context['form'] = form
    return render(request, 'users/forget_done.html', context)


# 找回密码-设新密码
# def ForgetConfirm(request):
#     user = request.user
#     context = dict()
#     if request.method == "POST":
#         form = Forget_confirmForm(request.POST)
#         if form.is_valid():
#             password = form.cleaned_data['password1']
#             user.set_password(password)
#             user.save()
#             messages.success(request, "密码修改成功！")
#             return HttpResponseRedirect(reverse('users:login'))
#         else:
#             context['form'] = form
#             return render(request, 'users/forget_confirm.html', context)
#     form = Forget_confirmForm()
#     context['form'] = form
#     return render(request, 'users/forget_confirm.html', context)