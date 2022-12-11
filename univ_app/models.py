from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Subject(models.Model):
    title = models.CharField(max_length=200, default = '', blank = True)

class Sgroup(models.Model):
    title = models.CharField(max_length=200, default = '', blank = True)
    subject = models.ForeignKey("Subject", blank = True, null = True, on_delete = models.SET_NULL)


class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", blank = True, null = True, on_delete = models.SET_NULL)

class Teacher(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", blank = True, null = True, on_delete = models.SET_NULL)


class Task(models.Model):
    title = models.CharField(max_length=200, default = '', blank = True) #this field is present in Test itself
    description = models.TextField(default = '', blank = True) #this field is present in Test itself
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey("Teacher", blank = True, null = True, on_delete = models.SET_NULL)
    group = models.ForeignKey("Group", blank = True, null = True, on_delete = models.SET_NULL)
    subject = models.ForeignKey("Teacher", blank = True, null = True, on_delete = models.SET_NULL)

    class Meta:
        abstract = True

class AnsweredTask(Task):
    grade = models.IntegerField(null = True, blank = True )
    finished_at = models.DateTimeField(blank = True, null = True)




# class Student(AbsctractUser):
#     group = models.ForeignKey("Group", blank = True, null = True, on_delete = models.SET_NULL)
#
# class Teacher(AbstractUser):
#     subjects = models.ForeignKey("Subject", blank = True, null = True, on_delete = models.SET_NULL)

# class CommonTask(Task):
#     nested_files = models.FileField()















# тут не будет: семестр, расписание, практики, категорий студентов, административного персонала, зачётки электронной.



























class Test(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length = 120 , blank = True, null = True)
    description = models.TextField(blank = True, default = "")
    link = models.CharField(max_length=1000, default = '')
    image = models.ImageField(upload_to = "uploads/", blank = True , null=True, default = "test.png")
    #upload_to = "uploads/Y%/%m/%d/"
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.slug}/'








class Question(models.Model):
    question = models.TextField(default = "")
    answered_correctly = models.BooleanField(default = False)
    related_test = models.ForeignKey("Test", on_delete=models.CASCADE, null=True )

    def __str__(self):
        return self.question


    def get_test_questions(the_test:Test):
        the_questions = Question.objects.filter(related_test = the_test)
        return the_questions







class Answer(models.Model):
    answer = models.CharField(max_length=1000)
    was_chosen = models.BooleanField(default=False)
    is_right = models.BooleanField(default=False)
    related_question = models.ForeignKey("Question", on_delete=models.CASCADE, null = True)

    def get_answers(the_question:Question):
        the_answers = Answer.objects.filter(related_question = the_question)
        return the_answers

    def __repr__(self):
        return self.answer

    def __str__(self):
        return self.answer



class TakenTest(models.Model):
    related_test = models.ForeignKey ("Test", on_delete = models.CASCADE, null = True)
    score = models.IntegerField()

class AnsweredQuestion(models.Model):
    related_taken_test = models.ForeignKey ("TakenTest", on_delete = models.CASCADE, null = True)
    related_question = models.ForeignKey ("Question", on_delete = models.CASCADE, null = True)
    correct = models.BooleanField(default = False)


class GivenAnswer(models.Model):
    related_answered_question = models.ForeignKey ("AnsweredQuestion", on_delete = models.CASCADE, null = True)
    checked = models.BooleanField(default = False)
