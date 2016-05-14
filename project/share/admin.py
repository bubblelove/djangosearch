from django.contrib import admin
from .models import Type, Ebook

# Register your models here.

class EbookAdmin(admin.ModelAdmin):
	list_display = ('name', 'author', 'types')
	list_filter = ['pub_date', 'types']
	search_fields = ['name', 'author']
admin.site.register(Ebook, EbookAdmin)
admin.site.register(Type)
