# forms

from django import forms
from django.contrib.auth.models import User

from app.models import Post, Comment, Report
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as BaseUserChangeForm


class PostForm(forms.ModelForm):
    """
    Форма Поста, нужна для Создания либо Изменения Поста
    """
    title = forms.CharField(max_length=255)
    content = forms.CharField(max_length=3000)

    class Meta:
        model = Post
        fields = ["title", "content"]


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows":"3",
        "placeholder":"Напишите Комментарий..."
        }))

    class Meta:
        model = Comment
        fields = ["body"]

class ReportForm(forms.ModelForm):
    description = forms.CharField(max_length=1024, widget=forms.Textarea(
        attrs={
            "class": "form-controm",
            "rows": 3,
            "placeholder": "Опишите вашу ситуацию"
        }
    ))

    class Meta:
        fields = ["theme", "description"]
        model = Report
        widget = {
            "theme": forms.Select(
                attrs={
                    "class": "form-select"
                }
            )
        }

class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )