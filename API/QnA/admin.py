from django.contrib import admin

from models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name",)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'rid', 'title', 'created', 'modified')

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(ResetEntry)

admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Keyword)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Message)
admin.site.register(Answer)
admin.site.register(Comment)
