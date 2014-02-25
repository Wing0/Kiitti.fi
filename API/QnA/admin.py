from django.contrib import admin

# Register your models here.
from models import *

class CustomerAdmin(admin.ModelAdmin):
	list_display = ("name",)


class QuestionAdmin(admin.ModelAdmin):
	list_display = ("title",)

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(ResetEntry)

admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(TagEntry)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Message)
admin.site.register(Answer)
admin.site.register(Comment)
