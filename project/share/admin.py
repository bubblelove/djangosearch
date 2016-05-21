from django.contrib import admin
from .models import Type, Ebook, UserProfile, KeepBook, Comment, Tribune, Advice
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.unregister(User) 
class EbookAdmin(admin.ModelAdmin):
	list_display = ('name', 'author', 'types')
	list_filter = ['pub_date', 'types']
	search_fields = ['name', 'author']
admin.site.register(Ebook, EbookAdmin)
admin.site.register(Type)

class UserProfileInline(admin.StackedInline):  
	model=UserProfile  
	fk_name='user'  
	max_num=1  
      
class UserProfileAdmin(UserAdmin):  
	inlines = [UserProfileInline, ]  
       
admin.site.register(User,UserProfileAdmin) 

admin.site.register(KeepBook)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('comments', 'score')

admin.site.register(Comment, CommentAdmin)

class TribuneAdmin(admin.ModelAdmin):
	list_display = ('contents', )

admin.site.register(Tribune, TribuneAdmin)

class AdviceAdmin(admin.ModelAdmin):
	list_display = ('contents', 'phone')

admin.site.register(Advice, AdviceAdmin)
