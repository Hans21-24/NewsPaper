from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'heading',
            'text',
            'category_type',
       ]

        labels = {
            'author': 'Автор',
            'heading': 'Заголовок',
            'text': 'Текст',
            'category_type': 'Категория'
        }

    def clean_name(self):
        name = self.cleaned_data["heading"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы."
            )
        return name
