from django.contrib import admin

# Register your models here.
from models import Organization, Topic, Tag, Question, Answer, Comment, User

class CustomerAdmin(admin.ModelAdmin):
	list_display = ("name",)


class QuestionAdmin(admin.ModelAdmin):
	list_display = ("heading",)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(User)
