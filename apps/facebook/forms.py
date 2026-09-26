from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
        }
        labels = {
            'title': 'Titulo',
            'body': 'Contenido'
        }
        error_messages = {
            'title': {
                'required': 'El campo es requerido.',
                'max_length': 'El titulo es demasiado largo'
            },
            'body': {
                'required': 'El campo es requerido.'
            }
        }