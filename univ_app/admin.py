from django.contrib import admin
from .models import *


class AnswerAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Answer._meta.fields]

class QuestionAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Question._meta.fields]

class TestAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]

class GivenAnswerAdmin(admin.ModelAdmin):
    list_display = ["id","related_answered_question" , "checked"]

class AnsweredQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "related_taken_test", "related_question", "correct"]

class TakenTestAdmin(admin.ModelAdmin):
    list_display = ["id", "related_test", "score"]


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)


admin.site.register(GivenAnswer,GivenAnswerAdmin)
admin.site.register(AnsweredQuestion,AnsweredQuestionAdmin)
admin.site.register(TakenTest,TakenTestAdmin)
