from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class PostForm(forms.ModelForm):
    postCategory = forms.ModelMultipleChoiceField(
        label='Category',
        queryset=Category.objects.all(),
    )
    postAuthor = forms.ModelChoiceField(
        label='Author',
        empty_label='Select a author',
        queryset=Author.objects.all(),
    )
    class Meta:
        model = Post
        fields = ['title','text']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Описание не может быть менее 20 символов."
            })

        return cleaned_data