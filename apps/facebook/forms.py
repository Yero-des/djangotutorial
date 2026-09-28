from django import forms
from .models import Post

BAD_WORDS = [
    'idiota', 'cabron', 'csm', 'tarado', 'gilipollas', 'imbecil', 'retrasado', 'hijo de'
]

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
    
    def as_p(self):
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s%(errors)s</p>',
            error_row='<ul class="invalid-feedback">%s</ul>',
            row_ender='</p>',
            help_text_html='<span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )
        
    def clean_title(self):
        title = self.cleaned_data['title']     
        
        for word in BAD_WORDS:
            if word in title.lower():
                raise forms.ValidationError('Trata de ser respetuoso')                

        return title
    
    def clean_body(self):
        body = self.cleaned_data['body']
        
        for word in BAD_WORDS:
            if word in body.lower():
                raise forms.ValidationError('Trata de ser respetuoso')
            
        return body