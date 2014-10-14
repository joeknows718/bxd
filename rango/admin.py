from django.contrib import admin
from rango.models import Category, Page, Event, UserProfile


class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')


admin.site.register(Page, PageAdmin)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(UserProfile)