from django.contrib import admin
from .models import Ebook, Type, User

# Register your models here.
#class QuestionAdmin(admin.ModelAdmin):
 #   fieldsets = [
  #      (None,               {'fields': ['question_text']}),
   #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    #]
class EbookAdmin(admin.ModelAdmin):
	list_display = ('name', 'author', 'types')
	list_filter = ['pub_date', 'types']
	search_fields = ['name', 'author']
admin.site.register(Ebook, EbookAdmin)
admin.site.register(Type)

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email')
admin.site.register(User, UserAdmin)
