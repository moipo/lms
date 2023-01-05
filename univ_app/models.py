from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from itertools import chain

class Subject(models.Model):
    title = models.CharField(max_length=200, default = '', blank = True)
    description = models.TextField( default = '', blank = True)
    image = models.ImageField(upload_to = "uploads/subjects/", blank = True , null=True, default = "test.png")

    def __str__(self):
        return self.title

    @property
    def all_tasks(self):
        common_tasks = self.commontask_set.all()
        info_tasks = self.infotask_set.all()
        test_tasks = self.test_set.all()
        tasks = list(chain(common_tasks, info_tasks, test_tasks))
        tasks.sort(key = lambda task : task.created_at)
        return tasks

class StGroup(models.Model):
    title = models.CharField(max_length=200, default = '', blank = True)
    subject = models.ForeignKey("Subject", blank = True, null = True, on_delete = models.SET_NULL)
    student = models.ForeignKey("Student", blank = True, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Grade(models.Model):
    grade = models.IntegerField(null = True, blank = True)
    # student = models.ForeignKey("Student", blank = True, null = True, on_delete = models.SET_NULL)
    # answered_task = models.OneToOne("AnsweredTask", blank = True, null = True, on_delete = models.SET_NULL)

class Teacher(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey("Subject", blank = True, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.user.first_name


class Task(models.Model):
    title = models.CharField(max_length=200, default = '', blank = True) #this field is present in Test itself
    description = models.TextField(default = '', blank = True) #this field is present in Test itself
    subject = models.ForeignKey("Subject", blank = True, null = True, on_delete = models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True, null = True, blank = True)
    created_by = models.ForeignKey("Teacher", blank = True, null = True, on_delete = models.SET_NULL)

    class Meta:
        abstract = True

    def get_type(self):
        return self.__class__.__name__


class CommonTask(Task):
    file = models.FileField(upload_to = "uploads/common_tasks/", blank = True, null = True)

class Test(Task):
    slug = models.SlugField(max_length = 120 , blank = True, null = True)
    link = models.CharField(max_length=1000, default = '')
    image = models.ImageField(upload_to = "uploads/", blank = True , null=True, default = "test.png")

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.slug}/'

class InfoTask(Task):
    file = models.FileField(upload_to = "uploads/info_tasks/", blank = True, null = True)











class AnsweredTask(models.Model):
    student = models.ForeignKey("Student", blank = True, null = True, on_delete = models.SET_NULL)
    finished_at = models.DateTimeField(blank = True, null = True)

    class Meta:
        abstract = True



class AnsweredCommonTask(AnsweredTask):
    grade = models.OneToOneField("Grade", blank = True, null = True, on_delete = models.SET_NULL)
    answer = models.TextField()
    file = models.FileField(upload_to = "uploads/answered_common_tasks/")


class AnsweredInfoTask(AnsweredTask):
    was_checked = models.BooleanField(blank = True, null = True)



class TakenTest(AnsweredTask):
    grade = models.OneToOneField("Grade", blank = True, null = True, on_delete = models.SET_NULL)
    related_test = models.ForeignKey ("Test", on_delete = models.CASCADE, null = True)
    score = models.IntegerField()
















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





class AnsweredQuestion(models.Model):
    related_taken_test = models.ForeignKey ("TakenTest", on_delete = models.CASCADE, null = True)
    related_question = models.ForeignKey ("Question", on_delete = models.CASCADE, null = True)
    correct = models.BooleanField(default = False)


class GivenAnswer(models.Model):
    related_answered_question = models.ForeignKey ("AnsweredQuestion", on_delete = models.CASCADE, null = True)
    checked = models.BooleanField(default = False)
