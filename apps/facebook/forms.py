from django import forms
from django.contrib.auth import get_user_model

from .models import Post

BAD_WORDS = [
    "idiota",
    "cabron",
    "csm",
    "tarado",
    "gilipollas",
    "imbecil",
    "retrasado",
    "hijo de",
    "mierda",
    "carajo",
    "cagada",
]

# Límites de imagen alineados con el promedio de las redes sociales
# (Instagram: 8 MB, X/Twitter: 5 MB, WhatsApp: 16 MB).
MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE = MAX_IMAGE_SIZE_MB * 1024 * 1024
# MPO es una variante de JPEG usada por algunas cámaras de móvil.
ALLOWED_IMAGE_FORMATS = {"JPEG", "MPO", "PNG", "WEBP"}
ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png", "image/webp")

User = get_user_model()


def has_more_two_words(chain):
    return len(chain.split()) > 2


class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            classes = field.widget.attrs.get("class", "")

            if self.errors.get(field_name):
                classes += " is-invalid"

            field.widget.attrs["class"] = classes.strip()


class PostForm(BootstrapModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dale un título a tu publicación",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
                    "placeholder": "¿Qué estás pensando?",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "d-none",
                    "accept": ",".join(ALLOWED_IMAGE_TYPES),
                    "data-max-size": MAX_IMAGE_SIZE,
                }
            ),
        }
        error_messages = {
            "title": {
                "required": "El campo es requerido.",
                "max_length": "El titulo es demasiado largo.",
            },
            "description": {"required": "El campo es requerido."},
        }
        help_texts = {
            "image": (
                "Formatos JPG, PNG o WebP. "
                f"Tamaño máximo: {MAX_IMAGE_SIZE_MB} MB."
            ),
        }

    def as_p(self):
        return self._html_output(
            normal_row="<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s%(errors)s</p>",
            error_row='<ul class="invalid-feedback">%s</ul>',
            row_ender="</p>",
            help_text_html='<span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )

    def clean_title(self):
        title = self.cleaned_data["title"]

        for word in BAD_WORDS:
            if word in title.lower():
                raise forms.ValidationError("Trata de ser respetuoso.")

        return title

    def clean_description(self):
        description = self.cleaned_data["description"]

        for word in BAD_WORDS:
            if word in description.lower():
                raise forms.ValidationError("Trata de ser respetuoso.")

        return description

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        # En edición, si no se sube una imagen nueva, el valor es el archivo
        # que ya estaba guardado en la publicación.
        if not hasattr(image, "content_type"):
            return image

        image_format = getattr(getattr(image, "image", None), "format", "")
        if image_format and image_format.upper() not in ALLOWED_IMAGE_FORMATS:
            raise forms.ValidationError(
                "Formato no permitido. Usa una imagen JPG, PNG o WebP."
            )

        if image.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError(
                f"La imagen no puede superar los {MAX_IMAGE_SIZE_MB} MB."
            )

        return image


class UserForm(BootstrapModelForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "photo"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control", "hidden": ""}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]

        if has_more_two_words(first_name):
            raise forms.ValidationError("Solo puedes tener maximo 2 nombres.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]

        if has_more_two_words(last_name):
            raise forms.ValidationError("Solo puedes tener maximo 2 apellidos.")

        return last_name
