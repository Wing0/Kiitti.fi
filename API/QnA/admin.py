from django.contrib import admin

# Register your models here.
<<<<<<< HEAD
from models import Question, Tag, Vote, Organization, Answer, Comment, User
=======
from models import Organization, Topic, Tag, Question, Answer, Comment, User
>>>>>>> d87f7a21f8cdfa112faebc797c6924dd34a857f3

class CustomerAdmin(admin.ModelAdmin):
	list_display = ("name",)


class QuestionAdmin(admin.ModelAdmin):
	list_display = ("topic",)

admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Organization)
