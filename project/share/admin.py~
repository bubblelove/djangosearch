from django.contrib import admin
from .models import Type, Ebook, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

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
      
admin.site.unregister(User)  
admin.site.register(User,UserProfileAdmin) 
