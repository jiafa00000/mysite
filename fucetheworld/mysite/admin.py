from django.contrib import admin
from .models import Article,Tag,Classification,Author,Saying
# Register your models here.

class AritcleAdmin(admin.ModelAdmin):
	list_display=('title','author','publish_time',)
	class Media:
		js = (
		'/static/tinymce/tinymce.min.js',
		'/static/tinymce/config.js', 
		)

class SayingAdmin(admin.ModelAdmin):
	list_display=('title','content')


admin.site.register(Article,AritcleAdmin),
admin.site.register(Tag),
admin.site.register(Classification),
admin.site.register(Author),
admin.site.register(Saying),