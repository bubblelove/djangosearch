#-*- coding:utf-8 -*- 
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ebook, User
from .forms import LoginForm, RegisterForm, HandimgForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from django import forms
from django.template import RequestContext
#1.比较纯文本密码和数据库中哈希后的密码,两个参数：要检查的纯文本密码，和数据库中用户的password字段的完整值   2.创建哈希密码  3.检查提供的字符串是否可以用check_password()验证
#@login_required
#authenticate()、login()、logout()等函数，分别实现认证、登录、登出等功能。
# Create your views here.
def index(request):
	if request.user.is_authenticated():
		user = request.user
	else:
		user = request.user
	#logout
	booklist = Ebook.objects.order_by('id')[:5]
	context = {'booklist': booklist}
#book = Ebook.objects.get(pk=ebook_id)
#question = get_object_or_404(Question, pk=question_id)
	return render(request, 'book/index.html', context)
#读取数据库
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = request.POST['password']
			user2 = User.objects.filter(username=username)
			user = authenticate(username=username, password=password)
			if user is not None:
				if check_password(user2.password_hash, password):
					login(request, user)
					return  HttpResponseRedirect('/book/')
				else:
					print("error!")
	else:
		form = LoginForm()
	return render(request, 'book/login.html', {'form': form})

def logout(request):
	logout(request)
	return HttpResponseRedirect('/book/')
#if not request.user.is_authenticated():

#Question.objects.get(pk=1)，q.choice_set.all()，q.choice_set.create(choice_text='Not much', votes=0)，q.choice_set.count()
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			realname = request.POST['realname']
			age = request.POST['age']
			email = request.POST['email']
			phone = request.POST['phone']
			hashs = make_password(password)
			if User.objects.filter(username=username) and User.objects.filter(email=email) and User.objects.filter(phone=phone) is None:
				u = User(username=username, password_hash=hashs, realname=realname, age=age, email=email, phone=phone)
				u.save()
				return render_to_response('book/success.html', {'username': username})
			else:
				return HttpResponse("该用户名或邮箱已被注册过！")
	else:
		form = RegisterForm()
	return render(request, 'book/register.html', {'form': form})
	
def search(request):
	return render(request, 'book/search.html')

def books(request, ebook_id):
	ebook = get_object_or_404(Ebook, pk=ebook_id)
	return render(request, 'book/book.html', {'ebook': ebook})

'''from django.contrib.auth import update_session_auth_hash

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    else:'''

def changefile(request):
	if request.method == "POST":
		form= HandimgForm(request.POST,request.FILES)
		if form.is_valid():
			#handle_uploaded_file(request.FILES['headimg'])
			return HttpResponse('upload ok!')
	else:
		form = HandimgForm()
	return render(request, 'book/changefile.html', {'form': form})
