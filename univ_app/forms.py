from .models import *
from django import forms
from django.contrib.auth.models import User


class GivenAnswerForm(forms.ModelForm):
    class Meta:
        model = GivenAnswer
        fields = ("checked",)
        labels = {"checked" : " "}



class AnswerFormNotModel(forms.Form):
    answer = forms.CharField(max_length=200, widget = forms.Textarea , label = "Ответ")
    is_right = forms.BooleanField(required = False, label = "является верным")

    is_right.widget.attrs.update({'value':"1",'placeholder':'Является верным'})
    answer.widget.attrs.update({'cols':'90','rows':'1', 'placeholder':'Ответ'})



class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
            'title',
            'description',
            'image',
        ]

        labels = {
            "title" : "Название теста",
            "description" : "Описание",
            'image': "Картинка",
        }










class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question',
        ]

        labels = {
            "question" : "Текст вопроса",
        }



class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs.update(
        {'class': 'form-control',
         'style':' placeholder : "Вопрос"; width:700px; height:25px;  display:inline-block;',
         })
        self.fields['is_right'].widget.attrs.update({'class': 'form-check-input',
        "style": " display:inline-block;"})

    class Meta:
        model = Answer
        fields = [
            'answer',
            'is_right',
        ]

        labels = {
            "is_right" : "Ответ является правильным ",
            'answer': "Ответ",
        }



class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
        {'class': 'form-control',
         'style':' placeholder : "Логин"',})
        self.fields['password'].widget.attrs.update(
        {'class': 'form-control',
         'style':' placeholder : "Пароль"',})

    class Meta:
        model = User
        fields = [
        'username',
        'password',
        ]
        labels = {
        "username" : "имя пользователя",
        "password" : "пароль"
        }
        help_texts = {'username' : " "}

        widgets= {
            'password' :  forms.PasswordInput(attrs = {'class' : 'form-control'})
        }


class CommonTaskForm(forms.ModelForm):
    class Meta:
        model = CommonTask
        fields = ["title", 'description', 'file']
        labels = {
            "title": "название",
            "description" : "описание",
        }
    def __init__(self, *args, **kwargs):
        super(CommonTaskForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class InfoTaskForm(forms.ModelForm):
    class Meta:
        model = InfoTask
        fields = ["title", 'description', 'file']
        labels = {
            "title": "название",
            "description" : "описание",
        }
    def __init__(self, *args, **kwargs):
        super(InfoTaskForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class AnsweredCommonTaskForm(forms.ModelForm):
    class Meta:
        model = AnsweredCommonTask
        fields = ['answer', 'file']
        labels = {
            "description" : "описание",
            'file': "прикрепить документ",
        }
    def __init__(self, *args, **kwargs):
        super(AnsweredCommonTaskForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class PictureForm(forms.Form):
    field_name = forms.ImageField( required = False)
    

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc']
        labels = {
            'doc': "Выберете документ для добавления",
        }
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})