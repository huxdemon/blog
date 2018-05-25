from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import VerifyCode

# 登录
class LoginForm(forms.Form):
    # 在大部分情况下，字段都具有一个合理的默认Widget。
    # 例如，默认情况下，CharField 具有一个TextInput Widget，它在HTML 中生成一个<input type="text">
    # attrs让widget 具有一些特殊的CSS 类。 可以指定‘type’ 属性使用的是新的输入类型
    # 这里使class的类型是form-control
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # def clean(self):
    #     cleaned_data = super(LoginForm, self).clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #
    #     def __init__(self, user, *args, **kwargs):
    #         self.user = user
    #         super(LoginForm, self).__init__(*args, **kwargs)
    #
    #     if self.user is False:
    #         raise forms.ValidationError("用户验证失败！")


# 注册
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    # 用来抛出错误
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')  # 拿数据
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        #  创建一个列表，将错误传入，以便同时显示错误
        error_list = list()
        if User.objects.filter(username=username).count():
            error_list.append(ValidationError("用户已存在！"))
        if password1 != password2:
            error_list.append(forms.ValidationError("输入密码不一致！"))
        if len(error_list):
            raise forms.ValidationError(error_list)


# 更改密码
class ResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # 继承了之前的，同时也写入了自己的方法
        # 既能使用之前的，也能使用自己覆写的
        super(ResetForm, self).__init__(*args, **kwargs)

    def clean(self):
        clean_data = super(ResetForm, self).clean()
        old_password = clean_data.get('old_password')
        new_password1 = clean_data.get('new_password1')
        new_password2 = clean_data.get('new_password2')

        error_list = list()
        if self.user.check_password(old_password) is False:
            error_list.append(ValidationError("原密码错误！"))
        if new_password1 != new_password2:
            error_list.append(ValidationError("输入密码不一致！"))
        if len(error_list):
            raise forms.ValidationError(error_list)


#  找回密码-发送邮件
class Forget_emailForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


# 找回密码-输入验证码
class Forget_codeForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        clean_data = super(Forget_codeForm, self).clean()
        code = clean_data.get('code')
        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')
        verify_code = VerifyCode.objects.filter(code=code).count()

        error_list = list()
        if password1 != password2:
            error_list.append(forms.ValidationError("输入密码不一致！"))
        if verify_code is None:
            error_list.append(forms.ValidationError("输入验证码错误！"))
        if len(error_list):
            raise forms.ValidationError(error_list)


# 找回密码-重置密码
# class Forget_confirmForm(forms.Form):
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#
#     def clean(self):
#         clean_data = super(Forget_confirmForm, self).clean()
#         password1 = clean_data.get('password1')
#         password2 = clean_data.get('password2')
#
#         if password1 != password2:
#             raise forms.ValidationError("输入密码不一致！")