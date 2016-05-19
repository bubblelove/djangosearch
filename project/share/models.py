# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Type(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):	
		return self.name

class Ebook(models.Model):
	name = models.CharField(max_length=20)
	author = models.CharField(max_length=30)
	brief = models.CharField(max_length=200)
	pub_date = models.DateField('date published') #default=datetime.datetime.now().date()
	types = models.ForeignKey(Type)
	count = models.IntegerField(blank=True, null=True)
	pub_at = models.CharField(max_length=15) 
	
	def __unicode__(self):#中文编码用unicode这个方法
		return self.name

	def was_published_recently(self):
		now = timezone.now()
		return now >= self.pub_date >= timezone.now() - datetime.timedelta(days=3)
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'


class UserProfile(models.Model):
	user=models.OneToOneField(User,unique=True,verbose_name=('用户'))
	realname = models.CharField(max_length=20,blank=True, null=True)
	phone = models.IntegerField(blank=True, null=True)
	birth_date = models.DateField('your birthday', blank=True, null=True)
	head = models.FileField(upload_to = 'static', blank=True)
	address = models.CharField(max_length=200,default='',blank=True, null=True)

	def __unicode__(self):
		return self.user.username
#先得到user，然后通过user提供的get_profile()来得到profile对象,比如user.get_profile().phone
#通过user模型得到user的id,就可以通过UserProfile模型来操作对应的profile信息
'''    user=User()  
    profile=UserProfile()  
    profile.user_id=user.id  
    profile.phone=phone  
    profile.save()  '''
