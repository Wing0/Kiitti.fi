from django.contrib import admin

# Register your models here.
from models import *

class CustomerAdmin(admin.ModelAdmin):
	list_display = ("name",)


class QuestionAdmin(admin.ModelAdmin):
	list_display = ("title",)

admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Organization)
