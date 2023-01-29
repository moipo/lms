from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.shortcuts import reverse
from itertools import chain

class Subject(models.Model):
    title = models.CharField(max_length=200, default = '', blank = True)
    description = models.TextField( default = '', blank = True)
    image = models.ImageField(upload_to = "uploads/subjects/", blank = True , null=True, default = "test.png")
    teacher = models.ForeignKey("Teacher", blank = True, null = True, on_delete = models.SET_NULL)
    st_group = models.ForeignKey("StGroup", blank = True, null = True, on_delete = models.SET_NULL)


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

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    st_group = models.ForeignKey("StGroup", blank = True, null = True, on_delete = models.SET_NULL)
    profile_picture = models.ImageField(upload_to = "uploads/profile_pictures/%Y/%m", blank = True, null = True)
    
    def __str__(self):
        return self.user.username
    
    def get_all_tasks_by_type(self,some_type):
        ans_common_tasks = AnsweredCommonTask.objects.filter(student = self, status = some_type)
        taken_tests = TakenTest.objects.filter(student = self, status = some_type)
        info_tasks = AnsweredInfoTask.objects.filter(student = self, status = some_type)
        tasks = list(chain(ans_common_tasks, taken_tests, info_tasks))
        # ans_tasks.sort(key = lambda task : task.finished_at)
        return tasks   
   

# class Grade(models.Model):
#     grade = models.IntegerField(null = True, blank = True)
    # student = models.ForeignKey("Student", blank = True, null = True, on_delete = models.SET_NULL)
    # answered_task = models.OneToOne("AnsweredTask", blank = True, null = True, on_delete = models.SET_NULL)

class Teacher(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    profile_picture = models.ImageField(upload_to = "uploads/profile_pictures/%Y/%m", blank = True, null = True)
    

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
        return str(self.__class__.__name__)


class CommonTask(Task):
    file = models.FileField(upload_to = "uploads/common_tasks/", blank = True, null = True)
    
    def __str__(self):
        return self.title

class Test(Task):
    slug = models.SlugField(max_length = 120 , blank = True, null = True, unique = True)
    link = models.CharField(max_length=1000, default = '')
    image = models.ImageField(upload_to = "uploads/", blank = True , null=True, default = "test.png")

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title) + '-' + str(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.slug}/'

class InfoTask(Task):
    file = models.FileField(upload_to = "uploads/info_tasks/", blank = True, null = True)
    

    def __str__(self):
        return self.title









class AnsweredTask(models.Model):
    ASND = "ASSIGNED"
    DONE = "DONE"
    PSSD = "PASSED"
    EVAL = "EVALUATED"
    CHKD = "CHECKED" #for InfoTask
    #was evaluated, was done
    
    STATUS_CHOICES = (
        (ASND, "Assigned"),
        (DONE, "Done"),
        (PSSD, "Passed"),
        (EVAL, "Evaluated"),
        (CHKD, "CHECKED"),
    )
    
    student = models.ForeignKey("Student", blank = True, null = True, on_delete = models.SET_NULL)
    finished_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    status = models.CharField(max_length = 255, choices=STATUS_CHOICES, default = ASND, blank = True)
    
    class Meta:
        abstract = True
    
    
    def related_task(self): 
        class_name = self.__class__.__name__
        if class_name == "AnsweredCommonTask":
            return self.common_task
        elif class_name == "TakenTest": 
            return self.related_test
        elif class_name == "AnsweredInfoTask":
            return self.related_info_task
    
    # def get_absolute_url(self):
    #     return reverse("t_task_answer", kwargs={"ans_task_type": self.__class__.__name__,
    #                                             "ans_task_id" : self.id})
    



class AnsweredCommonTask(AnsweredTask):
    
    
    
    # grade = models.OneToOneField("Grade", blank = True, null = True, on_delete = models.SET_NULL)
    grade = models.IntegerField(null = True, blank = True)
    answer = models.TextField(null = True, default = "")
    file = models.FileField(upload_to = "uploads/answered_common_tasks/" , blank = True, null = True)
    common_task = models.ForeignKey("CommonTask", blank = True, null = True, on_delete = models.SET_NULL)
    comment_from_teacher = models.TextField(default = "", blank = True)
    
    
    
    def __str__(self):
        return str(self.common_task)

class AnsweredInfoTask(AnsweredTask):
    related_info_task = models.ForeignKey("InfoTask", blank = True, null = True, on_delete = models.SET_NULL)
    
    # was_checked = models.BooleanField(blank = True, null = True)



class TakenTest(AnsweredTask):
    # grade = models.OneToOneField("Grade", blank = True, null = True, on_delete = models.SET_NULL)
    grade = models.IntegerField(null = True, blank = True)
    related_test = models.ForeignKey ("Test", on_delete = models.CASCADE, null = True)
    score = models.IntegerField(blank = True, null = True)
    
    

    def __str__(self):
        return str(self.related_test)














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
