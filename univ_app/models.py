from django.db import models
from django.utils.text import slugify


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
