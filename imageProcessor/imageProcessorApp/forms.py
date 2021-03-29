from django import forms
from .models import ImageProcessorModel


class ImageProcessorForm(forms.ModelForm):
    class Meta:
        model = ImageProcessorModel
        fields = ['photo',]