# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ebook, UserProfile, KeepBook, Type, Advice, Tribune, Comment
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ChangePasswordForm, AuthorForm, RecommendForm, AdviceForm, BbsForm, CommentForm
from django.template import RequestContext
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
import datetime
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from PIL import Image, ImageDraw, ImageFont   
from project.settings import BASE_DIR  
import cStringIO, string, os, random 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

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
					return HttpResponseRedirect('/share/change_password/')
				else:
					return HttpResponse("password must be matched!")
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
			return HttpResponseRedirect('/share/changefile/')
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
	return HttpResponseRedirect('/share/')
	
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
	return HttpResponseRedirect('/share/')

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
			return HttpResponseRedirect('/share/recommendlist/')
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
		return HttpResponseRedirect('/share/recommendlist/')
	else:
		return HttpResponse('You do not have this permission')

@login_required
def feedback(request):
	user = request.user
	if request.method == 'POST':
		form = AdviceForm(request.POST)
		if form.is_valid():
			contents = form.cleaned_data['contents']
			phone = form.cleaned_data['phone']
			date = datetime.datetime.now()
			Advice.objects.update_or_create(user=user, contents=contents, date=date, phone=phone)
			return HttpResponse("We have received your advice. We will deal with it as soon as possible")
	else:
		form = AdviceForm()
	return render_to_response('share/advice.html', RequestContext(request,{'form': form }))

def book(request, book_id):
	book = get_object_or_404(Ebook, pk=book_id)
	comment = book.comment_set.all()
	nums = 0
	for i in comment:
		nums = i.score + nums
	num = round(nums/comment.count(), 1) 
	paginator = Paginator(comment, 10)
	page=int(request.GET.get('page','1'))
	if page <1:
		page=1
	try:
		comments = paginator.page(page)
	except PageNotAnInteger:
		comments = paginator.page(1)
	except EmptyPage:
		comments = paginator.page(paginator.num_pages)
	return render(request, 'share/book.html', {'book':book, 'comments':comments, 'num': num })

@login_required
def discuss(request):
	user = request.user
	b = Tribune.objects.order_by('-date')
	after_range_num = 5
	before_range_num = 4
	paginator = Paginator(b, 10)
	page=int(request.GET.get('page','1'))
	if page <1:
		page=1
	try:
		bbs = paginator.page(page)
	except PageNotAnInteger:
		bbs = paginator.page(1)
	except EmptyPage:
		bbs = paginator.page(paginator.num_pages)
	if request.method == 'POST':
		form = BbsForm(request.POST)
		if form.is_valid():
			contents = form.cleaned_data['contents']
			date = datetime.datetime.now()
			Tribune.objects.update_or_create(user=user, contents=contents, date=date)
			return HttpResponseRedirect('/share/discuss/') 
	else:
		form = BbsForm()
		return render_to_response('share/discuss.html', RequestContext(request, {'form': form, 'bbs': bbs }))
		
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return render(request, 'share/ip.html', {'ip': ip})

@login_required
def rate(request, book_id):
	user = request.user
	book = Ebook.objects.get(id=book_id)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			content = form.cleaned_data['comments']
			score = form.cleaned_data['score']
			date = datetime.datetime.now()
			if len(content) >= 20:
				Comment.objects.update_or_create(user=user, book=book, date=date, comments=content, score=score, count=True, available=True)
			else:
				Comment.objects.update_or_create(user=user, book=book, date=date, comments=content, score=score)
			return HttpResponseRedirect(reverse('share:book', args=(book_id,)))
	else:
		form = CommentForm()
		return render_to_response('share/comment.html', RequestContext(request, {'form': form }))

@user_passes_test(lambda u: u.has_perm('share.can_manage'), login_url='/share/')
def cancelcomment(request, book_id, comment_id):
	book = Ebook.objects.get(id=book_id)
	comment = Comment.objects.get(id=comment_id)
	comment.delete()
	return HttpResponseRedirect(reverse('share:book', args=(book_id,)))

@user_passes_test(lambda u: u.has_perm('share.can_manage'), login_url='/share/')
def commentavaliable(request, book_id, comment_id):
	book = Ebook.objects.get(id=book_id)
	comment = Comment.objects.get(id=comment_id)
	comment.available = True
	comment.save()
	return HttpResponseRedirect(reverse('share:book', args=(book_id,)))

@user_passes_test(lambda u: u.has_perm('share.can_manage'), login_url='/share/')
def unavaliable(request, book_id, comment_id):
	book = Ebook.objects.get(id=book_id)
	comment = Comment.objects.get(id=comment_id)
	comment.available = False
	comment.save()
	return HttpResponseRedirect(reverse('share:book', args=(book_id,)))
