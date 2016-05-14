# -*- coding:utf-8 -*-
from django import forms
from django.core.validators import validate_email
#如果模型字段设置blank=True，那么表单字段的required 设置为False。否则，required=True。

class RegisterForm(forms.Form):
	username = forms.CharField(label="用户名:", max_length=100, required=True,  error_messages={'required': '请输入用户名'})#widget=forms.TextInput(attrs={'placeholder':u"用户名",})
	password = forms.CharField(label="密码:", error_messages={'required': u'请输入密码'}, widget=forms.PasswordInput())
	password2 = forms.CharField(label="确认密码:", error_messages={'required': u'请输入密码'}, widget=forms.PasswordInput())
	email = forms.EmailField()
	#recipients = MultiEmailField()
	#cc_myself = forms.BooleanField(required=False)
	#phone = forms.IntegerField()


class MultiEmailField(forms.Field):
	def to_python(self, value):
# Return an empty list if no input was given.
		if not value:
			return []
		return value.split(',')

	def validate(self, value):
		super(MultiEmailField, self).validate(value)

		for email in value:
			validate_email(email)


'''如果模型字段设置了choices，那么表单字段的Widget 将设置成Select，其选项来自模型字段的choices。选项通常会包含空选项，并且会默认选择。如果字段是必选的，它会强制用户选择一个选项。如果模型字段的blank=False 且具有一个显示的default 值，将不会包含空选项（初始将选择default 值）class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=3,
                widget=forms.Select(choices=TITLE_CHOICES))
    birth_date = forms.DateField(required=False)

class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
'''