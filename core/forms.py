from typing import Any, Mapping, Optional
from django import forms
from django.core.files.base import File
from .models import ContactMessage, Image

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit, Row, Column

class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"multiple": "multiple", "accept": "image/*"}),
        required=True,
        help_text="format [.jpg .png .gif]"
    )
    class Meta:
        model = Image
        fields = ("image", "description")
    
    def __init__(self, data=None, files=None, instance=None ) -> None:
        super().__init__(data=data, files=files, instance=instance)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            
                Column('image',Column(css_class="img-display row"), css_class="col-12"),
                
                Column("description", css_class="col-12")
            
        )


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", 'email', "message")
