# -*- coding:utf-8 -*-
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label="用户名:", max_length=100, required=True,  error_messages={'required': '请输入用户名'})
	password = forms.CharField(label="密码:", error_messages={'required': u'请输入密码'}, widget=forms.PasswordInput())

class RegisterForm(forms.Form):
	username = forms.CharField(label="用户名:", max_length=100, required=True,  error_messages={'required': '请输入用户名'})#widget=forms.TextInput(attrs={'placeholder':u"用户名",})
	password = forms.CharField(label="密码:", error_messages={'required': u'请输入密码'}, widget=forms.PasswordInput())
	email = forms.EmailField()
	phone = forms.IntegerField()

class UserfileForm(forms.Form):
	realname = forms.CharField()
	age = forms.IntegerField()
	
# def clean(self):
        #if not self.is_valid():
         #   raise forms.ValidationError(u"用户名和密码为必填项")
        #else:
         #   cleaned_data = super(LoginForm, self).clean()

class HandimgForm(forms.Form):
	headimg = forms.FileField()
