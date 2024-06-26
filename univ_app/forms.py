from django import forms
from django.contrib.auth.models import User

from .models import *


class GivenAnswerForm(forms.ModelForm):
    class Meta:
        model = GivenAnswer
        fields = ("checked",)
        labels = {"checked": " "}


class AnswerFormNotModel(forms.Form):
    answer = forms.CharField(max_length=200, widget=forms.Textarea, label="Answer")
    is_right = forms.BooleanField(required=False, label="is correct")

    is_right.widget.attrs.update({"value": "1", "placeholder": "is correct"})
    answer.widget.attrs.update({"cols": "90", "rows": "1", "placeholder": "answer"})


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
            "title",
            "description",
            "image",
        ]

        labels = {
            "title": "Title of the test",
            "description": "Description",
            "image": "Picture",
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question",
        ]

        labels = {
            "question": "question",
        }


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["answer"].widget.attrs.update(
            {
                "class": "form-control",
                "style": ' placeholder : "Question"; width:700px; height:25px;  display:inline-block;',  # pylint: disable=line-too-long
            }
        )
        self.fields["is_right"].widget.attrs.update(
            {"class": "form-check-input", "style": " display:inline-block;"}
        )

    class Meta:
        model = Answer
        fields = [
            "answer",
            "is_right",
        ]

        labels = {
            "is_right": "Answer is correct",
            "answer": "Answer",
        }


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "style": ' placeholder : "Login"',
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "style": ' placeholder : "Password"',
            }
        )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        labels = {"username": "login", "password": "password"}
        help_texts = {"username": " "}

        widgets = {"password": forms.PasswordInput(attrs={"class": "form-control"})}


class CommonTaskForm(forms.ModelForm):
    class Meta:
        model = CommonTask
        fields = ["title", "description", "file"]
        labels = {
            "title": "Title",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        super(CommonTaskForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class InfoTaskForm(forms.ModelForm):
    class Meta:
        model = InfoTask
        fields = ["title", "description", "file"]
        labels = {
            "title": "Title",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        super(InfoTaskForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class AnsweredCommonTaskForm(forms.ModelForm):
    class Meta:
        model = AnsweredCommonTask
        fields = ["answer", "file"]
        labels = {
            "description": "Description",
            "file": "Add a document",
        }

    def __init__(self, *args, **kwargs):
        super(AnsweredCommonTaskForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class PictureForm(forms.Form):
    field_name = forms.ImageField(required=False)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["doc"]
        labels = {
            "doc": "Choose a document to upload",
        }

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
