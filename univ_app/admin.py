from django.contrib import admin
from .models import *



class SubjectAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Subject._meta.fields]
admin.site.register(Subject, SubjectAdmin)

class StGroupAdmin(admin.ModelAdmin):
    list_display = [x.name for x in StGroup._meta.fields]
admin.site.register(StGroup, StGroupAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Student._meta.fields]
admin.site.register(Student, StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Teacher._meta.fields]
admin.site.register(Teacher, TeacherAdmin)

class CommonTaskAdmin(admin.ModelAdmin):
    list_display = [x.name for x in CommonTask._meta.fields]
admin.site.register(CommonTask, CommonTaskAdmin)

class AnsweredCommonTaskAdmin(admin.ModelAdmin):
    list_display = [x.name for x in AnsweredCommonTask._meta.fields]
admin.site.register(AnsweredCommonTask, AnsweredCommonTaskAdmin)








#tester
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
