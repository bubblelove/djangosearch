# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ebook, UserProfile, KeepBook, Type
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ChangePasswordForm, AuthorForm, RecommendForm
from django.template import RequestContext
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
import datetime
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
		profile = UserProfile.objects.get(user_id=user.id)
		head = profile.head
		lists = user.keepbook_set.all()
	else:
		user = request.user
		profile = None
		head = None
		lists = None
	booklist = Ebook.objects.order_by('id')#[:5]
	context = {'booklist': booklist, 'head':head, 'lists':lists,}
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
				u = User.objects.get(username = username)
				profile = UserProfile()
				profile.user_id = u.id
				profile.save()
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
					return HttpResponse("Successfully Modification! But please relogin")
				else:
					print("password must be matched!")
	else:
		form = ChangePasswordForm()
	return render(request, 'share/change_password.html', {'form': form})

@login_required
def changefile(request):
	user = request.user
	profile = UserProfile.objects.get(user_id=user.id)
	if request.method == 'POST':
		form = AuthorForm(request.POST, request.FILES)
		if form.is_valid():
			profile.realname = form.cleaned_data['realname']
			profile.birth_date = form.cleaned_data['birth_date']
			profile.head = form.cleaned_data['head']
			profile.phone = form.cleaned_data['phone']
			profile.save()
			return HttpResponse("Successfully upload!")
	else:
		form = AuthorForm()
	return render(request, 'share/changefile.html', {'form': form})

@login_required
def mycentral(request):
	user = request.user
	profile = UserProfile.objects.get(user_id=user.id)
	return render(request, 'share/selfcentral.html', {'profile': profile, 'user':user})

@login_required
def keep(request, book_id):
	user = request.user
	book = Ebook.objects.get(id=book_id)
	date = datetime.datetime.now()
	KeepBook.objects.update_or_create(user=user, book=book, date=date)
	return HttpResponse('keep succuess!')
	
@login_required
def keeplist(request):
	user = request.user
	lists = user.keepbook_set.all()
	return render(request, 'share/mykeep.html', {'lists': lists})

@login_required
def cancel(request, book_id):
	user = request.user
	book = Ebook.objects.get(id=book_id)
	c = user.keepbook_set.filter(book=book)
	c.delete()
	return HttpResponse('cancel success!')

@login_required
def recommend(request):
	errors = []
	user = request.user
	book = Ebook()
	if request.method == 'POST':
		form = RecommendForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data['name']
			author = form.cleaned_data['author']
			b = Ebook.objects.filter(name=name, author=author)
			if b:
				errors.append('This book has been recommended.') 
				return render_to_response('share/recommend.html', RequestContext(request,{'form': form, 'errors':errors}))
			book.name = name
			book.author = author
			book.brief = form.cleaned_data['brief']
			book.pub_date = form.cleaned_data['pub_date']
			book.types = form.cleaned_data['types']
			book.pub_at = form.cleaned_data['pub_at'] 
			book.pic = form.cleaned_data['pic'] 
			book.content = form.cleaned_data['content'] 
			book.references = user
			book.save()
			return HttpResponse('Recommended success!')
	else:
		form = RecommendForm()
	return render_to_response('share/recommend.html', RequestContext(request,{'form': form, 'errors':errors}))

@login_required
def recommendlist(request):
	user = request.user
	lists = user.ebook_set.all()
	return render(request, 'share/myrecommend.html', {'lists': lists})

@login_required
def cancelbook(request, book_id):
	user = request.user
	book = Ebook.objects.get(id=book_id)
	if user == book.references:
		book.delete()
		return HttpResponse('cancel success!')
	else:
		return HttpResponse('You do not have this permission')
