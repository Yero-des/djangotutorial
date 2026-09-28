from django import forms
from .models import Post

class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            classes = field.widget.attrs.get('class', '')

            if self.errors.get(field_name):
                classes += ' is-invalid'

            field.widget.attrs['class'] = classes.strip()

class PostForm(BootstrapModelForm):
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
        
    def clean_title(self):
        title = self.cleaned_data['title']        
        
        if 'i' in title:
            raise forms.ValidationError('No se puede')

        return title