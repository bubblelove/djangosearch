# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ebook
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from django.template import RequestContext
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from PIL import Image, ImageDraw, ImageFont   
from project.settings import BASE_DIR  
import cStringIO, string, os, random 

# HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
# Create your views here.

def index(request):
	if request.user.is_authenticated():
		user = request.user
	else:
		user = request.user
	booklist = Ebook.objects.order_by('id')[:5]
	context = {'booklist': booklist}
#book = Ebook.objects.get(pk=ebook_id)
#question = get_object_or_404(Question, pk=question_id)
	return render(request, 'share/index.html', context)

def register(request):
	errors = []
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			password2 = form.cleaned_data['password2']
			email = form.cleaned_data['email']
			filterResult = User.objects.filter(username=username)
			if len(filterResult)>0:  
				errors.append('user is already in use.') 
				return render_to_response('share/register.html', RequestContext(request,{'form': form, 'errors':errors}))
			filteremail = User.objects.filter(email=email)
			if len(filteremail)>0:  
				errors.append('email already been registered.') 
				return render_to_response('share/register.html', RequestContext(request,{'form': form, 'errors':errors}))
			if password == password2:
				p = make_password(password)
				user = User()
				user.username = username
				user.password = p
				user.email = email
				user.save()
				return render_to_response('share/success.html',{'username':username})
			else:
				errors.append('password must be matched.')  
				return render_to_response('share/register.html', RequestContext(request,{'form': form, 'errors':errors}))

	else:
		form = RegisterForm()
	return render_to_response('share/register.html', RequestContext(request,{'form': form, 'errors':errors}))

def login(request):
	errors = []
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login_user(request, user)
					return HttpResponseRedirect('/share/')
			else:
				errors.append('username or password wrong!')
				return render_to_response('share/login.html', RequestContext(request,{'form': form, 'errors':errors})) 
	else:
		form = LoginForm()
	return render_to_response('share/login.html', RequestContext(request,{'form': form, 'errors':errors}))

@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/share/')

@login_required
def change_password(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			username = request.user.username
			oldpassword = form.cleaned_data['oldpassword']
			password = form.cleaned_data['password']
			password2 = form.cleaned_data['password2']
			user = authenticate(username=username, password=oldpassword)
			if user is not None and user.is_active:
				if password == password2:
					user.set_password(password)
					user.save()
					return HttpResponse("Successfully Modification")
				else:
					print("password must be matched!")
	else:
		form = ChangePasswordForm()
	return render(request, 'share/change_password.html', {'form': form})
